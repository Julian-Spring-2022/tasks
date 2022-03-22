from tempfile import TemporaryFile
import os

import tasks


def test_listing_tasks():
    """
    Creating 2 tasks, then listing tasks shows the 2 created tasks.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")
    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")
    
    # assert contents == ["Do laundry ✅\n", "Clean up ✅\n"]
    assert contents == ["Do laundry V\n", "Clean up V\n"]
    
#def test_listing_no_tasks_does_not_error():
#    with TemporaryFile("w+") as stdout:
#        tasks.list(stdout=stdout, filename="tests.csv")