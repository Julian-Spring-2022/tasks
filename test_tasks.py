from tempfile import TemporaryFile
import os
import unittest

import tasks


def test_listing_tasks():
    """
    Creating 2 uncompleted tasks, then listing tasks shows the 2 created tasks.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")
    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")
    
    assert contents == ["Do laundry\n", "Clean up\n"]
    
    
def test_listing_no_tasks_does_not_error():
    """
    Try to read tasks and throw an error if there is no file with tasks. 
    """

    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    assert contents == ["There are no tasks.\n"]


def test_completing_tasks(monkeypatch):
    """
    Create tasks and then mark the first of them as complete. 
    Test whether the first task is actually shown as complete.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")

    monkeypatch.setattr('builtins.input', lambda _: "1")

    tasks.complete(filename="tests.csv")   

    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")

    assert contents == ["Do laundry X\n", "Clean up\n"]



def test_exception_when_already_complete(monkeypatch):
    """
    Create two tasks and mark one of them as complete repeatedly. 
    Test whether the corresponding exception is thrown.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")

    monkeypatch.setattr('builtins.input', lambda _: "1")

    tasks.complete(filename="tests.csv")

    with TemporaryFile("w+") as stdout:
        tasks.complete(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()

    os.remove("tests.csv")

    assert contents == ["Already completed, try again!\n"]



