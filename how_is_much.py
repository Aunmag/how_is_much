#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
from pickle import load, dump
from random import randrange
from math import sqrt
from PyQt4 import QtGui, QtCore

# Initialization of general values and configs:
lim_n = 100  # maximal task number
lim_inc = True  # auto increasing of the limit number
ans_t = 2000*len(str(int(lim_n)))  # basic time for the answering
ans_dec = False  # auto decreasing of the answer time
difficult = 0.05  # auto increasing speed of the answer time and the limit number (from 0.01 to 0.09)
step = 0  # will be increased with every new task
correct = True  # if the last answer is correct
answers_history = []  # answers history will be keeping here
tasks_history = []  # failed tasks will be keeping here for repetition
ask_heading = ""  # heading of ask will be containing here
ask_text = ""  # text of ask will be containing here

# Loading previous configs:
try:  # if the configs file exist
    saves = load(open("saves.p", "rb"))
    lim_n = saves["lim_n"]
    lim_inc = saves["lim_inc"]
    ans_t = saves["ans_t"]
    ans_dec = saves["ans_dec"]
except FileNotFoundError:  # if the configs file can't be found
    pass


class Window(QtGui.QWidget):

    led_time = 400
    led_timer_step = 0

    def __init__(self,):
        super(Window, self).__init__()

        # Main window:
        self.setFixedSize(330, 155)
        self.setWindowTitle("How Is Much")
        self.setWindowIcon(QtGui.QIcon("favicon.ico"))

        # Background:
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor("#eee"))
        self.setPalette(palette)

        # Window grid:
        grid = QtGui.QGridLayout()
        grid.setSpacing(6)
        grid.setMargin(6)

        # Window stylisation:
        try:
            with open("theme.css", "r") as theme:
                self.setStyleSheet(theme.read())
        except FileNotFoundError:
            pass

        # Heading of ask:
        self.lb_ask_heading = QtGui.QLabel("You can press \"Page Down\" key to clear answer form.", self)
        self.lb_ask_heading.setObjectName('lb_ask_heading')
        grid.addWidget(self.lb_ask_heading, 1, 1, 1, 4)

        # Text of ask:
        self.lb_ask_text = QtGui.QLabel("Welcome!", self)
        self.lb_ask_text.setObjectName('lb_ask_text')
        grid.addWidget(self.lb_ask_text, 2, 1, 1, 4)

        # Answer form:
        self.tb_answer = QtGui.QLineEdit(self)
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.tb_answer, checking)
        QtGui.QShortcut(QtGui.QKeySequence("Enter"), self.tb_answer, checking)
        QtGui.QShortcut(QtGui.QKeySequence("PgDown"), self.tb_answer, self.tb_answer.clear)
        self.tb_answer.setText("Press \"Return\" key to start.")
        self.tb_answer.setFixedHeight(35)
        self.tb_answer.setObjectName('tb_answer')
        self.tb_answer.setFocus()  # automatic setting of the cursor in the answer form
        grid.addWidget(self.tb_answer, 3, 1, 2, 4)

        # Timer:
        self.pb_timer = QtGui.QProgressBar(self)
        self.pb_timer.setTextVisible(False)
        self.pb_timer.setFixedHeight(5)
        self.pb_timer.setValue(100)
        self.pb_timer_value = 0  # temporary value for initialization of variable
        self.pb_timer_state = 0  # timer activation
        self.pb_timer_state_old = self.pb_timer_state  # backup of timer state
        grid.addWidget(self.pb_timer, 4, 1, 1, 4)

        # Limit number configs:
        self.lb_lim_n = QtGui.QLabel("Limit number", self)
        grid.addWidget(self.lb_lim_n, 5, 1)
        self.le_lim_n = QtGui.QLineEdit(self)
        self.le_lim_n.setText(str(int(lim_n)))
        self.le_lim_n.textChanged.connect(self.le_ans_t_upd)
        grid.addWidget(self.le_lim_n, 5, 2)
        self.cb_lim_inc = QtGui.QCheckBox("Auto increasing", self)
        self.cb_lim_inc.toggle() if lim_inc else None
        self.cb_lim_inc.stateChanged.connect(lim_inc_switch)
        grid.addWidget(self.cb_lim_inc, 5, 3)

        # Answer time configs:
        self.lb_lim_n = QtGui.QLabel("Answer time", self)
        grid.addWidget(self.lb_lim_n, 6, 1)
        self.le_ans_t = QtGui.QLineEdit(self)
        self.le_ans_t.setText(str(ans_t))
        grid.addWidget(self.le_ans_t, 6, 2)
        self.cb_ans_dec = QtGui.QCheckBox("Auto decreasing", self)
        self.cb_ans_dec.toggle() if ans_dec else None
        self.cb_ans_dec.stateChanged.connect(ans_dec_switch)
        grid.addWidget(self.cb_ans_dec, 6, 3)

        # Pause button:
        self.btn_pause = QtGui.QPushButton("Pause (Esc)", self)
        self.btn_pause.setFixedWidth(90)
        self.btn_pause.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_pause.setShortcut("Escape")
        self.btn_pause.setCheckable(True)
        self.btn_pause.setEnabled(False)
        grid.addWidget(self.btn_pause, 5, 4, 2, 1)

        # Other:
        self.setLayout(grid)

    def le_ans_t_upd(self):
        if step == 0:
            self.le_ans_t.setText(str(2000*len(self.le_lim_n.text())))

    def timer_upd(self):
        """Regular updating of the timer."""
        # If the timer is working:
        if self.pb_timer_value > 0 and self.pb_timer_state == 2:
            self.pb_timer_value -= 1  # decreasing of current value
            self.pb_timer.setValue(self.pb_timer_value)  # setting of current value
            QtCore.QTimer().singleShot(1, lambda: self.timer_upd())  # recalling itself
        elif self.pb_timer_value <= 0 and self.pb_timer_state == 2:
            self.pb_timer_state = 1
            checking()
            QtCore.QTimer().singleShot(1, lambda: self.timer_upd())  # recalling itself
        elif self.pb_timer_value <= ans_t and self.pb_timer_state == 1:
            self.pb_timer_value += self.led_timer_step
            self.pb_timer.setValue(self.pb_timer_value)  # setting of current value
            QtCore.QTimer().singleShot(1, lambda: self.timer_upd())  # recalling itself
        elif self.pb_timer_value > ans_t and self.pb_timer_state == 1:
            self.pb_timer_state = 0
            task_generation()

    def pause(self):
        """Game pause"""
        if self.btn_pause.isChecked():  # pause activation
            # General:
            self.pb_timer_state_old = self.pb_timer_state
            self.pb_timer_state = 0  # timer deactivation
            self.tb_answer.setDisabled(1)  # answer form blocking
            # Task hiding:
            self.lb_ask_text.setText("Pause")
        else:  # pause deactivation
            # Timer updating:
            self.pb_timer_state = self.pb_timer_state_old  # timer activation (2)
            self.timer_upd()  # timer launching
            # Task showing:
            self.lb_ask_text.setText(ask_text)
            # Answer form updating:
            self.tb_answer.setDisabled(0)  # answer form unblocking
            self.tb_answer.setFocus()  # automatic setting of the cursor in the answer form

    def upd_general(self):
        """General updating GUI elements."""
        # Configs form information updating:
        self.le_ans_t.setText(str(ans_t))
        self.le_lim_n.setText(str(int(lim_n)))
        # Timer updating:
        self.pb_timer.setRange(0, ans_t)  # range
        self.pb_timer_value = ans_t  # start value
        # Answer form updating:
        self.tb_answer.clear()  # answer form cleaning
        self.tb_answer.setDisabled(0)  # answer form unblocking
        self.tb_answer.setFocus()  # automatic setting of the cursor in the answer form
        # Other:
        self.lb_ask_heading.setText(ask_heading)  # ask heading updating
        self.lb_ask_text.setText(ask_text)  # ask text updating

    def upd_after_answer(self):
        """GUI updating after answering."""
        self.led_timer_step = (ans_t - self.pb_timer_value)/self.led_time
        self.pb_timer_state = 1
        self.tb_answer.setDisabled(1)  # answer form blocking
        self.lb_ask_text.setText("<font color=#%s>%s</font>" % ("009b9b" if correct else "ff0000", ask_text))


