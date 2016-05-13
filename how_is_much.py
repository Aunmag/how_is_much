#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
from random import randrange
from PyQt4 import QtGui, QtCore

# Configs:
target = 100  # necessary quantity of correct answers for the next level
basic_answer_time = 4000  # basic time for the answering
difficult = 0.66  # game difficult from 0.1 to 0.9 affect changing of time by answers

# Initialization general values:
step = 1  # it will increase with every player answer
trues = 0  # it will increase with every correct answer of player
mistakes = 0  # it will increase with every wrong answer of player
answers_history = []  # answers history will be keeping here


class Window(QtGui.QMainWindow):

    # General window configs:
    win_width = 300
    win_height = 170
    led_time = 500

    def __init__(self,):
        super(Window, self).__init__()
        # Main window:
        self.setFixedSize(self.win_width, self.win_height)
        self.setWindowTitle("Mathematics Trainer")
        self.setWindowIcon(QtGui.QIcon("favicon.ico"))
        # Label - about game:
        self.lb_about = QtGui.QLabel("<center>Mathematics Trainer v0.5 alpha by Aunmag</center>", self)
        self.lb_about.setGeometry(0, self.win_height - 160, self.win_width, 20)
        # Progress Bar - timer indicator:
        self.pb_time_indict = QtGui.QProgressBar(self)
        self.pb_time_indict.setTextVisible(False)
        self.pb_time_indict.setGeometry(0, self.win_height - 130, self.win_width, 20)
        self.pb_time_indict_value = 0  # temporary value for initialization of variable
        self.pb_time_indict_state = True  # activation of the timer indicator
        # Label - heading of ask:
        self.lb_ask_heading = QtGui.QLabel(str(ask_heading), self)
        self.lb_ask_heading.setGeometry(0, self.win_height - 110, self.win_width, 40)
        # Label - text of ask:
        self.lb_ask_text = QtGui.QLabel(ask_text, self)
        self.lb_ask_text.setGeometry(0, self.win_height - 80, self.win_width, 40)
        # Line Edit - answer form:
        self.tb_answer = QtGui.QLineEdit(self)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.tb_answer, checking)  # adding of hot key
        self.tb_answer.setGeometry(0, self.win_height - 30, self.win_width, 30)
        self.tb_answer.setAlignment(QtCore.Qt.AlignCenter)
        # Other:
        self.show()
        self.answer_timer = None  # it will be timer for the answering later

    def pb_time_indict_upd(self):
        """Regular updating of progress bar of the timer indicator."""
        # If the timer indicator is working:
        if self.pb_time_indict_value > 0 and self.pb_time_indict_state:
            self.pb_time_indict_value -= 1  # decreasing of current value
            self.pb_time_indict.setValue(self.pb_time_indict_value)  # setting of current value
            QtCore.QTimer().singleShot(1, lambda: self.pb_time_indict_upd())  # recalling itself

    def answer_start(self):
        """Launching of the timer and the timer indicator."""
        # Timer indicator launching:
        self.pb_time_indict_state = True  # activation of timer indicator
        self.pb_time_indict_upd()  # calling updating of timer indicator
        # If the timer already working:
        if self.answer_timer:
            self.answer_timer.stop()
        # Timer launching:
        self.answer_timer = QtCore.QTimer()
        self.answer_timer.timeout.connect(checking)  # wrong if time is up
        self.answer_timer.setSingleShot(True)  # ???
        self.answer_timer.start(answer_time)  # starting and setting time for the answering

    def upd_general(self):
        """General updating GUI elements."""
        # Updating of the time indicator:
        self.pb_time_indict.setRange(0, answer_time)  # range
        self.pb_time_indict_value = answer_time  # start value
        # Answer form updating:
        self.tb_answer.clear()  # answer form cleaning
        self.tb_answer.setDisabled(0)  # answer form unblocking
        self.tb_answer.setFocus()  # automatic setting of the cursor in the answer form
        # Ask heading updating:
        self.lb_ask_heading.setText(ask_heading)
        # Ask text updating:
        self.lb_ask_text.setText(ask_text)

    def upd_after_answer(self):
        """GUI updating after answering."""
        self.answer_timer.stop()  # stopping of the answering timer
        self.pb_time_indict_state = False  # deactivation of timer indicator
        self.tb_answer.setDisabled(1)  # answer form blocking

    def upd_correct(self):
        """Temporary changing color of the ask text if answer is correct."""
        self.lb_ask_text.setText("<font size=8 color=green><b><center>" + ask_text + "</center></b></font>")
        QtCore.QTimer().singleShot(self.led_time, lambda: task_generation())  # waiting before to continue

    def upd_wrong(self):
        """Temporary changing color of the ask text if answer is wrong."""
        self.lb_ask_text.setText("<font size=8 color=red><b><center>True is " + str(task) + "!</center></b></font>")
        QtCore.QTimer().singleShot(self.led_time*2, lambda: task_generation())  # waiting before to continue


