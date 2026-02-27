
# Python API Template

#### Python version
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

#### Package and project manager
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat&logoColor=white&label=uv&color=yellow)](https://github.com/astral-sh/uv)

#### Server and API
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32.0-green?style=flat&logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)

#### Databases and connectors
[![Postgres](https://img.shields.io/badge/Postgres-17-%23316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![QDrant](https://img.shields.io/badge/Qdrant-1.12.5-red.svg?style=flat&logoColor=white)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6-%234ea94b.svg?logo=mongodb&style=flat&logoColor=white)](https://www.mongodb.com)
[![Redis](https://img.shields.io/badge/Redis-6.2-DC382D?logo=Redis&logoColor=white)](https://redis.io/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22-violet?style=flat&logoColor=white)](https://sqlmodel.tiangolo.com/)
[![Beanie](https://img.shields.io/badge/Beanie-1.27.0-red?style=flat&logoColor=white)](https://beanie-odm.dev/)

#### Data Modelling
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json&logoColor=white&labelColor=grey)](https://pydantic.dev)

#### AI Frameworks
[![Langchain](https://img.shields.io/badge/Langchain-0.3.4-red?style=flat&logoColor=white)](https://www.langchain.com/)

#### Linter
[![Ruff](https://img.shields.io/badge/ruff-0.7.2-41B5BE?style=flat&logoColor=white)](https://docs.astral.sh/ruff/)

#### Static code analysis
[![MyPy](https://img.shields.io/badge/mypy-1.13.0-blue?style=flat)](https://mypy-lang.org/)

#### Docs
[![Sphinx](https://img.shields.io/badge/Sphinx-8.1.3-F7C942?style=flat&logo=sphinx&logoColor=white)](https://www.sphinx-doc.org/en/master/)

## Project description

This project is intended to be as a template for an API microservice, with connectors to multiple databases.
Users have the possibility to perform simple CRUD operations on different databases.

The code adopts and implement the following patterns or protocols:

- the code is organized following Clean Architecture principles
- the code implements and use [Result Pattern](https://www.milanjovanovic.tech/blog/functional-error-handling-in-dotnet-with-the-result-pattern) approach
- [Json Patch](https://datatracker.ietf.org/doc/html/rfc6902) standard is adopted for managing PATCH requests


## Install dependencies 

In order to run the project, you need to install _UV_ first.

On Linux and MacOS environments, launch the following command:

```shell
curl -LsSf https://astral.sh/uv/0.5.6/install.sh | sh
```

On Windows environments, launch the following command.

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.5.6/install.ps1 | iex"
```

After _UV_ has been installed, you are ready to install project dependencies:

```shell
uv sync 
```

## Launching the application

In order to launch the entire application (server, databases, models), you need to install Docker.
After Docker has been installed and launched, run the following command from project root:

```shell
docker compose up
```

If you want to start the server locally, launch the following command:

```shell
python main.py
```

## Code quality

To perform code linting (e.g. remove unused dependencies and similar) launch the following command:
```shell
ruff check --fix
```

To format the code, launch the following command:

```shell
ruff format 
```

## Docs

To create documentation for this microservice, run the following command:

```shell
docs/make html
```

To remove outdated documentation files, run the command:

```shell
docs/make clean
```

## TODOs

- using Keycloak for requests authorization
- using Redis as a cache for incoming requests