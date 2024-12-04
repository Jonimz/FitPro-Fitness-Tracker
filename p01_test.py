from struct import unpack

from FitPro import *
import sys


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


def test_workout():
    result = log_work("running", 30, "medium")
    unittest(result == {"type": "running", "duration": 30, "intensity": "medium"})

    result = log_work("jogging",10, "medium" )
    unittest(result == {"type": "jogging", "duration": 10, "intensity": "medium"})

    result = log_work("running", 30, "tired")
    unittest(result == "Please enter a valid intensity")


if __name__ == "__main__":
    test_workout()



