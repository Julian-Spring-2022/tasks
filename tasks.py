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
import sys


DONE = " ✅"


def list(stdout=sys.stdout, filename="tasks.csv"):
    """
    List the current known tasks.
    """

    try:
        with open(filename) as tasks_file:
            reader = csv.reader(tasks_file)
            for name, completed in reader:
                stdout.write(f"{name}{DONE if completed == 'True' else ''}\n")
    except FileNotFoundError:
        stdout.write("There are no tasks.\n")


def create(name, status=False, filename="tasks.csv"):
    """
    Create a new task.
    """

    with open(filename, "a") as tasks_file:
        writer = csv.writer(tasks_file)
        writer.writerow([name, status])


def complete(completing=True, stdout=sys.stdout, filename="tasks.csv"):
    """
    Mark an existing task as completed.
    """

    try:
        with (
            open(filename) as tasks_file,
            NamedTemporaryFile("w", delete=False) as new,
        ):
            reader = csv.reader(tasks_file)
            stdout.write("Current tasks:\n")
            for id, (name, completed) in enumerate(reader):
                if completed != 'True':
                    stdout.write(f"{id + 1} {name} {completed}\n")

            if completing:
                to_complete = int(input("task ID?> ")) - 1
                writer = csv.writer(new)
                tasks_file.seek(0)
                for id, (name, completed) in enumerate(reader):
                    if id == to_complete:
                        writer.writerow([name, True])
                    else:
                        writer.writerow([name, completed])

                os.rename(new.name, filename)

    except FileNotFoundError:
        stdout.write("There are no tasks.\n")


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
