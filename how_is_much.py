#!/usr/bin/env python
# -*- coding: utf-8 -*-

# How Is Much v0.3 (pre-alpha) by Aunmag

from random import randrange

# Loading:
step = 1
trues = 0
mistakes = 0
target = 100
answers_history = []

# Welcome:
print("Hello it's the How Is Much v0.3 (pre-alpha) by Aunmag.\n"
      "Here you can improve your brain by means of arithmetical tasks." + "\n"
      "If you want to finish the game write 'end' in answer.\n")

# Level configs:
lvl = input("To start enter any level (1 to 7) here: ")
if lvl.lower() == "end":
    raise SystemExit(1)
elif not lvl.isdigit():
    lvl = 3
elif int(lvl) < 1:
    lvl = 1
elif int(lvl) > 7:
    lvl = 7
lvl = int(lvl)

print("\nLevel " + str(lvl) + ". Good luck, begin! =)\n")

while True:

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
    if mode == 0:
        if step < lvl:
            z = randrange(1, step + 1)
        else:
            z = randrange(1, lvl + 1)
        task = answers_history[z - 1]
        answer = input("What was right answer " + str(z) + " steps before? Write answer: ")
    elif mode == 1:
        task = x + y
        answer = input("How is much " + str(x) + "+" + str(y) + " ? Write answer: ")
    elif mode == 2:
        task = x - y
        answer = input("How is much " + str(x) + "-" + str(y) + " ? Write answer: ")
    elif mode == 3:
        task = x * y
        answer = input("How is much " + str(x) + "*" + str(y) + " ? Write answer: ")
    elif mode == 4:
        task = (x * y) / y
        answer = input("How is much " + str(x) + "/" + str(y) + " ? Write answer: ")

    # Updating history of answers:
    answers_history.insert(0, task)

    # Removing unnecessary answers from history:
    if len(answers_history) > lvl:
        answers_history.pop()

    # Checking of answer:
    if answer.lower() == "end":
        print("\nGame has ended. You got " + str(trues - mistakes) + " scores."
              "\nTrue answers: " + str(trues) +
              "\nFalse answers: " + str(mistakes))
        end = input("Enter 'end' again to exit: ")
        if end.lower() == "end":
            break
    elif int(answer) == task:
        trues += 1
        print("Right!\n")
    elif int(answer) != task:
        mistakes += 1
        print("Wrong!! Is " + str(task) + "!\n")
    if lvl < 7:
        print("Current " + str(lvl) + " level is completed by " + str(int((trues - mistakes)/target*100)) + "%!\n")

    step += 1

    # Level control:
    if trues - mistakes == target and lvl < 7:
        lvl += 1
        print("Hooray! You have " + str(target) + " scores "
              "(" + str(trues) + " true and " + str(mistakes) + " false answers). "
              "Welcome to " + str(lvl) + " level!\n")
        trues = 0
        mistakes = 0
        continue
    elif trues - mistakes <= -3 and lvl > 1:
        lvl -= 1
        print("You have enough mistakes to return back "
              "(" + str(trues) + " true and " + str(mistakes) + " false answers). "
              "Practice on " + str(lvl) + " level else.\n")
        trues = 0
        mistakes = 0
        continue
