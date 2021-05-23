# ddr_arduino_controller
My little project essentially translating .sm files into commands to play DDR tracks, when hooked up to my playstation. Just some fun.

* ![Python-App workflow](https://github.com/kemcbride/ddr_arduino_controller/actions/workflows/python-app.yml/badge.svg)


## How to run (from my memory)
1. set up python 3.7+ virtual env (I use dataclass)
2. `source bin/activate`
3. `pip install -r requirements.txt`
4. `python __main__.py {path/to/your.sm}`
5. copy the output to wherever; i mean right now to `arduino/ps1controller/hysteria.sm`
6. The only way I know to set up the arduino is via the arduino IDE. Verify & Upload.
7. Hook it all up, boot up the playstation and konamix,
8. press the MacroPin button on the first note of your chart!

optionally: set up correct bpm offset, fix chart selection, etc.
There are lots of bugs etc. Good luck.


## Reference Images

After trying to debug what I was doing wrong on May ~22 2021, I made this circuit diagram online: https://crcit.net/c/b473b849964645f9a8e5d0a5cde722ab

![Circuit.png Diagram from Imgur](https://i.imgur.com/XyPsRPC.png)
![A picture of my circuit from Imgur](https://i.imgur.com/y0jQQtO.jpg)
