# auto transcriber.py
# FloralDew 8/3/2025 started
# Python 3.13.3

import numpy as np
import whisper
import torch
import cv2
import face_recognition # face recognition lib. Find more in README.md
import moviepy
from whisper.audio import pad_or_trim # for language detection preproc
import time
from datetime import timedelta # for time conversion
# use NLLB to translate into English
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# the basic architecture as class
class VideoTranscriber:

    def __init__(self, whisper_model_size = 'base', 
                 device = "cuda" if torch.cuda.is_available() else "cpu",
                 btranslate = False,
                 nllb_model_name = "facebook/nllb-200-distilled-600M"):
        """Initialize models and components"""

        print('Audio Transcriber'.center(60, '='))
        print(f"Using device: {device}")
        
        # Load Whisper model
        print(f"🔧 Setting up Whisper Model...")
        self.whisper_model = whisper.load_model(whisper_model_size, device = device)
        print(f"✅ Whisper Model loaded successfully")

        # Load NLLB if transtation
        if btranslate:
            # Load NLLB model
            print(f"🔧 Setting up NLLB Translation Models...")
            nllb_tokenizer = AutoTokenizer.from_pretrained(nllb_model_name)
            nllb_model = AutoModelForSeq2SeqLM.from_pretrained(nllb_model_name).to(device)
            print(f"✅ NLLB Model loaded successfully")

            language_pairs = [
                {'name': 'ja2en', 'src': 'jpn_Jpan', 'tgt': 'eng_Latn'},
                {'name': 'zh2en', 'src': 'zho_Hans', 'tgt': 'eng_Latn'},
            ]

            # Create translation pipelines
            translators = {}

            print(f"\n🌍 Creating translation pipelines...")
            for config in language_pairs:
                translator = pipeline(
                    'translation',
                    model = nllb_model,
                    tokenizer = nllb_tokenizer,
                    src_lang = config['src'],
                    tgt_lang = config['tgt'],
                    max_length = 512,
                    device = 0 if torch.cuda.is_available() else -1
                )
                translators[config['name']] = translator

                print(f"   ✅ {config['name']}")

            self.translators = translators # a dict

        # Initialize configuration
        self.device = device
        self.btranslate = btranslate

    def extract_and_process_audio(self, video_path: str, tgt_sr = 16000): # 16000 for whisper
        """Extract audio track from video file"""

        print('Extracting and processing audio...'.center(60, '='))
        # load the video
        video = moviepy.VideoFileClip(video_path, audio_fps = tgt_sr)
        audio_moviepy = video.audio # extract audio
        print("✅ audio extraction done!")

        # convert to array
        waveform = audio_moviepy.to_soundarray()

        # Convert to mono
        print(f'   number of audio channels: {waveform.shape[1]}')
        waveform = np.mean(waveform, axis = 1, keepdims = False, dtype = np.float32)

        # Normalize audio (Whisper expects normalized input)
        audio_array = waveform / np.max(np.abs(waveform))
        audio_array = torch.tensor(audio_array, dtype = torch.float32).to(self.device) # convert to torch
        print("✅ audio processing done!")

        extraction_result = {
            'video': video,
            'audio': audio_array,
            'audio_sr': tgt_sr
        }

        audio_moviepy.close() # release resources

        return extraction_result
        
    def build_speaker_database(self, video, interval = 2):
        """Create speaker identification database based on time"""

        print('Performing face recognition...'.center(60, '='))
        known_face_encodings = []
        speaker_database = {}
        for sec in range(0, int(video.duration), interval):
            frame = video.get_frame(sec)
            # Resize frame of video size for faster face recognition processing
            if frame.shape[0] >= 720: # the hight of the frame
                small_frame = cv2.resize(frame, (0, 0), fx = 0.3, fy = 0.3) # in RGB
            elif frame.shape[0] >= 480:
                small_frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5) # in RGB
            elif frame.shape[0] >= 360:
                small_frame = cv2.resize(frame, (0, 0), fx = 0.8, fy = 0.8) # in RGB
            else:
                small_frame = frame
            # Find all the faces and face encodings in the current frame of video
            current_face_locations = face_recognition.face_locations(small_frame, model='cnn') # could use cnn model, but slower
            # a list of encodings of faces in the frame
            current_face_encodings = face_recognition.face_encodings(small_frame, current_face_locations)
            for current_face_encoding in current_face_encodings: # there might be multiple faces in a frame
                if known_face_encodings:
                    # would rather set the tolerance higher to avoid side face being identified as a new person
                    matches = face_recognition.compare_faces(known_face_encodings, current_face_encoding, tolerance = 0.7)
                    face_distances = face_recognition.face_distance(known_face_encodings, current_face_encoding)
                    best_match_index = np.argmin(face_distances) # return the index of the biggest element
                    if not matches[best_match_index]: # face encoding doesn't exist in list as known
                        known_face_encodings.append(current_face_encoding)
                        speaker_database.setdefault(sec, []) # if key doesn't exist, add. else nothing happens
                        speaker_database[sec].append(f'speaker_{len(known_face_encodings)}')
                    else:
                        speaker_database.setdefault(sec, []) # if key doesn't exist, add. else nothing happens
                        speaker_database[sec].append(f'speaker_{best_match_index + 1}') # speaker number = index + 1
                else:
                    known_face_encodings.append(current_face_encoding)
                    speaker_database.setdefault(sec, []) # if key doesn't exist, add. else nothing happens
                    speaker_database[sec].append(f'speaker_{len(known_face_encodings)}')

            # print the proc
            if not sec % (np.ceil((video.duration // interval) / 10) * interval): # total 10 proc outputs
                print(f"   by sec {sec}: completed!")

        print("✅ speaker database built!")
        return speaker_database

    def transcribe_or_translate_segments(self, audio_data, audio_sr: int):
        """Generate transcription with language detection"""

        print('Transcribing detecting and translating...'.center(60, '='))
        # use whisper model to segment the audio based on sentences
        transcribe_result = self.whisper_model.transcribe(audio_data, language = None, # auto detect lang
                                                          task = 'transcribe', # transcribe
                                                          verbose = None, # no proc details
                                                          word_timestamps = False # no word by word details
                                                          )
        print("✅ transcription done!")

        processed_transcribe_res = []
        if self.btranslate:
            # perform segment-wise language detection

            print(f"📝 Starting language detection...")
            for segment in transcribe_result["segments"]:
                start_sample = int(segment["start"] * audio_sr)
                end_sample = int(segment["end"] * audio_sr)
                segment_audio = audio_data[start_sample:end_sample]

                # Pad or trim to fit model input requirements for language detection
                segment_audio = pad_or_trim(segment_audio)
                mel = whisper.log_mel_spectrogram(segment_audio).to(self.device)
                _, probs = self.whisper_model.detect_language(mel)
                language_code = max(probs, key = probs.get)
                processed_transcribe_res.append({
                    'index':segment['id'],
                    'start':segment['start'],
                    'end':segment['end'],
                    'lang':language_code,
                    'text':segment['text']
                })
            
            print("✅ language detection done! Performing translation...")
            translated_res = []
            for segment in processed_transcribe_res:
                translated_res.append(segment)
                # then add a translated segment after every non-english segment
                if not segment['lang'] == 'en':
                    translator_name = segment['lang'] + '2en'
                    if translator_name not in self.translators.keys(): # don't have corresponding translator
                        translated_res.append({
                            'index':segment['index'],
                            'start':segment['start'],
                            'end':segment['end'],
                            'lang':segment['lang'],
                            'text':'[Translated][Translator for this language is unavailable]'
                        })
                    else: # translate!
                        translated_sentence = self.translators[translator_name](segment['text'])[0]['translation_text']
                        translated_res.append({
                            'index':segment['index'],
                            'start':segment['start'],
                            'end':segment['end'],
                            'lang':segment['lang'],
                            'text':f' [Translated]{translated_sentence}'
                        })
            processed_transcribe_res = translated_res
            print("✅ translation done!")

        else: # don't need translation, don't need language detection
            for segment in transcribe_result["segments"]:
                processed_transcribe_res.append({
                    'index':segment['id'],
                    'start':segment['start'],
                    'end':segment['end'],
                    'lang':'not detected',
                    'text':segment['text']
                })

        return processed_transcribe_res

    def align_speakers_and_speech(self, transcription: list[dict], speaker_timeline: dict):
        """Match speech segments with identified speakers"""

        print('Aligning speakers and speech...'.center(60, '='))
        MAX_SPEAKER_COUNT = 100
        transcription_speaker_detected = []

        # the underlying principle of speaker alignment:
        # who speaks has most scenes
        for sentence in transcription:
            # this table: index: speaker number; value: times detected in a speech
            table = np.zeros(MAX_SPEAKER_COUNT + 1, dtype = int)
            start_sec = sentence['start']
            end_sec = sentence['end']
            timeline_for_sentence = {sec:speakers for sec, speakers in speaker_timeline.items() 
                                     if start_sec <= sec <= end_sec}
            for speakers in timeline_for_sentence.values():
                for speaker in speakers:
                    table[int(speaker[-1])] += 1
            speaker_number = np.argmax(table)
            transcription_speaker_detected.append(sentence | {'speaker':speaker_number}) # 0 for no one

        print("✅ alignment done!")
        return transcription_speaker_detected

    def format_output(self, aligned_data: list[dict], output_path: str):
        """Generate final formatted transcript"""

        with open(output_path, 'w', encoding = "utf-8") as file:
            file.write(f'Transcription'.center(60, '=') + '\n\n')
            for seg in aligned_data:
                speaker = '(No Face)' if seg['speaker'] == 0 else f'speaker_{seg['speaker']}'
                file.write(f'[{str(timedelta(seconds = round(seg['start'])))}]' + 
                           f'(lang: {seg['lang']}){speaker}: {seg['text']}\n')
            file.write('\n' + f'End of output'.center(60, '=') + '\n')
        
        print("\n✅ output to file!")

# main func
def audio_transcriber(input_file: str, output_file: str, btranslate = False):
    """Main entry point - implements required interface"""
    try:
        transcriber = VideoTranscriber(whisper_model_size = 'base', btranslate = btranslate) # medium for multilingual stability
        extraction = transcriber.extract_and_process_audio(input_file)
        transcribed_res = transcriber.transcribe_or_translate_segments(extraction['audio'], extraction['audio_sr'])
        # speaker_db is a dict: {sec:[speakers]}
        speaker_db = transcriber.build_speaker_database(extraction['video'], interval = 1)

        aligned_data = transcriber.align_speakers_and_speech(transcribed_res, speaker_db)
        transcriber.format_output(aligned_data, output_file)
        
        extraction['video'].close() # release resources

    except Exception as e:
        print(f"❌ Exception: {e}")
    # return transcriber.process_video(input_file, output_file)

if __name__ == "__main__":
    start_time = time.time() # timer
    input_file = 'video_interview_English.mp4'
    output_file = 'output.txt'
    btranslate = False
    audio_transcriber(input_file, output_file, btranslate = btranslate)
    end_time = time.time()
    print(f'time: {end_time - start_time}')
    