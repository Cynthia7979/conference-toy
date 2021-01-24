# Conference-Toy
Make video conference your toy!

## What?
This project aims to make a tool that can change your appearance on a video conference.

It will have the following features:
- [x] Capture video from a specified camera,
- [x] Add accessories onto video, and/or
    * Moving/resizing accessories are not done yet
- [ ] Make the video a still picture,
- [x] Implement a GUI that shows the resulting video, and
- [x] Configure a webcam and have DingTalk/Zoom/WeMeet connect to it

### Notices
1. Due to my platform limitation, this project will be available for **Windows Only**.
Feel free to fork this repository and implement support for other platforms ;)
2. Due to some unknown problems with `sys.exit()`, the program may not exit correctly when pressing `q` or `x`.
In this scenario, please kill the process manually.

## How?
I will be using **Python 3.7** and the following libraries:
* `opencv-python`
* [pyvirtualcam](https://github.com/letmaik/pyvirtualcam)
* `Tkinter` for file selection
* `pillow` for jpeg reading
* `numpy`

## Where (did resources come from)?
* **pigegon.png** [Google Search](https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Fpigeon-cliparts.html&psig=AOvVaw12HzEyabJbPaVXrRQSnXeL&ust=1611397156736000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCPjsitOor-4CFQAAAAAdAAAAABAD)
* **mopemope.jpg** Screenshot by myself