def lim_inc_switch(state):
    if step == 0:
        global lim_inc
        lim_inc = True if state == QtCore.Qt.Checked else False


def ans_dec_switch(state):
    if step == 0:
        global ans_dec
        ans_dec = True if state == QtCore.Qt.Checked else False


def start():

    # GUI configs form blocking:
    gui.le_lim_n.setDisabled(1)
    gui.le_ans_t.setDisabled(1)

    # GUI switches style update:
    style_on = ".QCheckBox:indicator {background: #bbb;}"
    style_off = ".QCheckBox:indicator {background: #ddd;}"
    gui.cb_lim_inc.setStyleSheet(style_on if lim_inc else style_off)
    gui.cb_ans_dec.setStyleSheet(style_on if ans_dec else style_off)

    # Limit number correcting:
    if gui.le_lim_n.text().isdigit():
        global lim_n
        if int(gui.le_lim_n.text()) < 2:
            lim_n = 2
        elif int(gui.le_lim_n.text()) > 1000000:
            lim_n = 1000000
        else:
            lim_n = int(gui.le_lim_n.text())

    # Answer time correcting:
    if gui.le_ans_t.text().isdigit():
        global ans_t
        if int(gui.le_ans_t.text()) < 1000:
            ans_t = 1000
        elif int(gui.le_ans_t.text()) > 600000:
            ans_t = 600000
        else:
            ans_t = int(gui.le_ans_t.text())

    # Configs saving:
    dump({"lim_n": lim_n, "lim_inc": lim_inc, "ans_t": ans_t, "ans_dec": ans_dec}, open("saves.p", "wb"))

    # GUI pause button unblocking:
    gui.btn_pause.setEnabled(True)

    # Game beginning:
    task_generation()


