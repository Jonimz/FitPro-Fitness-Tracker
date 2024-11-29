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
import turtle

from pygame.examples.scrap_clipboard import screen


class User:
    """A class for the user information for Fitpro
    """
    def __init__(self, name, age, height, workout):
        self.name= name
        self.age= age
        self.height= height
        self.workout = []

    def log_workout(self, workout):
        """
        A function for the user's workouts

        :arg: a workout object to be added to the list
        """
        self.workouts.append(workout)

    def __str__(self):
        """"
        :returns: string representing the user age, name, height
        """
        return f"User(name={self.name}, age= {self.age}, height= {self.height})"

class Workout:
    """
    class for the workout session
    """
    def __init__(self, workout_type, duration, calories):
        """initializes a workout instance with workout_type, duration, calories
        """
        self.workout_type = workout_type
        self.duration = duration
        self.calories= calories

class FitPro:
    def __init__(self,  root):
        self.root= tk.Tk
        self.root.title("FitPro workout Tracker")

        #the user data
        self.workout = []
        self.duration = 0
        self.calories = 0

        self.create_widgets()

    def create_widgets(self):







screen.mainloop()

