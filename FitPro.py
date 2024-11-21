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
        print("Please enter a workout")
    if duration >=0:
        print("Please enter a postive number")

    if  intensity not in{"high, low, medium, moderate"}:
        print("Renter Intensity")
    return{"type": workout_type, "duration" : duration, "intensity" : intensity}