def task_generation():

    global step, mode, x, y, z

    step += 1

    if randrange(4) == 0 and tasks_history:
        # Repetition of a failed task:
        failed_task = randrange(len(tasks_history))  # choosing a failed task
        mode = tasks_history[failed_task][0]  # lading of the mode from the chosen failed task
        x = tasks_history[failed_task][1]  # lading of x from the chosen failed task
        y = tasks_history[failed_task][2]  # lading of y from the chosen failed task
        del tasks_history[failed_task]  # removing the chosen failed task
    else:
        # Mode generation (memorization, addition, subtraction, multiplication, division):
        min_mod = 0 if step > 1 else 1
        max_mod = 4
        mode = randrange(min_mod, max_mod + 1)
        # Numbers generation:
        if mode == 0:
            z = randrange(len(answers_history))
        elif mode == 1 or mode == 2:
            x = randrange(int(lim_n*0.1), int(lim_n) + 1)
            y = randrange(int(lim_n*0.1), int(lim_n) + 1)
        else:
            x = randrange(1, int(sqrt(lim_n)) + 1)
            y = randrange(1, int(sqrt(lim_n)) + 1)

    # Ask creating:
    global task, ask_heading, ask_text
    ask_heading = "How is much?"
    if mode == 0:
        task = answers_history[z]
        ask_heading = "What was right answer?"
        ask_text = ("%s step before?" % (z + 1)) if z == 0 else ("%s steps before?" % (z + 1))
    elif mode == 1:
        task = x + y
        ask_text = ("%s+%s" % (x, y))
    elif mode == 2:
        task = x - y
        ask_text = ("%s-%s" % (x, y))
    elif mode == 3:
        task = x * y
        ask_text = ("%s*%s" % (x, y))
    elif mode == 4:
        task = int((x*y) / y)
        ask_text = ("%s/%s" % (x*y, y))

    # Answers history updating:
    answers_history.insert(0, task)  # adding of the new task answer
    if len(answers_history) > len(str(int(lim_n))):
        answers_history.pop()  # clearing of old task answers

    # For the GUI:
    gui.upd_general()  # GUI updating
    gui.pb_timer_state = 2  # timer activation
    gui.timer_upd()  # calling updating of the timer


def checking():

    # If game is starting:
    if step == 0:
        start()
        return

    # Answer checking:
    global correct
    correct = True if str(task) == gui.tb_answer.text() else False

    # Limit number increasing:
    if lim_inc:
        global lim_n
        formula = round(lim_n*difficult, 1)
        lim_n += formula if correct else (formula/2)*(-1)

    # Answering time decreasing:
    if ans_dec:
        global ans_t
        formula = ans_t*(difficult*0.1)
        ans_t += int(formula*(-1) if correct else formula/2)

    # Adding task for repetition:
    if mode != 0 and not correct:
        tasks_history.append((mode, x, y))

    # Ending of checking:
    gui.upd_after_answer()

# GUI creating:
app = QtGui.QApplication(argv)
gui = Window()
gui.show()
exit(app.exec_())
