# ddr_arduino_controller

![Python-App workflow](https://github.com/kemcbride/ddr_arduino_controller/actions/workflows/python-app.yml/badge.svg)


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2>Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#background">Background</a></li>
    <li><a href="#reference">Reference</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a project intended for use with Arduino + a stripped down PlayStation Controller (and a PlayStation with a copy of some Dance Dance Revolution game), where you can press a button and have the Arduino run through the steps (and ideally play any* song perfectly**!).

_\*any: any song that you run the tooling on, that you build it to run, that doesn't have unsupported gimmicks/features_

_\*\*perfectly: theoretically perfectly... realistically, my playstation seems to have a bit of drift. Hence bpm offset options._


### Built With

* [Arduino](https://www.arduino.cc/)
* [Python](https://www.python.org/)
* [StepMania Files](https://www.stepmania.com/)
  * StepMania FILES, as of current date, mostly available via search dot stepmaniaonline dot net

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* python3.7+
* Arduino of some sort (+ the Arduino software)
* A Playstation and a DDR game you can run
* Some Playstation controller (The one I use is stripped from an old DDR pad for playstation)
* At least one button/switch you can attach to the Arduino


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/kemcbride/ddr_arduino_controller.git
   ```
2. Set up Python 3.7+ virtual environment (This project uses [dataclass](https://docs.python.org/3/library/dataclasses.html))
  ```sh
  python3.7 -m venv 
  ```
3. "Activate" the virtual environment
  ```sh
  source bin/activate
  ```
4. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage

1. `python __main__.py {path/to/your.sm}`
2. copy the output to wherever; The way I have it set up now: `arduino/ps1controller/hysteria.h`
3. The only way I know to set up the arduino is via the arduino IDE. Verify & Upload. [TODO] Set up arduino-cli options
4. Hook it all up, boot up the playstation and konamix,
5. press the MacroPin button on the first note of your chart!

## Testing

To run the tests under testing, I use this command (with the virtual env already activated, etc) from the repo root:
```sh
python -m testing
```

## Background
[TODO] Add some explanation of what it is and does here. And why.

## Reference

After trying to debug what I was doing wrong on May ~22 2021, I made this [circuit diagram](https://crcit.net/c/b473b849964645f9a8e5d0a5cde722ab) online. Beware, it probably isn't very useful. Also it's not entirely accurate, it has different pins in use on the Arduino.

![Circuit.png Diagram from Imgur](https://i.imgur.com/XyPsRPC.png)
![A picture of my circuit from Imgur](https://i.imgur.com/y0jQQtO.jpg)



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
