#!/usr/bin/env python

"""GUI version of popsicle sticks."""

# Standard Python Libraries
from typing import List

# Third-Party Libraries
import PySimpleGUI as sg

# Fullstack Academy Libraries
from popsicle_sticks_cli import (
    Database,
    add,
    edit,
    grab_csv,
    load_from_csv,
    pull,
    remove,
    reset,
)


def student_text(db: Database) -> List[str]:
    """Return student names formatted to fit the listbox.

    Args:
        db (Database): A database file.

    Returns:
        List[str]: A list of formatted student text.
    """
    return ["{:<45}\t{:<3}".format(k, v) for k, v in db.students.items()]


def window_height(db: Database) -> int:
    """Set the window height to 15 by default or the size of the number of students.

    Args:
        db (Database): A database file.

    Returns:
        int: The window height.
    """
    if len(db.students) > 15:
        return len(db.students)
    else:
        return 15


if __name__ == "__main__":
    """Set theme and initialize database."""
    sg.theme("DarkGrey14")
    db = Database()

    """Launch popup to ask for csv file path if the db does not exist or is empty."""
    if not db.students:
        try:
            load_from_csv(
                db,
                sg.popup_get_file(
                    "Load a student roster csv (from learndot), press cancel to manually load.",
                    title="Load from CSV",
                    default_path=grab_csv(),
                ),
            )
        except ValueError:
            pass

    """Set layout for our window."""
    layout = [
        [sg.Text("You pulled:"), sg.Text(size=(25, 1), key="-OUTPUT-")],
        [sg.Listbox(student_text(db), size=(33, window_height(db)), key="-STUDENTS-")],
        [
            sg.Button("Pull"),
            sg.Button("Add"),
            sg.Button("Remove"),
            sg.Button("Edit"),
            sg.Button("Reset"),
        ],
    ]

    """Instantiate our window."""
    window = sg.Window("Popsicle Sticks", layout, grab_anywhere=True)

    """Event loop."""
    while True:
        event, values = window.read()  # Read the event and values from window.

        if event == sg.WIN_CLOSED:  # If window is closed.
            break

        elif event == "Reset":  # If "Reset" is pressed.
            if values["-STUDENTS-"]:
                reset(db, values["-STUDENTS-"][0].split("\t")[0])
            else:
                reset(db, None)

        elif event == "Add":  # If "Add" is pressed.
            add(db, sg.popup_get_text("Enter a name."))

        elif event == "Remove":  # If "Remove" is pressed.
            if values["-STUDENTS-"]:
                remove(db, values["-STUDENTS-"][0].split("\t")[0])

        elif event == "Edit":  # If "Edit" is pressed.
            if values["-STUDENTS-"]:
                edit(
                    db,
                    values["-STUDENTS-"][0].split("\t")[0],
                    sg.popup_get_text(
                        "Enter a name.",
                        default_text=values["-STUDENTS-"][0].split("\t")[0],
                    ),
                )

        elif event == "Pull":  # If "Pull" is pressed.
            window["-OUTPUT-"].update(pull(db))
        window["-STUDENTS-"].update(student_text(db))

    """Write out database file and close the window."""
    db.write()
    window.close()
