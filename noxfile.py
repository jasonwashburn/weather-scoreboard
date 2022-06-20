from pathlib import Path

import nox

VENV_DIR = Path("./venv")
locations = "src", "tests", "noxfile.py"

nox.options.sessions = "lint", "tests"


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-isort")
    session.run("flake8", *args)


@nox.session
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def format(session):
    session.install("black", "isort")
    session.run("isort", *locations)
    session.run("black", *locations)


@nox.session
def tests(session):
    args = session.posargs
    session.install("pytest", "pytest-mock", "pytest-cov")
    session.run("pytest", *args)
