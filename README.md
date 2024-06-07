# Backend

The backend for the PWA

install pipenv:
https://pipenv.pypa.io/en/latest/installation.html

```bash
pip install pipenv --user
```

Pipenv is a dependency manager for Python projects. If you’re using pip and virtualenv, you can replace those with pipenv. Use the pipfile to manage dependencies and the pipfile.lock to ensure deterministic builds.

## IMPORTANT NOTE

We had issues with just freezing the requirements.txt file, so we are using pipenv to manage the dependencies. If you want to add a new dependency, you should run the following command:

```bash
pipenv install <package-name>
```

Before you commit your changes, you should run the following command to update the lockfile:

```bash
pipenv lock
```

Then you can run the following command to update the requirements.txt file:

```bash
pipenv requirements > requirements.txt
```

## Run

```bash
pipenv run dev
```

This will start the server on port 8000, by running the dev script defined in the Pipfile.
