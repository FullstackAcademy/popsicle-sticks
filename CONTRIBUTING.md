
# CONTRIBUTING

**TABLE OF CONTENTS**
- [CONTRIBUTING](#CONTRIBUTING)
    - [Issues](##issues)
    - [Pull Requests](##pull-requests)
        - [Set up pre-commit](###set-up-pre-commit)


---


Thank you for your consideration of contributing to this project.

Before contributing, we encourage you to read our CONTRIBUTING policy
(you are here) and our [README](README.md), all of which should be in this repository.

## Issues

Prior to raising an issue on this repository, we recommend you search through existing issues
(open or closed) to see if your issue has already been addressed or noted. If an issue exists but
is unresolved, feel free to leave a comment with details of your issue and run environment. You
can raise new issues [here](https://github.com/fullstackacademy/popsicle-sticks/issues).

## Pull Requests

If you submit a pull request, you will see your code ran through our continuous integration (CI)
system that runs various checks on your code to ensure it complies with our coding standard.
If your code fails these checks we will likely ask you to resolve the error so the checks pass.

We use [pre-commit](https://pre-commit.com) to check our code, which allows you to run and
resolve these checks locally.

### Set up pre-commit

It is recommended you set up a virtual environment to contain your dependencies to the project.
You can instantiate a virtual environment with the command `python -m venv <virtual environment name>`.
the virtual environment file will contain either a `scripts` or `bin` directory dependent on operating system.

If you are using Mac or Linux you can run `source venv/bin/activate`.

If you are using Windows you can run `venv\Scripts\Activate.ps1`.

Once this is done, make sure you install the requirements for the project: `python -m pip install -r requirements.txt`.

Now install pre-commit: `python -m pip install pre-commit`

Activate pre-commit: `pre-commit install`

Finally, run pre-commit across the files: `pre-commit run -a`

Pre-commit will notify you of any issues in the code and attempt to automatically resolve the issues, but may require
manual fixing.
