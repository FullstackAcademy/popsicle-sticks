#!/usr/bin/env python

"""CLI version of popsicle sticks."""

# Standard Python Libraries
import json
import os
from pathlib import Path
from random import randrange
import re
import sys
from typing import Callable, Dict, Generator, List

# Third-Party Libraries
import pandas


def grab_csv() -> str:
    """Grab a relevant CSV file in the current directory.

    Returns:
        str: A CSV file path.
    """
    listed_directory = os.listdir()
    for file in listed_directory:
        match = re.search(r".*[0-9]{4}\-[A-Z]{1,4}\-[A-Z]{1,4}\-CYB-[PF]T.csv", file)
        if match:
            return match.string


class Name(object):
    """Name object used for storing student names."""

    def __init__(self, first_name: str, last_name: str) -> None:
        """Initialize Name.

        Args:
            first_name (str): A first name.
            last_name (str): A last name.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = " ".join([self.first_name, self.last_name])


class Names(object):
    """Names object used for storing a collection of student names."""

    def __init__(self, csv_path: str = grab_csv()) -> None:
        """Initialize Names.

        Args:
            csv_path (str, optional): A path to a CSV roster file. Defaults to grab_csv().
        """
        super().__init__()
        self.csv_path = csv_path
        self.dataframe = pandas.read_csv(self.csv_path)
        self._names = list(self._process_names())

    @property
    def non_unique_names(self) -> List[str]:
        """Return non-unique first names in the data set.

        Returns:
            List[str]: A list of non-unique first names.
        """
        first_names = [
            name.first_name for name in self._names
        ]  # grab first names from our names list
        non_unique = list(
            {ele for ele in first_names if first_names.count(ele) > 1}
        )  # check to make sure first names only appear once
        return non_unique

    @property
    def names(self) -> Generator[str, None, None]:
        """Yield first names of students if unique, full names if not.

        Yields:
            Generator[str, None, None]: Names of students.
        """
        for name in self._names:
            if name.first_name not in self.non_unique_names:
                yield name.first_name
            else:
                yield name.full_name

    def _process_names(self):
        """Process the names of students in a csv to grab a nickname if a student has one, first name if not and last name."""
        for _, row in self.dataframe.iterrows():
            first_name = row["nickname"]
            if str(first_name).lower() == "nan":
                first_name = row["firstName"]
            last_name = row["lastName"]
            yield Name(first_name, last_name)


class Database(object):
    """Database class used for storing student data."""

    def __init__(
        self,
        db_path: str = "./db.json",
        load_from_csv: bool = False,
        csv_path: str = "",
    ) -> None:
        """Initialize Database.

        Args:
            db_path (str, optional): A path to a database file. Defaults to "./db.json".
            load_from_csv (bool, optional): Option to load from a CSV file. Defaults to False.
            csv_path (str, optional): A path to a CSV file. Defaults to "".
        """
        super().__init__()
        self.db_path: str = db_path
        self.contents: dict = self._load()
        if load_from_csv:
            if not csv_path:
                csv_path = grab_csv()
            self.load_from_csv(csv_path)
        self.students = self.contents["students"]
        self.last_student = self.contents["last student"]

    @staticmethod
    def is_empty(file_path: str) -> bool:
        """Given a file path, determine if the file is empty.

        Args:
            file_path (str): A file path.

        Returns:
            bool: If a file is empty.
        """
        if os.path.exists(file_path):
            return os.stat(file_path).st_size == 0

    def _load(self) -> dict:
        """Open and read the db file if it exists, if not provide generic blank data."""
        if not os.path.exists(self.db_path) or self.is_empty(self.db_path):
            Path(self.db_path).touch()
            return {"students": {}, "last student": ""}
        return json.loads(open(self.db_path).read())

    @property
    def lowest_value(self) -> int:
        """Grab the lowest value of the student keys.

        Returns:
            int: The lowest value.
        """
        return int(min(self.students.items(), key=lambda x: x[1])[1])

    def write(self):
        """Write out the data in the class to the dbfile."""
        with open(self.db_path, "w+") as writeout:
            writeout.write(
                json.dumps(
                    {"students": self.students, "last student": self.last_student}
                )
            )

    def append(self, student_name: str, value: int = 0):
        """Append a student to the database.

        Args:
            student_name (str): A student name.
            value (int, optional): A value for the student. Defaults to 0.
        """
        self.students[student_name] = value

    def remove(self, student_name: str):
        """Remove a student from the database.

        Args:
            student_name (str): A student name.
        """
        self.students.pop(student_name, None)

    def reset(self, student_name: str = None):
        """Reset the value of a student or the whole database if student_name is None.

        Args:
            student_name (str, optional): A student name. Defaults to None.
        """
        if student_name:
            self.students[student_name] = 0
            return
        for student_name in self.students:
            self.students[student_name] = 0
        self.last_student = ""

    def destroy(self):
        """Destroy the database (nullify contents)."""
        self.students = {}
        self.last_student = ""

    def pull(self) -> str:
        """Increment the value of the student and return a student name.

        Gets a random integer between 0 and the number of students and returns
        a student name if they were not the last called on and they are not >= 2
        calls more than the lowest student value. i.e. a student that has been called
        on 3 times will not be called on again until a student that has been called on
        1 time is called again.

        Returns:
            str: A student name.
        """
        while True:
            random_integer = randrange(0, len(self.students))  # nosec
            student_name = list(self.students)[random_integer]
            if (
                not self.students[student_name] - self.lowest_value >= 2
                and student_name != self.last_student
            ):
                return self._extracted_from_pull_6(student_name)
            if not self.students[student_name] - self.lowest_value >= 2:
                return self._extracted_from_pull_6(student_name)

    def _extracted_from_pull_6(self, student_name: str) -> str:
        """Increment student value and set last student to the student name.

        Args:
            student_name (str): A student name.

        Returns:
            str: A student name.
        """
        self.students[student_name] += 1
        self.last_student = student_name
        return student_name

    def edit(self, original: str, fix: str):
        """Edit a student name.

        Args:
            original (str): The original name.
            fix (str): The modified name.
        """
        value = self.students[original]
        self.remove(original)
        self.append(fix, value)

    def load_from_csv(self, csv_path: str = None):
        """Read the given csv and loads its data into a database file.

        Args:
            csv_path (str, optional): A path to a valid csv file. Defaults to None.
        """
        try:
            student_names = Names(csv_path)
            for name in student_names.names:
                self.students[name] = 0
        except AttributeError:
            self.students = {}


def database(db_path: str = "db.json") -> Dict[str, int]:
    """Create a database if one does not exist, load it if it does.

    Args:
        db_path (str, optional): A path to a database. Defaults to 'db.json'.

    Returns:
        Dict[str, int]: Loaded database data.
    """
    if not os.path.exists(db_path):
        Path(db_path).touch()
    return json.loads(open(db_path).read())


def edit(db: Database, original: str, fix: str):
    """Replace a student name in a database with a new name.

    Args:
        db (Database): A database file.
        original (str): The current student name.
        fix (str): The new/changed student name.
    """
    db.edit(original, fix)


def create(db: Database):
    """Loop add function while input is presented. Good for entering multiple student names.

    Args:
        db (Database): A database file.
    """
    valid_input = True
    while valid_input:
        valid_input = add(db, None)


def add(db: Database, student_name: str):
    """Add a student name to the database.

    Args:
        db (Database): A database file.
        student_name (str): A student name.
    """
    if not student_name:
        print("Current Students")
        print("----------------")
        [print(x) for x in db.students]
        student_name = input("Student Name => ")
    if not student_name:
        return
    db.append(student_name)


def remove(db: Database, student_name: str):
    """Remove a student name from the database.

    Args:
        db (Database): A database file.
        student_name (str): A student name.
    """
    db.remove(student_name)


def reset(db: Database, student_name: str):
    """Reset the value of a student in the database. Reset all students if student_name is None.

    Args:
        db (Database): A database file.
        student_name (str): A student name.
    """
    db.reset(student_name)


def destroy(db: Database):
    """Destroy the database, setting blank values.

    Args:
        db (Database): A database file.
    """
    db.destroy()


def pull(db: Database) -> str:
    """Return a student name at random. Increment the student value.

    Args:
        db (Database): A database file.

    Returns:
        str: A student name.
    """
    return db.pull()


def _check_multiple(
    arguments: sys.argv, database: Database, function: Callable, *args, **kwargs
):
    """If multiple arguments are presented, loop the given function until there are no more arguments.

    This is used for functions like `add` so multiple students can be input at once with space-delimited
    arguments, e.g.: python popsickle_sticks_cli.py add "Alan Turing" "Ada Lovelace" "Grace Hopper"

    Args:
        arguments (sys.argv): The system arguments.
        database (Database): A database file.
        function (Callable): A function to run.
    """
    if len(arguments) >= 3:
        for argument in arguments[2:]:
            function(database, argument, *args, **kwargs)
    else:
        function(database, None)


def load_from_csv(database: Database, csv_path: str):
    """Load database values from a CSV roster file.

    Args:
        database (Database): A database file.
        csv_path (str): The path to a CSV roster file.
    """
    if not database.students:
        database.load_from_csv(csv_path)


if __name__ == "__main__":
    help_message = """usage: popsicle_sticks_cli.py [--help] [create, add, remove, reset, destroy, pull, load]

optional arguments:
--help                  show this help message and exit

modules:
create                  accept student names and create database
add [student]           add a single student to the database
remove [student]        remove a student from the database
reset [student]         if a single student is provided, reset student's counter, else reset entire database
destroy                 destroy the database, removing all students
load [csv file path]    load database from values in a CSV roster file.
    """

    if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "--help":
        print(help_message)
        sys.exit(1)
    module = sys.argv[1]
    db = Database()
    if module == "create":
        create(db)
    elif module == "add":
        _check_multiple(sys.argv, db, add)
    elif module == "remove":
        _check_multiple(sys.argv, db, remove)
    elif module == "reset":
        _check_multiple(sys.argv, db, reset)
    elif module == "destroy":
        destroy(db)
    elif module == "pull":
        print(pull(db))
    elif module == "load":
        if len(sys.argv) == 3:
            load_from_csv(db, sys.argv[2])
        else:
            print(
                "No csv file presented. Please specify the csv file to load from like: python popsicle_sticks_cli.py load 'student_roster.csv'"
            )
    else:
        print("Please provide a valid module to run.")
        sys.exit(1)
    db.write()
    sys.exit(0)
