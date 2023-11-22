# EMedia
- Is a simple media player with separated controls and video screen. Can play/show video, audio and image files
- Testing: Added webview to play YouTube videos
- Testing: Display PDF

### Rquirements:
- PySide6
- opencv-python
- QtAwesome
- requests
- pytube

### Install requirements:
```
pip install PySide6 opencv-python QtAwesome requests pytube
```

Also you need ffprobe, put it in the program folder
[https://ffbinaries.com/downloads](https://ffbinaries.com/downloads)


### BUGS:
- Changing media while still playing hang application when playing video for the first time after program start.
- - Solution: Play video and press stop, after that no freezes and hangs noticed