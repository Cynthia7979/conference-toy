# Tutorial: Help! How to Stop It From Crashing???

This project is developed in three days. Due to this, it is pretty flawed
and may crash frequently due to a lot of reasons. 

Follow the following steps to run the program "correctly":
1. **Have [OBS](https://obsproject.com/download) and [obs-virtual-cam](https://github.com/CatxFish/obs-virtual-cam/releases)
installed!** This project is partially based on them.
2. **Run `main.py`** and see if the camera works correctly.
3. **With `main.py` running, open a web meeting to test the webcam.**
To do this, choose `OBS-Camera` as your camera in the meeting app.
4. If everything's set, feel free to add some accessories (stickers) by clicking the button. 
If the program crashes, check if you:
    * Used images that're **larger** your camera dimensions. The matrix operation cannot do that, and my 
solution has some bugs.
5. Also, **close your camera in the meeting** when starting/restarting the program to prevent conflict. You may open it afterwards.

If you met any problems that're not listed here, please [create an Issue](https://github.com/Cynthia7979/conference-toy/issues/new/choose)