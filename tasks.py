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


#DONE = " ✅"
DONE = " \u2705"


def list(stdout=sys.stdout, filename="tasks.csv"):
    """
    List the current known tasks.
    """
    # HW TASK 1: check box ONLY if completed=="True"
    try:
        with open(filename) as tasks_file:
            reader = csv.reader(tasks_file)
            for name, completed in reader:
                output = name 
                if completed=="True":
                    output = name + DONE
                stdout.write(f"{output}\n")
    except FileNotFoundError:
        pass


def create(name, filename="tasks.csv"):
    """
    Create a new task.
    """
    # added newline option to address compatibility for Windows
    with open(filename, "a", newline='') as tasks_file:
        writer = csv.writer(tasks_file)
        writer.writerow([name, False])


def complete(filename='tasks.csv',to_complete=None):
    """
    Mark an existing task as completed.
    """

    with (
        # added newline option to address compatibility for Windows
        open(filename,newline='') as tasks_file, 
        NamedTemporaryFile("w", delete=False,newline='') as new,
    ):
        reader = csv.reader(tasks_file)
        print("Current tasks:")
        # HW TASK 2: index tasks to begin counter at 1
        for id, (name, completed) in enumerate(reader):
            print(id+1, name, completed)
        # clunky, but facilitates testsing
        if to_complete==None:
            to_complete = int(input("task ID?> "))
        writer = csv.writer(new)
        tasks_file.seek(0)
        # HW TASK 2 (continued): index tasks to begin counter at 1
        for id, (name, completed) in enumerate(reader):
            if id == to_complete-1:
                writer.writerow([name, True])
            else:
                writer.writerow([name, completed])
    # for Windows compatibility, must remove "tasks.csv" to overwrite
    try:
        os.remove(filename)  
        os.rename(new.name, filename)        
    except:
        os.rename(new.name, filename)


operations = dict(
    create=create,
    complete=complete,
    list=list,
)


operations = dict(
    create=create,
    complete=complete,
    list=list,
)


def main():
    # Modified input instructions, for clarity
    print("Enter a command [create <taskname>, list, complete].")
    while True:
        line = input("-> ").strip()
        if not line:
            return

        operation, *args = line.split()
        fn = operations.get(operation)
        fn(*args)


if __name__ == "__main__":
    main()