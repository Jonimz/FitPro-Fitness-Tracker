######################################################################
# Author: Joyce Nimely
# Username: Nimely_J
#
# FinalProject: FitPro App
#
# Purpose: A python based fitness tracking application that allows user to log workouts,
# set fitness goal, and track progress
#This project uses the Tkinter module to build a user-friendly graphical
# interface (GUI).

# A GUI widget is a graphical component such as a button, text label as shown below.
# GUI widgets also exist to make drop-down menus and scroll bars, display images, etc...
# Tkinter gives you the ability to create GUI Windows containing widgets.
# This program is a simple exploration.
#######################################################################
# Acknowledgements:
####################################################################################

import tkinter as tk
from tkinter import messagebox


def log_work(workout_type, duration, intensity):
    """"
    This functions allows the user to log their workouts
    Args:
       workout_type (str): The type of workout (stairmaster, running, cycling).
       duration (int): The duration of the workout in minutes.
      intensity (str):  The  intensity level ( low, medium, high).

    Return: The logged workout details
        """

    if not workout_type:
        return "Please enter a workout:"
    if duration >=0:
        return "Please enter a postive number:"
    valid_intensities={"high", "low", "medium"}
    if intensity not in valid_intensities:
        return "Please enter a valid intensity"
    return{"type": workout_type, "duration" : duration, "intensity" : intensity}

root= tk.Tk()
root.title("FitPro App")
root.geometry("300x300")
textbox = tk.Text(root, height= 4, font=("Arial"))
textbox.pack(padx=10)

#creating the widgets
label = tk.Label(root, text= "welcome", font=("Arial", 16 ))
label.pack(padx = 10, pady = 10)


root.mainloop()

