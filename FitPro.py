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
        self.root.title("FitPro Workout Tracker")

        #the user data
        self.workout = []
        self.duration = 0
        self.calories = 0

        self.create_user_frame()
        self.create_workout_frame()

    def create_user_frame(self):
        """"
        creates the user information frame """



        user_frame = tk.Frame(self.root)
        user_frame.pack(pady = 10)

        tk.Label(user_frame, text = "Name:").grid(row =0, column = 2, padx= 5, pady= 5)
        self.name_entry = tk.Entry(user_frame)
        self.name_entry.grid(row= 0, column = 1, padx=5, pady= 5)

        tk.Label(user_frame, text="Age:").grid(row=0, column=2, padx=5, pady=5)
        self.age_entry = tk.Entry(user_frame)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(user_frame, text="Height:").grid(row=0, column=2, padx=5, pady=5)
        self.height_entry = tk.Entry(user_frame)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)

    def create_workout_fame(self):
        """
        creates the workout logging and progress fame

        :return:
        """
        workout_fame = tk.Frame()
        workout_fame.pack(pady=10)

        tk.Label(workout_fame, text = "Workout Type:").grid(row = 5, column = 2, padx= 5, pady = 5 )
        self.type = tk.Entry(workout_fame)
        self.type.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(workout_fame, text="Duration(mins):").grid(row=0, column=2, padx=5, pady=5)
        self.duration_entry = tk.Entry(workout_fame)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(workout_fame, text="Calories Burned:").grid(row=0, column=2, padx=5, pady=5)
        self.calories_entry= tk.Entry(workout_fame)
        self.calories_entry.grid(row=2, column=1, padx=5, pady=5)
















if __name__ == "__main__":
    root = tk.Tk()
    app = FitPro(root)
    root.mainloop()








