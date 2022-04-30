import threading
import time

import SpeechAsr

from PyQt5 import QtWidgets, QtGui, QtCore, uic

from asrInterface import Ui_MainWindow
import sys

import speech_recognition as sr
import difflib
import os

r = sr.Recognizer()


def open_pictures_similarity(input_command):

    if difflib.SequenceMatcher(None, input_command, "show pictures").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "should pictures").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "shouldn't pictures").quick_ratio() > 0.7:
        return True
    else:
        return False


def open_notepad_similarity(input_command):

    if difflib.SequenceMatcher(None, input_command, "open notepad").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "and not and").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "open not pond").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "open not pot").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "and pond").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "and look").quick_ratio() > 0.7:
        return True
    else:
        return False


def play_music_similarity(input_command):
    if difflib.SequenceMatcher(None, input_command, "play music").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "peregrine music").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "play falcon").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "peregrine falcon").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "protein music").quick_ratio() > 0.7:
        return True
    elif difflib.SequenceMatcher(None, input_command, "protein think").quick_ratio() > 0.7:
        return True
    else:
        return False


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def speech_recognition_baiduApi(self):
        self.ui.label.setText('I am hearing...')
        with sr.Microphone(sample_rate=8000) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=59)

        with open("source/temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

        input_command = SpeechAsr.get_command()
        print(input_command)
        if "play music," in input_command:
            self.play_music()
        elif "open notepad," in input_command or "open note that," in input_command:
            self.open_notepad()
        elif "show pictures," in input_command or "show picture," in input_command:
            self.show_picture()
        else:
            self.ui.label.setText('sorry, I can\'t understand...')

        time.sleep(2)
        self.ui.label.setText('How can I help?')

    def play_music(self):
        self.ui.label.setText('play music')
        os.startfile(r"source\music.mp3")

    def open_notepad(self):
        self.ui.label.setText('open notpad')
        os.system(r"notepad.exe source\file.txt")

    def show_picture(self):
        self.ui.label.setText('show picture')
        os.startfile(r"source\picture.jpg")

    def speech_recognition(self):
        mic = sr.Microphone()

        with mic as source:
            r.adjust_for_ambient_noise(source)
            self.ui.label.setText('I am hearing...')
            try:
                audio = r.listen(source, timeout=5)
                input_command = r.recognize_sphinx(audio)
                print(input_command)
                if play_music_similarity(input_command):
                    self.play_music()
                elif open_notepad_similarity(input_command):
                    self.open_notepad()
                elif open_pictures_similarity(input_command):
                    self.show_picture()
                else:
                    self.ui.label.setText('sorry, I can\'t understand...')
            except Exception as e:
                print(e)
                self.ui.label.setText('sorry, I can\'t understand...')

            time.sleep(2)
            self.ui.label.setText('How can I help?')

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.ui.label.setText("How can I help?")
        # timer = threading.Timer(0.1, self.speech_recognition)
        # timer.start()
        timer = threading.Timer(1, self.speech_recognition_baiduApi)
        timer.start()


app = QtWidgets.QApplication([])
application = myWindow()
application.show()

sys.exit(app.exec())
