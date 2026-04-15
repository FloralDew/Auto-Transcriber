# Audio Transcriber README

By FloralDew 8/8/2025

---

**(FILES INTRODUCTION)** In this folder, [audio_transcriber.py](audio_transcriber.py) is the main python implementation. [requirements.txt](requirements.txt) contains all possible python packages you need to run the code. mp4 files are three sample videos.

**For more information about the program, please refer to [REPORT](Report for Transcription Program.md)**

**For more information about the samples, please refer to [TEST CASE AND OUTPUT](Test Case and Sample output.md)**



## Setup Instructions

This Python program is based on **Python 3.13.3** with packages mentioned [here](requirements.txt) 

**(some could be unnecessary, but I listed all in case of any error)**

Among them, most packages can be directly downloaded using `pip install`, but the **face_recognition** package needs particular attention: [face_recognition Windows Installation Guide](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)

Put it simply, before running `pip install face_recognition`, you need to have **Visual Studio with C/C++ complier** installed.

You can find the github repository and more specific instructions of face_recognition package [here](https://github.com/ageitgey/face_recognition/)

>  For more information why I use this package, please refer to the [report](Report for Transcription Program.md)



## Usage Guide

To play with the code, you only need to change these params inside syntax `if __name__ == "__main__"` at line 281:

- `input_file`. Specify the input video path (or filename, if audio_transcriber.py is in the same directory).

- `output_file`. Specify the output file where transcription will be written.
- `btranslate`. Specify whether you need the transcription translated.

Other params you can play with:

- `whisper_model_size`. At line 264. Bigger for more precise but slower transcription.
- `interval`. At line 268. Specify the interval (in sec) of frame captured.



## How to Use CUDA if Available

First, install dlib with GPU support:

```bash
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 -G "Visual Studio 16 2019"
cmake --build .
cd ..
python setup.py install --set USE_AVX_INSTRUCTIONS=1 --set DLIB_USE_CUDA=1 -G "Visual Studio 16 2019"
```

Note that CUDA 12.1 cannot be compiled by Visual Studio 2022. Use 2019 instead.

You can probably encounter several problems during the installation.
- If you have use vs2022 to complie dlib, you need to run `python setup.py` first to clean up buffer before specifying vs2019.
- vs2019 needs cuda toolset to complie dlib, copy C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\extras\visual_studio_integration\MSBuildExtensions\\* to <vs dict>\MSBuild\Microsoft\VC\v160\BuildCustomizations\
- The directory structure of newer CUDNN has changed and prevent CMake from locating CUDNN. To solve this problem:
  - copy include\12.9\\* to include\
  - copy lib\12.9\x64\\* to lib\x64\
  - copy bin\12.9\\* to bin\
- If `fatal error C1060: compiler is out of heap space` occurs, run `set CL=/bigobj /Zm300` in cmd to increase heap space limit.