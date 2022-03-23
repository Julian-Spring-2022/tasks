<<<<<<< Updated upstream
def test_tasks():
    pass
=======
from tempfile import TemporaryFile
import os

import tasks


def test_listing_tasks_not_compete():
    """
    Creating 2 tasks, then listing tasks shows the 2 created tasks.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")
    with TemporaryFile("w+", encoding="utf-8") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")
    # Note that UTF-8 encoding of checkmark ✅ is '\u2705'
    assert contents == ["Do laundry\n", "Clean up\n"]
    
def test_listing_tasks_some_complete():
    """
    Creating 2 tasks, complete second task, then listing tasks showing that
    the 1st task is not complete and the second task is complete.
    
    Also verify that list of tasks begins with 1 instead of 0, with argument
    to_complete
    """
    
    to_complete = 2
    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")
    tasks.complete("tests.csv",to_complete=to_complete)
    with TemporaryFile("w+", encoding="utf-8") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")
    # Note that UTF-8 encoding of checkmark ✅ is '\u2705'
    assert contents == ["Do laundry\n", "Clean up \u2705\n"]

def test_listing_no_tasks_does_not_error():
    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    assert contents==[]