# Temporary for the start:
start_ask_text = "<center>To start type LVL number (1 to 7) and press \"Return\" key.</center>"
ask_heading = ""
ask_text = start_ask_text


def task_generation():

    global trues
    global mistakes
    global answer_time

    # Time for the answering:
    answer_time = (basic_answer_time - ((trues - mistakes)/target)*basic_answer_time*difficult)*lvl

    # Mode generation (0 - memorization, 1 - addition, 2 - subtraction, 3 - multiplication, 4 - division):
    min_mod = 1
    if step > 1:
        min_mod = 0
    max_mod = 4
    if lvl < 3:
        max_mod = 2
    mode = randrange(min_mod, max_mod + 1)

    # Numbers generation:
    max_num = 10 ** lvl
    global x
    global y
    x = randrange(1, max_num)
    y = randrange(1, max_num)

    # Converting numbers for multiplication and division modes by levels:
    if mode > 2:
        if lvl < 5:
            x //= 10 ** (lvl - 1)
            if x == 0:
                x = randrange(1, 10)
        elif lvl >= 5:
            x //= 10 ** (lvl - 2)
            if x == 0:
                x = randrange(10, 100)
        if lvl < 7:
            y //= 10 ** (lvl - 1)
            if y == 0:
                y = randrange(1, 10)
        elif lvl == 7:
            y //= 10 ** (lvl - 2)
            if y == 0:
                y = randrange(10, 100)

    # Asks:
    global task
    global ask_heading
    global ask_text
    global answers_history
    ask_heading = "How is much?"
    if mode == 0:
        z = randrange(len(answers_history))
        task = answers_history[z]
        ask_heading = "What was right answer?"
        if z == 0:
            ask_text = (str(z+1) + " step before?")
        else:
            ask_text = (str(z+1) + " steps before?")
    elif mode == 1:
        task = x + y
        ask_text = (str(x) + "+" + str(y))
    elif mode == 2:
        task = x - y
        ask_text = (str(x) + "-" + str(y))
    elif mode == 3:
        task = x * y
        ask_text = (str(x) + "*" + str(y))
    elif mode == 4:
        task = (x*y) / y
        ask_text = (str(x*y) + "/" + str(y))
    ask_heading = ("<center>" + ask_heading + "</center>")
    ask_text = ("<font size=8><b><center>" + ask_text + "</center></b></font>")

    # Updating history of answers:
    answers_history.insert(0, task)
    # Removing unnecessary answers from history:
    if len(answers_history) > lvl:
        answers_history.pop()

    gui.upd_general()
    gui.answer_start()


def checking():

    global trues
    global mistakes

    # If game is starting:
    global lvl
    if ask_text == start_ask_text:
        lvl = int(gui.tb_answer.text())
        if lvl < 1:
            lvl = 1
        elif lvl > 7:
            lvl = 7
        task_generation()
        return
    # If answer is empty:
    elif gui.tb_answer.text() == "" or gui.tb_answer.text() == "-":
        mistakes += 1
        gui.upd_after_answer()
        gui.upd_wrong()
    # If answer is correct:
    elif task == int(gui.tb_answer.text()):
        trues += 1
        gui.upd_after_answer()
        gui.upd_correct()
    # If answer is wrong:
    else:
        mistakes += 1
        gui.upd_after_answer()
        gui.upd_wrong()

    global answers_history
    global step
    step += 1

    # Level control:
    if trues - mistakes == target and lvl < 7:
        lvl += 1
        trues = 0
        mistakes = 0
        step = 1
        answers_history = []
    elif trues - mistakes <= -3 and lvl > 1:
        lvl -= 1
        trues = 0
        mistakes = 0
        step = 1
        answers_history = []

# GUI creating:
app = QtGui.QApplication(argv)
gui = Window()
gui.show()
exit(app.exec_())
