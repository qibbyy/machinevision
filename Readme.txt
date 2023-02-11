1. In order to run the program, the prequisite library are needed to be installed before run any program. All the installation can be done by using command prompt terminal.
the library that are needed to be install:
- Python
- OpenCV
- Tkinter
- Pillow
- RPi.GPIO (only can be install in raspberrypi)

2. If choose to run with raspberry pi, please type in 'git clone https://github.com/qibbyy/machinevision.git' at terminal to easily install all the required file to run the programme.

3. Once all the libraries needed are installed, there are two choices of program that can be run which are main.py and without_RPi.py.

4. Make sure the connection are the same as inside the report if intended to run the main.py.

5. Both programme can be modify to run custom dataset, just need to change the xml file at the load cascade classifier section.

6. To create custom dataset, please open Readme.txt inside haar_training folder.

7. If there is no changes made to the programme, both programme can be run by typing 'python main.py' or 'python without_RPi.py' at command prompt terminal.

8. During the running of the programme, the programme will open a GUI that will display the video feed and allow to change two parameters via a slider.

9. Adjust the slider to increase the accuracy and consistency of detection.