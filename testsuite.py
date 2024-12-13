from inspect import getframeinfo, stack
from FitPro import User, Workout, FitPro

def unittest(did_pass):
    """
    Print the result of a unit test.
    :param did_pass: a boolean representing the test
    """
    caller = getframeinfo(stack()[1][0])
    linenum = caller.lineno
    if did_pass:
        print(f"Test at line {linenum} ok.")
    else:
        print(f"Test at line {linenum} FAILED.")

def fitpro_testsuite():
    """
    Test suite for the User and Workout classes.
    """
    print("\nRunning fitpro_testsuite().")

    # Test User class initialization
    user = User("Alice", 25, 160)
    unittest(user.name == "Alice")
    unittest(user.age == 25)
    unittest(user.height == 160)
    unittest(user.workouts == [])

    # Test logging a workout
    workout1 = Workout("Yoga", 30, 200)
    user.log_workout(workout1)
    unittest(len(user.workouts) == 1)
    unittest(user.workouts[0] == workout1)
    unittest(user.workouts[0].workout_type == "Yoga")
    unittest(user.workouts[0].duration == 30)
    unittest(user.workouts[0].calories == 200)

    # Test string representation of User
    unittest(str(user) == "User(name=Alice, age=25, height=160)")

    # Test multiple workouts
    workout2 = Workout("Running", 45, 300)
    workout3 = Workout("Cycling", 60, 500)
    user.log_workout(workout2)
    user.log_workout(workout3)
    unittest(len(user.workouts) == 3)
    unittest(user.workouts[1] == workout2)
    unittest(user.workouts[2] == workout3)

    print("fitpro_testsuite() is complete.")

if __name__ == "__main__":
    fitpro_testsuite()
