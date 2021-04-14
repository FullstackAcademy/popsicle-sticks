<p align="center">
  <a href="" rel="noopener">
 <img width=100px height=100px src="./assets/PSLogo.png" alt="Project logo"></a>
</p>

<h3 align="center">Popsicle Sticks</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/fullstackacademy/FullStackAcademy/popsicle-sticks.svg)](https://github.com/FullStackAcademy/popsicle-sticks/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/FullStackAcademy/popsicle-sticks.svg)](https://github.com/FullStackAcademy/popsicle-sticks/pulls)

</div>

---

<p align="center"> A class instructional tool
    <br>
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

Popsicle Sticks is a program intended to facilitate cold calling students during class in a way that is fair, random, and trackable. Popsicle Sticks provides an option to run as a GUI or CLI and allows the ingestion of class rosters from a csv file.

## 🏁 Getting Started <a name = "getting_started"></a>

You can run clone this repository with the `git clone` command and run directly from source, or you can use our `releases` and grab the binary for your operating system.

### Prerequisites

`python 3.7.5` is a prerequisite to running this program from source. If you need help installing Python in your environment, follow the instructions [here](https://docs.Python.org/3/using/windows.html).

```
$ python --version
Python 3.8.2
```

### Installing

To run from source, you must install the requirements.

```
python -m pip install -r requirements.txt
```


## 🎈 Usage <a name="usage"></a>

### CLI Options
```console
$  python popsicle_sticks_cli.py
usage: popsicle_sticks_cli.py [--help] [create, add, remove, reset, destroy, pull]

optional arguments:
--help                  show this help message and exit

modules:
create                  accept student names and create database
add [student]           add a single student to the database
remove [student]        remove a student from the database
reset [student]         if a single student is provided, reset student's counter, else reset entire database
destroy                 destroy the database, removing all students
```

### GUI Options

![](./assets/PopsicleSticksDemo.gif)

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.Python.org/) - Language
- [Pandas](https://pandas.pydata.org) - CSV Parsing
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - GUI Framework

## ✍️ Authors <a name = "authors"></a>

- [@DeemOnSecurity](https://github.com/DeemOnSecurity)
