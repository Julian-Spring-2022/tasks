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


DONE = " X"


def list(stdout=sys.stdout, filename="tasks.csv"):
    """
    List the current known tasks.
    """

    try:
        with open(filename) as tasks_file:
            reader = csv.reader(tasks_file)
            for name, completed in reader:
                stdout.write(f"{name}{DONE if eval(completed) else ''}\n")
    except FileNotFoundError:
        stdout.write("There are no tasks.\n")


def create(name, filename="tasks.csv"):
    """
    Create a new task.
    """

    with open(filename, "a", newline="") as tasks_file:
        writer = csv.writer(tasks_file)
        print(name)
        writer.writerow([name, False])


def complete(stdout=sys.stdout,filename="tasks.csv"):
    """
    Mark an existing task as completed.
    """

    with (
        open(filename) as tasks_file,
        NamedTemporaryFile("w", delete=False) as new):
        reader = csv.reader(tasks_file)
        print("Current tasks:")
        for id, (name, completed) in enumerate(reader):
            print(id+1, name, DONE if eval(completed) else '')

        to_complete = int(input("task ID?> "))
        writer = csv.writer(new, lineterminator="\n")
        tasks_file.seek(0)
        for id, (name, completed) in enumerate(reader):

            if id+1 == to_complete and eval(completed) == True:

                try:
                    raise Exception("Already completed, try again!")
                except:
                    stdout.write("Already completed, try again!\n")

            if id+1 == to_complete:
                writer.writerow([name, True])
            else:
                writer.writerow([name, completed])

    os.remove(filename)
    os.rename(new.name, filename)


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

        if operation == 'create':
            args = " ".join([*args])
            fn(args)
        else:
            fn(*args)


if __name__ == "__main__":
    main()



# NOTES
# 1) needed to use eval because string was "truthy" even though it said "False"
# 2) needed to join arguments in main function into one string
# 3) had to increment id in loops, delete tasks.csv file before renaming new file, and fix end of line 
# 4) Integrated exception when task was already completed

