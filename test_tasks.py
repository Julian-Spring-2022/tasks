<<<<<<< Updated upstream
def test_tasks():
    pass
=======
from tempfile import TemporaryFile
import os

import tasks


def test_new_task_should_be_incomplete():
    """
    Testing bug #1: when creating a task it should not be marked as complete.
    """
    with TemporaryFile("w+") as stdout:
        tasks.create("test", filename="tests.csv")
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")
    assert contents == ["test\n"]


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

    assert contents == ["Do laundry\n", "Clean up\n"]


def test_listing_no_tasks_does_not_error():
    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    assert contents == ["There are no tasks.\n"]


def test_completing_no_tasks_does_not_error():
    with TemporaryFile("w+") as stdout:
        tasks.complete(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    assert contents == ["There are no tasks.\n"]


def test_ids_of_completable_tasks_should_start_at_1():
    """
    Testing feature #3: when listing the tasks to complete, the IDs should
    start at 1.
    """
    tasks.create("test1", filename="tests.csv")
    tasks.create("test2", filename="tests.csv")
    with TemporaryFile("w+") as stdout:
        tasks.complete(completing=False, stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")

    assert contents == ["Current tasks:\n",
                        "1 test1 False\n",
                        "2 test2 False\n"]


def test_completed_tasks_are_filtered_from_completable_tasks():
    """
    Testing feature #4: completed task are filtered out entirely from the list
    of completable tasks.
    """
    tasks.create("test1", status=True, filename="tests.csv")
    tasks.create("test2", filename="tests.csv")
    with TemporaryFile("w+") as stdout:
        tasks.complete(completing=False, stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")

    assert contents == ["Current tasks:\n",
                        "2 test2 False\n"]
>>>>>>> Stashed changes
