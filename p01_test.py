

from FitPro import  User, Workout, FitPro

from inspect import getframeinfo, stack

def unittest(did_pass):
    """
    Print the result of a unit test.

    :param did_pass: a boolean representing the test
    :return: None
    """

    caller = getframeinfo(stack()[1][0])
    linenum = caller.lineno
    if did_pass:
        msg = "Test at line {0} ok.".format(linenum)
    else:
        msg = ("Test at line {0} FAILED.".format(linenum))
    print(msg)

# Tests for the User class
def test_user_class():
    """
    Test the User class function.
    """
    user = User("Joyce N", 25, 180)
    unittest(user.name == "Joyce N")
    unittest(user.age == 25)
    unittest(user.height == 180)

    # Create a workout instance
    workout = Workout("running", 30, 300)
    user.log_workout(workout)
    unittest(len(user.workouts) == 1)  # Check if workout was logged
    unittest(user.workouts[0].workout_type == "running")  # Verify workout type

# Testing the FitPro application's save_user
def test_fit_pro_save_user():









