import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

class User:
    """A class for the user information for FitPro."""

    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.height = height
        self.workouts = []

    def log_workout(self, workout):
        """Adds a workout to the user's workout list."""
        self.workouts.append(workout)

    def __str__(self):
        """Returns a string representation of the user."""
        return f"User(name={self.name}, age={self.age}, height={self.height})"

class Workout:
    """A class for individual workout sessions."""

    def __init__(self, workout_type, duration, calories):
        self.workout_type = workout_type
        self.duration = duration
        self.calories = calories

class FitPro:
    """A class for the FitPro application."""

    def __init__(self, window):
        self.window = window
        self.window.title("FitPro Workout Tracker")
        self.user = None

        # Initialize instance attributes
        self.name_entry = None
        self.age_entry = None
        self.height_entry = None
        self.workout_type_entry = None
        self.duration_entry = None
        self.calories_entry = None

        self.create_user_frame()
        self.create_workout_frame()

    def create_user_frame(self):
        """Creates the user information frame."""
        user_frame = tk.Frame(self.window)
        user_frame.pack(pady=10)

        tk.Label(user_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(user_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(user_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(user_frame)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(user_frame, text="Height (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(user_frame)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(user_frame, text="Login", command=self.log_in).grid(row=3, columnspan=2, pady=10)

    def log_in(self):
        """Saves user information."""
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            height = float(self.height_entry.get())

            if not name:
                raise ValueError("Please enter a name.")
            if age < 1 or age > 120:
                raise ValueError("Please enter a valid age between 1 and 120.")
            if height < 30 or height > 300:
                raise ValueError("Please enter a valid height between 30 cm and 300 cm.")

            self.user = User(name, age, height)
            messagebox.showinfo("Success", f"User saved: {self.user}")

            # Clear input fields after successful login
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.height_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def create_workout_frame(self):
        """Creates the workout logging and progress frame."""
        workout_frame = tk.Frame(self.window)
        workout_frame.pack(pady=10)

        tk.Label(workout_frame, text="Workout Type:").grid(row=0, column=0, padx=5, pady=5)
        self.workout_type_entry = tk.Entry(workout_frame)
        self.workout_type_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(workout_frame, text="Duration (minutes):").grid(row=1, column=0, padx=10, pady=5)
        self.duration_entry = tk.Entry(workout_frame)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(workout_frame, text="Calories Burned:").grid(row=2, column=0, padx=5, pady=5)
        self.calories_entry = tk.Entry(workout_frame)
        self.calories_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(workout_frame, text="Log Workout", command=self.log_workout).grid(row=3, columnspan=2, pady=10)
        tk.Button(self.window, text="View Progress", command=self.view_progress).pack(pady=5)

    def log_workout(self):
        """Logs a workout for the user."""
        if not self.user:
            messagebox.showwarning("No User", "Please save user information first.")
            return

        try:
            workout_type = self.workout_type_entry.get().strip()
            duration = int(self.duration_entry.get())
            calories = int(self.calories_entry.get())

            if not workout_type:
                raise ValueError("Please enter the workout type.")
            if duration <= 0 or calories <= 0:
                raise ValueError("Please enter positive numbers for duration and calories.")

            workout = Workout(workout_type, duration, calories)
            self.user.log_workout(workout)

            self.workout_type_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.calories_entry.delete(0, tk.END)

            messagebox.showinfo("Success", f"Workout logged: {workout_type}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def view_progress(self):
        """Displays the user's workout progress."""
        if not self.user:
            messagebox.showwarning("Missing User Info", "Please enter the user information first.")
            return

        total_workouts = len(self.user.workouts)
        total_duration = sum(w.duration for w in self.user.workouts)
        total_calories = sum(w.calories for w in self.user.workouts)

        progress_message = (
            f"Name: {self.user.name}\n"
            f"Total Workouts: {total_workouts}\n"
            f"Total Duration: {total_duration} minutes\n"
            f"Total Calories Burned: {total_calories} kcal"
        )

        messagebox.showinfo("Workout Progress", progress_message)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='light gray')
    app = FitPro(root)
    root.mainloop()
