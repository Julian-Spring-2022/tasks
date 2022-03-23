#!/usr/bin/env python3
"""
A simple task manager.

For the purposes of our exercise we store tasks in a file which we'll
call tasks.csv (a CSV file). We'll talk more later about other ways to
store state which are more robust.
"""
from tempfile import NamedTemporaryFile
import csv
import os


DONE = " ✅"


def list():
    """
    List the current known tasks.
    """

    with open("tasks.csv") as tasks_file:
        reader = csv.reader(tasks_file)
        for name, completed in reader:
            print(f"{name}{DONE if completed else ''}")


def create(name):
    """
    Create a new task.
    """

    with open("tasks.csv", "a") as tasks_file:
        writer = csv.writer(tasks_file)
        writer.writerow([name, False])


def complete():
    """
    Mark an existing task as completed.
    """

    with (
        open("tasks.csv") as tasks_file,
        NamedTemporaryFile("w", delete=False) as new,
    ):
        reader = csv.reader(tasks_file)
        print("Current tasks:")
        for id, (name, completed) in enumerate(reader):
            print(id, name, completed)

        to_complete = int(input("task ID?> "))
        writer = csv.writer(new)
        tasks_file.seek(0)
        for id, (name, completed) in enumerate(reader):
            if id == to_complete:
                writer.writerow([name, True])
            else:
                writer.writerow([name, completed])

    os.rename(new.name, "tasks.csv")


operations = dict(
    create=create,
    complete=complete,
    list=list,
)


def main():
    print("Enter a command [create, list, complete].")
    while True:
        line = input("-> ").strip()
        if not line:
            return

        operation, *args = line.split()
        fn = operations.get(operation)
        fn(*args)


if __name__ == "__main__":
    main()
