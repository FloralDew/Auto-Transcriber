[TOC]

# Test Case and Sample output

FloralDew

You can find the processing time at the end of each `terminal output` block.



## 1. Multiple speakers

### Test case introduction

- Video duration: 2min53s (**The 15-sec trimmed version** is available [here](video_interview_English_trimmed.mp4))
- number of speaker: 2 (IELTS interviewer and interviewee)
- language: 1 (English)

The video is an interview. 

The camara **doesn't always focus on the speaker**: sometimes on the listener, sometimes on their side faces. This brings the inevitability of speaker recognition error.

You can find the video [here](video_interview_English.mp4)

### Program settings

- Whisper model size: base (base is already enough for English speech recognition)
- btranslate = False (already in English. Don't need translation)
- interval: 1s
- device: cpu

### Terminal output

```
=====================Audio Transcriber======================
Using device: cpu
🔧 Setting up Whisper Model...
✅ Whisper Model loaded successfully
=============Extracting and processing audio...=============
✅ audio extraction done!
   number of audio channels: 2
✅ audio processing done!
=========Transcribing detecting and translating...==========
✅ transcription done!
===============Performing face recognition...===============
   by sec 0: completed!
   by sec 18: completed!
   by sec 36: completed!
   by sec 54: completed!
   by sec 72: completed!
   by sec 90: completed!
   by sec 108: completed!
   by sec 126: completed!
   by sec 144: completed!
   by sec 162: completed!
✅ speaker database built!
==============Aligning speakers and speech...===============
✅ alignment done!

✅ output to file!
time: 107.32856774330139
```

### output.txt

```
=======================Transcription========================

[0:00:00](lang: not detected)speaker_1:  Good afternoon. My name is Jonathan Lewis.
[0:00:04](lang: not detected)speaker_2:  Good afternoon.
[0:00:06](lang: not detected)speaker_2:  Can you tell me your full name please?
[0:00:07](lang: not detected)speaker_2:  Please, and I'll show them.
[0:00:09](lang: not detected)speaker_2:  Thank you. And what shall I call you?
[0:00:11](lang: not detected)(No Face):  Please call me an I-O.
[0:00:12](lang: not detected)speaker_1:  Where are you from?
[0:00:14](lang: not detected)speaker_2:  I'm from India. Actually I come from Delhi.
[0:00:17](lang: not detected)speaker_1:  In this first part of the test, I'm going to ask you some questions about yourself.
[0:00:22](lang: not detected)speaker_1:  Do you work or are you a student?
[0:00:24](lang: not detected)speaker_2:  No, I'm not working at the moment. I'm just studying.
[0:00:27](lang: not detected)speaker_2:  What are you studying?
[0:00:30](lang: not detected)speaker_1:  I'm doing bachelor's in media and communication studies.
[0:00:33](lang: not detected)speaker_1:  Why did you choose that course?
[0:00:38](lang: not detected)speaker_2:  Mainly because I think the scores are a variety of diverse options to choose from.
[0:00:47](lang: not detected)speaker_2:  It could be a filmmaker or an actor or a journalist.
[0:00:51](lang: not detected)speaker_2:  And also because I think this course offers you a chance to use your creative skills.
[0:01:00](lang: not detected)speaker_2:  Let's talk about weather.
[0:01:03](lang: not detected)speaker_1:  Is some of your favourite time of year?
[0:01:06](lang: not detected)speaker_1:  Why or why not?
[0:01:08](lang: not detected)(No Face):  No, it's not. Absolutely not.
[0:01:10](lang: not detected)speaker_2:  Why not?
[0:01:12](lang: not detected)speaker_2:  I think because in my country it's mostly summerish for like,
[0:01:20](lang: not detected)speaker_2:  six months in a year.
[0:01:22](lang: not detected)speaker_2:  And they're even hotter now because of the whole climate change situation.
[0:01:26](lang: not detected)speaker_2:  And it's just very sweaty, your hair gets frizzy,
[0:01:29](lang: not detected)(No Face):  your makeup keeps melting.
[0:01:31](lang: not detected)(No Face):  So it's horrible in my country in summers.
[0:01:34](lang: not detected)speaker_1:  I see. So what do you do in summer when the weather's very hot and why?
[0:01:39](lang: not detected)speaker_1:  I get annoyed and grunky.
[0:01:41](lang: not detected)speaker_2:  Other than that, I try to stay home.
[0:01:46](lang: not detected)speaker_2:  Or I try to drink plenty of water so I don't get dehydrated.
[0:01:52](lang: not detected)speaker_2:  And I also have to use a lot of insect repellent at night because the mosquitoes won't let you sleep.
[0:02:00](lang: not detected)speaker_2:  So would you like travelling during summer?
[0:02:04](lang: not detected)(No Face):  No, not really to be honest.
[0:02:07](lang: not detected)speaker_2:  I hate going out in summers.
[0:02:09](lang: not detected)speaker_2:  It's miserable outside.
[0:02:12](lang: not detected)speaker_2:  I try to stay home mostly.
[0:02:15](lang: not detected)speaker_2:  Even if I go out with my friends, I make sure we go to a restaurant or someplace that's properly air conditioned.
[0:02:22](lang: not detected)speaker_2:  I say, did you enjoy the summer holidays when you were at school?
[0:02:26](lang: not detected)speaker_2:  Yeah, I did.
[0:02:30](lang: not detected)speaker_2:  Maybe because when I was a kid I did not care much about the hot weather as much as I do now.
[0:02:38](lang: not detected)speaker_2:  Or maybe because I did not have to attend my school.
[0:02:43](lang: not detected)speaker_1:  But it was when my parents would take me out on lunch or to a park anywhere.
[0:02:48](lang: not detected)speaker_2:  My cousins would come over.
[0:02:50](lang: not detected)speaker_2:  We would play different indoor outdoor games.

=======================End of output========================

```

### Remark

The reason why "**lang: not detected**" is that btranslate == False, so the program just directly transcribed the speech **without language detection and translation process**. Note that if there are still multiple languages other than English in speech when btranslate == False, the transcription will still be in the corresponding language if Whisper model works well.

Without language detection and translation process, and the whisper model size being base, the processing time decreased significantly. Also, since the speech is all in English, even base model has a decent performance.



## 2. Multilingual

### Test case introduction

- Video duration: 15s
- number of speaker: 1 (myself)
- language: 3 (English, Japanese, Chinese)

The audio of  the video is comprised of three clear-spoken sentences in three different languages. 

The speaker always appears in the frame.

The video isn't available for now.

### Program settings

- **Whisper model size: medium** (medium for multilingual stability. Otherwise the output might err)
- **btranslate = True** (see README.md for details of this argument)
- interval: 1s
- device: cpu

### Terminal output

```
=====================Audio Transcriber======================
Using device: cpu
🔧 Setting up Whisper Model...
✅ Whisper Model loaded successfully
🔧 Setting up NLLB Translation Models...
✅ NLLB Model loaded successfully

🌍 Creating translation pipelines...
Device set to use cpu
   ✅ ja2en
Device set to use cpu
   ✅ zh2en
=============Extracting and processing audio...=============
✅ audio extraction done!
   number of audio channels: 2
✅ audio processing done!
=========Transcribing detecting and translating...==========
✅ transcription done!
📝 Starting language detection...
✅ language detection done! Performing translation...
✅ translation done!
===============Performing face recognition...===============
   by sec 0: completed!
   by sec 2: completed!
   by sec 4: completed!
   by sec 6: completed!
   by sec 8: completed!
   by sec 10: completed!
   by sec 12: completed!
   by sec 14: completed!
✅ speaker database built!
==============Aligning speakers and speech...===============
✅ alignment done!

✅ output to file!
time: 70.57297897338867
```

### output.txt

```
=======================Transcription========================

[0:00:00](lang: en)speaker_1:  The weather in Canada is much cooler than that in China. I really like the climate here.
[0:00:07](lang: ja)speaker_1:  御野さん、こんにちは。部屋の下記を忘れないで下さい。
[0:00:07](lang: ja)speaker_1:  [Translated]Mr. Wano, hello. Don't forget the bottom of the room.
[0:00:12](lang: zh)speaker_1:  今天白天到夜間、武漢天氣很熱。
[0:00:12](lang: zh)speaker_1:  [Translated]Today, day and night, it's hot in Wuhan.

=======================End of output========================

```

### Remark

The medium model shows great capability dealing with multilingual speech. There's just one transcription error: 鍵 rather than 下記. But this is most probably due to my pronunciation. Overall, the output is not bad.

By the way, it takes 70 seconds to run the program, nearly five times the duration of original video, **because whisper size is larger and gpu is unavailable.**



