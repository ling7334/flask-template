# How to contribute to Flask-template

Thank you for considering contributing to Flask-template!

## Support questions

Please, don't use the issue tracker for this. Use one of the following
resources for questions about your own code:

* [e-mail](mailto:ling7334@gmail.com)

## Reporting issues

- Describe what you expected to happen.
- If possible, include a [minimal, complete, and verifiable example](https://stackoverflow.com/help/mcve) to help
  us identify the issue. This also helps check that the issue is not with your
  own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python, Flask, SQLAlchemy and flask-sqlalchemy versions. If possible, check if this
  issue is already fixed in the repository.

## Submitting patches

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- Try to follow [PEP8](https://pep8.org/), but you may ignore the line length limit if following
  it would make the code uglier.

### First time setup

- Download and install the [latest version of git](https://git-scm.com/downloads).
- Configure git with your [username](https://help.github.com/articles/setting-your-username-in-git/)
and [email](https://help.github.com/articles/setting-your-email-in-git/):

        git config --global user.name 'your name'
        git config --global user.email 'your email'

- Make sure you have a [GitHub account](https://github.com/join).
- Fork Flask-template to your GitHub account by clicking the [Fork](https://github.com/ling7334/flask-template/fork) button.
- [Clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork) your GitHub fork locally:

        git clone https://github.com/{username}/flask-template
        cd flask-template

- Add the main repository as a remote to update later::

        git remote add origin https://github.com/ling7334/flask-template
        git fetch origin

- Install `Pipenv`:

      python3 -m pip install pipenv

- Create a virtualenv and install depedence:

        pipenv install

### Start coding

- Create a branch to identify the issue you would like to work on (e.g.
  ``2287-dry-test-suite``)
- Using your favorite editor, make your changes, 
[committing as you go](https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes).
- Try to follow [PEP8](https://pep8.org/), but you may ignore the line length limit if following
  it would make the code uglier.
- Include tests that cover any code changes you make. Make sure the test fails
  without your patch.
- Push your commits to GitHub and [create a pull request](https://help.github.com/articles/creating-a-pull-request/).
- Celebrate 🎉

### Running the tests

Run the basic test suite with:

    pytest

This only runs the tests for the current environment. Whether this is relevant
depends on which part of Flask you're working on. Travis-CI will run the full
suite when you submit your pull request.

The full test suite takes a long time to run because it tests multiple
combinations of Python and dependencies. You need to have Python 2.7, 3.4,
3.5 3.6, and PyPy 2.7 installed to run all of the environments. Then run:

    tox

### Running test coverage

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run ``pytest`` using ``coverage`` and generate a
report on the terminal and as an interactive HTML document::

    coverage run -m pytest
    coverage report
    coverage html
    # then open htmlcov/index.html

Read more about [coverage](https://coverage.readthedocs.io>).

Running the full test suite with ``tox`` will combine the coverage reports
from all runs.


# Building the docs

Build the docs in the ``docs`` directory using Sphinx:

    cd docs
    make html

Open ``_build/html/index.html`` in your browser to view the docs.

Read more about [Sphinx](https://www.sphinx-doc.org).
