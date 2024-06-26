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

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).


## Deploy on Vercel

**NOTE**: a problem vercel is that the AI model cannot be deployed on our backend because the necessary libraries exceed the size limit of Vercel's free tier. Alternative deployment options might have to be researched.

**NOTE**: This repo is part of an organization, to make use of vercels on-click deployment, you will have to have an vercel pro plan. One work around to keep using a hobby plan, is to deploy using github actions. You will need 3 keys: VERCEL_TOKEN, ORG_ID, PROJECT_ID. The GITHUB_TOKEN gets filled in automatically.

To get the VERCEL_TOKEN, you will have to login in your account and create one manually.

To get the ORG_ID and PROJECT_ID, I recommend that you download the [vercel CLI](https://vercel.com/docs/cli). Then run the command ```vercel```. The first time it will ask some question that can be left default(if nothing has changed). It will then deploy a version to vercel and generate a .vercel folder in your project folder. This folder contains a json containing the ORG_ID and PROJECT_ID.

These 3 can be filled in the repository secrets. 
