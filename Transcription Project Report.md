# Transcription Project: Report
8/7/2025 FloralDew



## High Level Overview (How it works)

The whole transcription procedure is comprised of the following steps (just as the function names indicate):

1. **Initialization**. First, set up the whisper model **(Base for English, but I recommend at least medium for multilingual stability)**.
   - If `btranslate` (a bool param indicating whether you want the output translated into English)` == True`, load the NLLB translation model. Now I only set 2 translators (Japanese to English & Chinese to English) as examples. **To add more, please add language pairs to the list `language_pairs` at code line 42 as illustrated**. 
     - Note **(robustness)**: The program won't stop running when encountering languages not in translators. It will just indicate ''[Translator for this language is unavailable]'' in the output file.
     - Note: Whisper itself is embedded with translation function, but it is not as robust and precise as NLLB.
   - If `btranslate == False`, there's no need to load NLLB
2. **Extract and process the audio**. Extract audio from video, and process it for best whisper function.
3. **Transcribe & translate**. Transcribe using whisper.
   - If `btranslate == True`, perform language detection for each segment of speech. Then performing translation with specific NLLB translators according to language detected.
   - if `btranslate == False`, return the direct transcription, language marked "not detected".
4. **Time-wise face recognition**. Capture the frame every `interval` seconds (default 1, can be changed at code line 268). Perform face recognition with face_recognition package. Return a dict `{time: [speakers]}`
   - Note **(robustness)**: If no one exist in frame, the program won't stop running. The output will be marked "no face". See example [here](Test Case and Sample output.md).
   - Note: The reason for which I use **face_recognition** instead of **facenet_pytorch** to build this program is that the latter is outmoded and requires lots of packages of older version (for instance, numpy 1.24.0) which are no longer supported and may cause serious compatibility issues. What's more, **face_recognition** is much more modern and has higher recognition accuracy.
5. **Align speakers and speech.** For each segment of processed whisper transcription output in step 3, determine the speaker recognized most times. And he or she is the most probable speaker.
6. **Output**. Literally. Output to txt file.



## Issues and Solutions

1. Even if a long speech consists of **multiple languages**, Whisper **only embeds the first** language detected in return value, making it difficult to use NLLB models (because you must specify the pipeline) for translation. This adds to the difficulties of multilingual implementation. To address the problem, I **call whisper twice**. In the first call, whisper is used to form the whole transcription. In the second call, whisper is used as a language detector for each speech segment to add a language code key to the segment.
2. Time-wise face recognition is the most **time-consuming** step in this program. To solve it, I use a **resize** function to decrease the frame size before performing face recognition. Meanwhile, to maintain the precision of face recognition, the frames are scaled differently according to their original size. See more in code line 110 and after.
3. Some basic **coding problems**. For example, how to use `moviepy` to capture video frames, how to use Whisper for language detection and so on. I asked AI for help and they were greatly helpful. However, the basic logic of this program is my original work.



## Evaluation

Here list my comments on the program.

### Pros:

1. The program is robust in a way (See more in aforementioned part "High level overview").
   - Successfully handle video with no face detected
   - Successfully handle multiple languages even some translators are unavailable
   - Successfully handle all-English speech but `btranslate == True`
   - Successfully handle some common problems, like typo in file path
2. Multilingual implementation. You only need to change the param `btranslate` at code line 280 to indicate whether translation is needed.
3. Acceptable processing time. Works well even when gpu is unavailable.

### Cons:

1. **(IMPORTANT)** The underlying principle of this transcription program limits the precision of speaker recognition. It uses face instead of voiceprint recognition to identify the speaker, which means if the camera isn't focused on the speaker, for example, most commonly, on the listener, discrepancy could easily occur. To solve the problem, a more SOTA voiceprint model is needed. For example, `pyannote-audio` package.

2. As indicated before, whisper was called twice. This can give rise to redundancy in processing time. Thus, a model for voice segmenting is needed.



## Instruction to Run Code

To play with the code, you only need to change these params inside syntax `if __name__ == "__main__"` at line 281:

- `input_file`. Specify the input video path (or filename, if audio_transcriber.py is in the same directory).

- `output_file`. Specify the output file where transcription will be written.
- `btranslate`. Specify whether you need the transcription translated.

Other params you can play with:

- `whisper_model_size`. At line 264. Bigger for more precise but slower transcription.
- `interval`. At line 268. Specify the interval (in sec) of frame captured.
