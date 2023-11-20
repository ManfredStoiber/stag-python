# Python Wrapper for [STag - A Stable, Occlusion-Resistant Fiducial Marker System](https://github.com/ManfredStoiber/stag)

## 📊 Comparison Between Different Marker Systems:
[<img src="https://github.com/ManfredStoiber/stag/assets/47210077/668ca457-33dd-4ce7-8b94-662c7a5bb4d9" width="400" height="200" />](https://www.youtube.com/watch?v=vnHI3GzLVrY)

## 📋 Getting Started
0. Install Prerequisites
    - [CMake >= 3.16](https://cmake.org/getting-started/)
        - On Linux: `apt install cmake`
    - [OpenCV 4](https://opencv.org/get-started/) for C++
        - On Linux: `apt install libopencv-dev`
    - [Eigen 3](https://gitlab.com/libeigen/eigen)
        - On Linux: `apt install libeigen3-dev`
    - Run `pip install numpy`
        - On Linux: if during step 2.2 the error "numpy/ndarrayobject.h: No such file or directory" occurs, try one of following solutions:
            - Run `apt install python-numpy` or
            - Search for "ndarrayobject.h" (`find / -name ndarrayobject.h`) and create a symlink from its parent directory to "/usr/include/numpy" (e.g. `ln -s /usr/local/lib/python3.8/dist-packages/numpy/core/include/numpy /usr/include/numpy`)
    - Run `pip install opencv-python`
1. Clone this repository recursively: `git clone --recursive https://github.com/ManfredStoiber/stag-python`
2. Build
    1. cd into project: `cd stag-python`
    2. `pip install .`
3. Run test app
    1. `cd example`
    2. `python example.py`

## 📖 Usage

For an example how to use this library, refer to [example.py](https://github.com/ManfredStoiber/stag-python/blob/master/example/example.py)

## 🏷 Markers

- Collection of markers: [Drive](https://drive.google.com/drive/folders/0ByNTNYCAhWbIV1RqdU9vRnd2Vnc?resourcekey=0-9ipvecbezW8EWUva5GBQTQ&usp=sharing)
- Marker Generator: see [ref/marker generator](https://github.com/ManfredStoiber/stag/tree/master/ref/marker%20generator) for reference code for marker generation

## 📔 Known Issues
- Sometimes markers are detected multiple times
    - Workaround: only use one of the detections

## 📰 Originally Published in the Following Paper:

[B. Benligiray; C. Topal; C. Akinlar, "STag: A Stable Fiducial Marker System," Image and Vision Computing, 2019.](https://arxiv.org/abs/1707.06292)

Some figures from the paper:

<p align="center">
  <img src="https://user-images.githubusercontent.com/19530665/57179654-c0c11e00-6e88-11e9-9ca5-0c0153b28c91.png"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/19530665/57179660-cae31c80-6e88-11e9-8f80-bf8e24e59957.png"/>
</p>

