# BMC submission system

*Created on 19.05.2025, by Emre Kavur*\
*Last updated on 22.05.2025, by Emre Kavur*

This project is designed to create the challenge submission system for challenges organized in MICCAI conferences. It has two main layers: frontend and backend.

NOTE: This README covers development, deployment and maintenance of the project. If you are looking for documentation for how to use the system, please refer: [User Manual](./docs/UserManual.md).

### Table of contents: <!-- omit in toc --> <!-- omit from numbering -->
<!-- TOC tocDepthFrom:2 tocDepthTo:5 chapterDepthFrom:2 chapterDepthTo:6 anchorMode:gitlab -->

- [1. Workflow](#1-workflow)
    - [1.1. Project folder structure](#11-project-folder-structure)
- [2. Setting up the development environment](#2-setting-up-the-development-environment)
- [3. Project management](#3-project-management)
    - [3.1.  Backend management](#31-backend-management)
        - [3.1.1. Installing Python 3.13 and uv](#311-installing-python-313-and-uv)
        - [3.1.2. Installing the backend](#312-installing-the-backend)
    - [3.2. Frontend management](#32-frontend-management)
        - [3.1.1. Installing Node.js 22 LTS](#311-installing-nodejs-22-lts)
        - [3.1.2. Installing the frontend](#312-installing-the-frontend)
- [4. Running `bmc-submission-system` project](#4-running-bmc-submission-system-project)
    - [4.1. Running backend (`BMC_API` module)](#41-running-backend-bmc_api-module)
    - [4.1.1 Running Redis server](#411-running-redis-server)
    - [4.1.2 Running the main FastAPI app](#412-running-the-main-fastapi-app)
    - [4.1. Running frontend](#41-running-frontend)
- [5. Dependency management of the project](#5-dependency-management-of-the-project)
    - [5.1. Backend](#51-backend)
    - [5.2. Frontend](#52-frontend)
- [6. Development of the project](#6-development-of-the-project)
    - [6.1. Backend](#61-backend)
        - [6.1.1. Settings](#611-settings)
        - [6.1.2. Server workers](#612-server-workers)
            - [6.1.2.1. Uvicorn](#6121-uvicorn)
            - [6.1.2.2. Gunicorn with Uvicorn Worker Class](#6122-gunicorn-with-uvicorn-worker-class)
            - [6.1.2.3. Selecting the server](#6123-selecting-the-server)
        - [6.1.3. Database](#613-database)
            - [6.1.3.1. Creation of the database](#6131-creation-of-the-database)
            - [6.1.3.2. Accessing database via ORM](#6132-accessing-database-via-orm)
            - [6.1.3.3. Updating database tables with migrations](#6133-updating-database-tables-with-migrations)
        - [6.1.4. Endpoints](#614-endpoints)
        - [6.1.5. Pre-commit](#615-pre-commit)
        - [6.1.6. Logging](#616-logging)
    - [6.1.7. Global rate limiter](#617-global-rate-limiter)
        - [6.1.8. Running tests](#618-running-tests)
            - [6.1.8.1. Test configurations](#6181-test-configurations)
            - [6.1.8.2. Test files](#6182-test-files)
            - [6.1.9 Shared folders](#619-shared-folders)
    - [6.2. Frontend](#62-frontend)
        - [6.2.1. Development](#621-development)
        - [6.2.2. Useful commands](#622-useful-commands)
            - [6.2.3 Shared folders](#623-shared-folders)
- [7. Deployment](#7-deployment)
    - [7.1. Checks before deployment](#71-checks-before-deployment)
    - [7.2. Docker compose services](#72-docker-compose-services)
    - [7.3. Docker Compose volumes](#73-docker-compose-volumes)
    - [7.4. Docker Compose networks](#74-docker-compose-networks)
    - [7.5. Deploying the project to server](#75-deploying-the-project-to-server)

<!-- /TOC -->

## 1. Workflow

```
                         FRONTEND                            BACKEND
                   ┌──────────────────┐        ┌────────────────────────────────────────────────────────┐
┌──────────┐       │                  │        │ ┌─────────────┐       ┌──────────┐                     │
│   User   │       │                  │        │ │Gunicorn WSGI│       │          │       ┌─────────┐   │
│ Requests │ ◄───► │ nginx web-server │ ◄───►  │ │with Unicorn │ ◄───► │ FastAPI  │ ◄───► │  Redis  │   │
└──────────┘       │                  │        │ │workers      │       │   App    │       └─────────┘   │
                   │                  │        │ └─────────────┘       │          │                     │
                   └──────────────────┘        │                       └──────────┘                     │
                                               └────────────────────────────────────────────────────────┘

```

The ports 80 (HTTP) and 443 (HTTPS) are being listened by Nginx server. All requests from HTTP port are forwarded to HTTPS by default. Then the requests are passed to Gunicorn WSGI to 0.0.0.0:5000 address. Gunicorn interacts with the FastAPI application, and responses are forwarded through 0.0.0.0:5000 to Nginx. Nginx forwards the answer to user.

**Here some quick information about technologies under the hood:**

- Backend has been developed with Python version 3.13. Backward compatibility has not been tested and is not guaranteed. Please use Python 3.13 or newer.

- The backend has been developed on [FastAPI](https://fastapi.tiangolo.com/) . See [Development of project](#6-development-of-the-project) section for more information.

- [uv](https://docs.astral.sh/uv/) is used for backend project and dependency management. See [Backend management](#31-backend-management) section for more information.

- [SQLite](https://www.sqlite.org/) is used for database with [SQLAlchemy](https://www.sqlalchemy.org/) as ORM and [Alembic](https://alembic.sqlalchemy.org) as migration manager. See [Database](#613-database) section for more information. 

- The frontend has been developed on [Vue.js](https://vuejs.org/) with [Vite](https://vite.dev/) build tool. Project is managed by [Node.js](https://nodejs.org/) v22 See [Development of frontend](#62-frontend) and See [Frontend management](#32-frontend-management) sections for more information. 

- Project deployment is handled by [Docker](https://www.docker.com/) containers. [Docker Compose](https://docs.docker.com/compose/) is used for controlling deployment with multiple containers. All scripts and settings are located `deploy/` folder. See [Deployment](#7-deployment) section for more information.

- Project is served via [Nginx](https://www.nginx.com/) server as reverse proxy. Also the built frontend files are hosted by Nginx. See [Docker compose services](#73-docker-compose-services) section under Deployment for more information.

All development was handled in Ubuntu Linux operating system. It is also possible to develop under other operating system, but a Linux based system is recommended.

### 1.1. Project folder structure
Important files and folders:

```bash
$ tree -d -L 2 "bmc-submission-system"
bmc-submission-system
├── backend # Backend module folder
│   └── BMC_API # Codes for FastAPI application.
├── deploy # Deployment configs
├── docs
├── frontend # Frontend module folder
│   ├── dist # Build applications files for deployment. These files are uploaded to /opt/BMC/www path on sever during deployment
│   ├── node_modules # Node.js modules install folder. Created and managed automatically by Node.js.
│   ├── public
│   └── src # Files for Vue.js application
└── nginx # Nginx server configuration for reverse proxy settings and hosting frontend
    ├── certs
    └── logrotate
```
There are also some other dot files/folders for additional tool configs such as `.gitignore`, `.dockerignore`, `.flake8`, etc.


## 2. Setting up the development environment
The repo is managed by Git. Just pull the repo to begin. It is recommended to use develop branch for developing. 

Any IDE can be used for development and debugging. 

## 3. Project management

### 3.1.  Backend management
This project uses [uv](https://docs.astral.sh/uv/) for management. It's a modern and extremely fast dependency management tool for Python projects. It manages virtual environments, dependencies, package version conflicts, version control, building project and publishing. All settings and package information are stored in the `pyproject.toml` file.

Before starting, uv must be installed on your development machine.

#### 3.1.1. Installing Python 3.13 and uv
If it is not installed in your system, install Python 3.13. Then install uv by following official docs:

https://docs.astral.sh/uv/getting-started/installation/


#### 3.1.2. Installing the backend

These main requirements that need to be installed: `Docker Desktop`, `BMC_API`.

**Installing Docker Desktop** 

Please follow the instructions for your operating system at https://docs.docker.com/get-docker/ This will install Docker Compose along with Docker Engine and Docker CLI 


**Installing `BMC_API` module**

The project must be installed once. Change directory to `bmc-submission-system/backend` and just run the following code:
```bash
$ uv sync
```
This will create/update `uv.lock` file, create a new virtual environment under `.venv` folder and install all dependencies.

### 3.2. Frontend management


#### 3.2.1. Installing Node.js 22 LTS
If it is not installed in your system, install Node.js with minimum version of 22 via https://nodejs.org/en/download


#### 3.2.2. Installing the frontend

The frontend must be installed once. Change directory to `bmc-submission-system/frontend` and just run the following code:

```sh
npm install
```
This will create/update `package-lock.json` file, create necessary files `node_modules` folder  and install all dependencies.

## 4. Running `bmc-submission-system` project
The frontend and backend modules below should be run together for full development. Optionally, they can be run alone if only one of them is developed.


### 4.1. Running backend (`BMC_API` module)

### 4.1.1 Running Redis server
Redis server must be run **before** `BMC_API` module. It serves as a caching database for `user/logout` and `user/refresh_token` endpoints. If you won't use/test these services, it is not obligatory to run Redis service in the development environment.

The easiest way to run Redis in its official Docker container without installing anything else on your system:
```bash
$ docker run --name redis -d -p 6379:6379 redis:7-alpine
```

### 4.1.2 Running the main FastAPI app
There are multiple ways of running the module. Open a new terminal in `bmc-submission-system/backend` directory, run the following command first:

```bash
uv run alembic upgrade "head"
```
This will prepare the database for first run. Please refer [Database](#613-database) section.

Then run the module:
```bash
$ uv run python -m BMC_API
```

This will start the server on the configured host.

Alternatively, you can switch to the virtual environment shell and run the project there:

```bash
$ source .venv/bin/activate
$ python -m BMC_API
```
After using any of the running methods, there should be similar outputs in the terminal:
```bash
INFO: Will watch for changes in these directories: ['/bmc-submission-system/backend']
INFO: Uvicorn running on http://localhost:5000 (Press CTRL+C to quit)
INFO: Started reloader process [3274458] using WatchFiles
[2025-05-20T10:41:48.423655+0200 | INFO | logging:callHandlers:1736 - Started server process [3274484]]
[2025-05-20T10:41:48.424476+0200 | INFO | logging:callHandlers:1736 - Waiting for application startup.]
[2025-05-20T10:41:48.424678+0200 | INFO | logging:callHandlers:1736 - Application startup complete.]
```
These outputs mean that the project is running without any problems.

### 4.1. Running frontend
Open a new terminal in `bmc-submission-system/frontend` directory, run the following command:

```sh
npm run dev
```

This will start the server on the configured host. Th frontend module will listen the api address defined in `frontend/src/api/axios.js` file.

## 5. Dependency management of the project

### 5.1. Backend
You can add, remove, update packages using uv.

Add a dependency:
```bash
$ uv add <DEPENDENCY_NAME>
```
Here DEPENDENCY_NAME is the project name at https://pypi.org/.

Remove a dependency:
```bash
$ uv remove <DEPENDENCY_NAME>
```

Get the latest versions of the dependencies and to update the uv.lock file:
```bash
$ uv lock --upgrade
```
This will update dependencies according to defined version numbers or ranges in `pyproject.toml` file. For more information about dependency specifiers: https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers

If you just want to update a few packages and not all:
```bash
$ uv lock --upgrade <PACKAGE_NAME>
```

List all the available packages with versions:
```bash
$ uv pip list
```

There are many other useful commands in uv. For more information, see: https://docs.astral.sh/uv/reference/cli/

### 5.2. Frontend

You can add, remove, update packages using uv.

Add a dependency:
```bash
$ npm install <DEPENDENCY_NAME>
```
Here DEPENDENCY_NAME is the project name at https://www.npmjs.com/

Remove a dependency:
```bash
$ npm uninstall <DEPENDENCY_NAME>
```

Get the latest versions of the dependencies and to update the package-lock.json file:
```bash
$ npm update --save
```
This will update dependencies according to defined version numbers or ranges in `package.json` file. For more information about dependency specifiers: https://docs.npmjs.com/about-semantic-versioning

If you just want to update a few packages and not all:
```bash
$ npm update <PACKAGE_NAME>
```

List all the installed packages with versions:
```bash
$ npm list
```
To fix issues about packages this is very useful:

```bash
$ npm audit fix --force
```

There are many other useful commands in Node.js. For more information, see: https://docs.npmjs.com/


## 6. Development of the project

### 6.1. Backend 

All development files are located in `bmc-submission-system/backend` folder. The backend layers is designed following Onion Architecture. This is a layered approach with the domain/business logic at the core, insulated from external frameworks and tools. It separates of concerns between business logic and technical details. Domain and application logic are isolated from external details, they can be unit-tested easily.

Here is the brief overview of folder structure:

**Folder structure:** 
```bash
backend
├── BMC_API
│   ├── __main__.py
│   ├── backups # Created database backups. It is bound to the remote folder on the deployment server.
│   ├── database # Main database file. It is bound to the remote folder on the deployment server.
│   ├── logs # Logs folder for backend service. It is bound to the remote folder on the deployment server.
│   ├── outputs # Folder for created proposal PDF files. It is bound to the remote folder on the deployment server.
│   ├── src
│   │   ├── api #-> Configurations for API level. 
│   │   │   ├── application.py # FastAPI application declaration
│   │   │   ├── dependencies # Useful functions for serving along the app
│   │   │   ├── exception_handlers.py
│   │   │   ├── gunicorn_runner.py # Configuration for gunicorn server with custom uvicorn workers.
│   │   │   ├── middleware # Custom middlewares for FastAPI app
│   │   │   ├── routes # Entrypoint for endpoint addresses
│   │   │   └── schemas # Schemas for base models
│   │   ├── application #-> Configurations for application level. 
│   │   │   ├── dependencies.py # Additional dependencies for injections
│   │   │   ├── dto # Data Transfer Objects, inherited from base schemas 
│   │   │   ├── interfaces # Interfaces for recursively used dependencies
│   │   │   └── use_cases # All classes for application level operations
│   │   ├── core # -> Core application settings
│   │   │   ├── config # Main configuration settings for project.
│   │   │   ├── exceptions
│   │   │   ├── lifetime.py # Startup/Shutdown actions, cron jobs, repeated events
│   │   │   └── logging # Configuration settings for logging.
│   │   ├── domain # -> Settings for domain level, mainly database related settings, ORM models (SQLAlchemy)
│   │   │   ├── entities # All ORM models (SQLAlchemy)
│   │   │   ├── interfaces
│   │   │   ├── repositories # Protocols for classes at application/use_cases
│   │   │   ├── services
│   │   │   └── value_objects # Objects for database models, mainly enums
│   │   ├── infrastructure # -> Settings for infrastructure objects, meta data
│   │   │   ├── external_services
│   │   │   ├── messaging
│   │   │   └── persistence # Meta data for ORM models, dependencies, utils
│   │   │       ├── dao # Classes/functions for each database model
│   │   │       └── migration # Migrations managed by Alembic
│   │   └── initial_data.py # Initial data(initial admin, etc.) while database is created from starch.
│   │── tests # Pytests for project.
│   └── .env # File for critical variables. NOT INCLUDED in repo. Obtain it from project managers
├── Dockerfile # Docker image configuration
├── alembic.ini # Configurations for Alembic (database migration tool)
├── pyproject.toml # Python project settings file that includes dependencies, settings for uv, linting, formatting, etc.
├── uv.lock # File will be created/managed by uv, don't edit manually
└── .venv # Folder will be created by uv when the project initialized
```

The modules are located into "application", "infrastructure", "domain", "api" and "core" folders.

- `core/`: Contains pure business logic.
- `infrastructure/`: Contains ORM configs, metadata, migrations, external_services.
- `application/`: Contains Service/Use-case, DTO's.
- `domain/`: Contains ORM models (SQLAlchemy).
- `api/`: FastAPI endpoints, deals with HTTP request/response handling.

#### 6.1.1. Settings
Project settings can be managed in three ways: settings.py file, `.env` file and Docker compose settings. Settings are managed by the [`pydantic_settings`](https://github.com/pydantic/pydantic-settings) package. The setting priority of these methods is `Docker compose` > `.env` file > `settings.py`. 

**IMPORTANT NOTE:** `.env` file contains most critical variables. Therefore it is not included in the repo. Please obtain the file from project maintainers then locate it at `bmc-submission-system/backend/BMC_API/.env` Otherwise, the app will raise error. Also, never expose file at somewhere else!

All environment variables in `.env` file should start with *BMC_API_* prefix. For example if you see in your "backend/BMC_API/src/core/config/settings.py" a variable named like `random_parameter`, you should provide the "BMC_API_RANDOM_PARAMETER" variable to configure the value.

An example of .env file:

```bash
BMC_API_RATE_LIMIT="4/second"
BMC_API_DB_FILE_BACKUP_PERIOD_IN_SEC = 86400 
BMC_API_DB_FILE_BACKUPS_CLEAN_PERIOD_IN_SEC = 86400
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

During server startup, the `get_settings()` function in `settings.py` is called. First values in `settings.py` file are passed, then settings in `.env` imported. If the project is in the deployment stage, additional settings defined in the `deploy/docker-compose.yml` file are parsed. These values have the highest priority and will override previous settings with the same name. Again, preference names start with the prefix *BMC_API_*. See the *Deployment* section for more information.

#### 6.1.2. Server workers
The `BMC_API` module is started from the `backend/BMC_API/__main__.py` file. This file runs the `Uvicorn` or `Gunicorn` (with Uvicorn workers) server. The choice of server type is based on debugging and operating system. Here is the brief information about these two configurations:

##### 6.1.2.1. Uvicorn
[Uvicorn](https://www.uvicorn.org/) is an ASGI webserver implementation for Python. Since FastAPI is an [ASGI](https://asgi.readthedocs.io/en/latest/) web framework, Uvicorn is the default server that comes with the FastAPI package. The main disadvantage of Uvicorn is that it runs as a single process. [Hypercorn](https://pgjones.gitlab.io/hypercorn/) and [Daphne](https://github.com/django/daphne) are two other alternatives for Unicorn, but they are not preferred in this project.

##### 6.1.2.2. Gunicorn with Uvicorn Worker Class
Gunicorn is primarily an application server that uses the WSGI standard. The biggest advantage of Gunicorn is that it supports acting as a process manager and allowing users to tell it which specific worker process class to use. Gunicorn would then start one or more worker processes using that class.

Gunicorn is not compatible with FastAPI because FastAPI uses the latest [ASGI standard](https://asgi.readthedocs.io/en/latest/). However, there is a way to use Gunicorn with FastAPI. The Uvicorn worker class is compatible with Gunicorn. In other words, we can use Gunicorn server with Uvicorn worker class. In this configuration, Gunicorn would be the process manager listening on the IP and port, the replication would be done by having multiple Uvicorn worker processes. This will make the server response faster when multiple users are using the system.

##### 6.1.2.3. Selecting the server
- **Development stage:** On your local machine, when the `BMC_API` module is started via the `$ uv run python -m BMC_API` command as explained before, the decision of the server configuration is handled automatically.  If `settings.reload` is *True* or the operating system is Windows, the module will be run via Uvicorn. Enabling `settings.reload` is a very useful feature during development and debugging and only supported by Uvicorn, not Gunicorn. The reason for using Uvicorn on Windows is that the Gunicorn server is not compatible with Windows operating systems because it depends on some features in Unix-like kernels.

- **Deployment stage:** When deploying to the server, Gunicorn is the main server configuration to take advantage of using multiple worker processes. See the [Deployment](#7-deployment) section for more information.

#### 6.1.3. Database
SQLite is a lightweight, embedded, file-based database system that stores data in a single disk file. It's a C-based, open-source relational database management system (RDBMS) that doesn't require a separate server process, making it suitable for applications that need a simple, self-contained database solution. Python has a native support for SQLite with sqlite3 library. However, it is necessary to use an ORM and migration tools since the necessity of the broad operations.

SQLAlchemy is an open-source Python library that provides an object-relational mapper (ORM) for interacting with databases. It enables developers to work with databases using Python objects, providing efficient and flexible access.

Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. Main config for Alembic is at `backend/alembic.ini` fie. Here script_location defined at `BMC_API/src/infrastructure/persistence/migrations`. All migration and version scripts are kept here.

##### 6.1.3.1. Creation of the database
If there is no database on `backend/BMC_API/database`, a new one must be created. 

Locate to `backend/` folder then run:
```bash
uv run alembic revision --autogenerate
```

It will call from BMC_API.src.domain.entities.load_all_models function to load all models locate n `backend/BMC_API/src/domain/entities`. Then it will detect changes automatically if there is any. Finally it will create migration file(s) on ./migrations folder. After that run:
```bash
uv run alembic upgrade "head"
```
This will create a new database file if there isn't any and perform all pending migrations.

##### 6.1.3.2. Accessing database via ORM
All database operations are handled from the classes and functions located at `backend/BMC_API/src/infrastructure/persistence/dao` folder.
`base_dao.py` contains most of the basic operations while other dao classes holds extra operations for specific services. 

All operations are handled by build-in SQLAlchemy functions. Please refer [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/) for more details.

##### 6.1.3.3. Updating database tables with migrations
To handle migrations, the changes between ORM models and their state in actual database must be detected. For automatic change detection, locate to `backend/` folder then run:

```bash
uv run alembic revision --autogenerate
```
It will create new migration file(s) on ./migrations folder if there is a change detected.

The second stage is to perform pending migrations. To run all migrations:
```bash
uv run alembic upgrade "head"
```
This will execute all migration scripts on ./migrations folder.

To run specific migration:
```bash
uv run alembic upgrade "<revision_id>"
```

If going back to previous revision for a reason (for example a malfunction, or a bug) desired, it is possible via:
```bash
uv run alembic downgrade "<revision_id>"
```

It is also possible to revert all migrations (be careful):
```bash
uv run alembic downgrade base
```

#### 6.1.4. Endpoints

All endpoints can be listed from <host_name>/api/docs address. This address and statistics endpoints are open, but can be password protected on production stage at the server with configuration located `nginx/Dockerfile`. 

All endpoints are managed in `backend/BMC_API/src/api/routes/router.py` file. The usage of endpoints are explained at [User Manual](./docs/UserManual.md)


#### 6.1.5. Pre-commit
[Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks. pre-commit is very useful to check your code before publishing it. 

To install pre-commit simply run inside the shell:

```bash
$ pre-commit install
```
In this project, it's configured using `.pre-commit-config.yaml` file.

By default it runs:

-   ruff (formats your code);
-   mypy (validates types);
-   flake8 (spots possible bugs);

The stricter version of this hook can be found in `.pre-commit-config.yaml.old` file.

You can read more about pre-commit here: https://pre-commit.com/


#### 6.1.6. Logging
All logs are collecting in `backend/BMC_API/logs/` folder as .log files. Logging  for `BMC_API` module is handled by [Loguru](https://github.com/Delgan/loguru) library. Loguru makes logging management really simple comparing with Python’s built-in logging module. All sinks added to the logger are thread-safe by default.

Here logging settings are managed in `backend/BMC_API/src/core/logging/logging.py` file. Logging handler, log record formatting, integrating handler for default uvicorn logger, and other settings are set in here.

Log files of `BMC_API` module are rotated daily. In other words, there are individual log files for each day to organize them easier. The current log file is `api_logs.log`, while rotated file names are `api_logs.YYY-MM-DD_HH-MM.log`.

Logger retention period of the logs is "3 months". That means, older logs than 3 months are deleted periodically.

### 6.1.7. Global rate limiter 
There is a global rate limiter defined to protect from bots, or applications that are over-using or abusing. [SlowApi](https://slowapi.readthedocs.io/en/latest/api/) library is used for this feature. The configurations are defined in `backend/BMC_API/src/api/application.py` file at *# Add global rate limiter* section of the file. The limit is 4 request per second which can be changed via `rate_limit` parameter in `.env` file. 

When the rate limit is exceeded, 429_TOO_MANY_REQUESTS error is returned.

#### 6.1.8. Running tests
As a testing framework, [pytest](https://docs.pytest.org/en/) v8 is used. Pytest is selected because of for its simplicity, scalability, and powerful features such as fixture support and parameterization.

##### 6.1.8.1. Test configurations
The main test configuration is stored in `backend/BMC_API/tests/conftest.py` file. Here fixtures are defined for `anyio_backend`, `fastapi_app` and `client`. These fixtures can be directly used in test functions. Assume a test file called *test_something.py* in `tests` folder. The content of the file can be such that:

```python
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

@pytest.mark.anyio
async def test_some_page(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the endpoint for some_page.

    :param client: client for the app. It comes from the fixture defined in conftest.py
    :param fastapi_app: current FastAPI application. It comes from the fixture defined in conftest.py
    """
    url = fastapi_app.url_path_for("some_page")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
```
Here, there is no need to import `fastapi_app` and `client` because pytest first import all fixtures from `conftest.py` while it is initializing.

##### 6.1.8.2. Test files
The tests files/functions are located at `backend/BMC_API/tests` folder. To execute all tests, simple run the pytest in `backend/BMC_API` folder:

```bash
$ pytest -vv .
```
This will execute all tests. You can use `-s` option to sent output of print() functions to stdout `$ pytest -s -vv .`

You can use options for the coverage of the tests. For example, to generate coverage reports as terminal report with line numbers, use this:

```bash
$ pytest --cov-report term-missing --cov=./ .
```

For coverage reports as HTML pages, use this:

```bash
$ pytest --cov-report html --cov=./ .
```
This will create a fancy HTML report page under htmlcov/ folder in root folder.


You can combine all options:  `$ pytest -vv -s --cov-report html --cov=./ .` (Recommended to use this one)

Please see pytest docs for more information.

##### 6.1.9 Shared folders
`database`, `backups`, `outputs`, `logs` folders are bounded related folders on remote server. See [7.4. Docker Compose volumes](#74-docker-compose-volumes) for more information

### 6.2. Frontend 

Frontend part of the project has been developed on [Vue.js](https://vuejs.org/) with [Vite](https://vite.dev/) build tool. 

- `frontend/dist` folder keeps built and production ready files. Created automatically when project is built.
- `frontend/node_modules` keeps dependencies. Created automatically when project is installed.
- `frontend/src` keeps source codes. This is the place where development is handled.

**Customize configuration**
You can configure project with the files below:

- `frontend/package.json`
- `frontend/vite.config.js`

See [Vite Configuration Reference](https://vitejs.dev/config/).

#### 6.2.1. Development
Before start deployment, you need to temporarily change base API url setting at `frontend/src/api/axios.js`. For the development, the value must be same as address of backend module, such as *'http://localhost:5000/api/'* DO NOT FORGET to change it back before building and deploying project.

- Main codes for pages can be found at `frontend/src/views`
- Data management for both surveys can be found at `frontend/src/stores`
- Multiuse components can be found at `frontend/src/components`
- Router settings can be found at `frontend/src/router/index.js`
- Static files can be found at `frontend/src/assets`
- Additional style settings can be found at `frontend/src/style`

#### 6.2.2. Useful commands
- Project Setup: `npm install`. Run once when initializing project.
- Compile and Hot-Reload for Development: `npm run dev`. Run during development.
- Compile and Minify for Production: `npm run build`. Run just before deploying project.
- Lint with [ESLint](https://eslint.org/): `npm run lint`

##### 6.2.3 Shared folders
`www` folders are bounded related folder on remote server. See [7.4. Docker Compose volumes](#73-docker-compose-volumes) for more information

## 7. Deployment
Deployment is managed from a single point using [Docker Compose](https://docs.docker.com/compose/). The main configuration file is `deploy/docker-compose.yml`, where all services, volumes, and network settings are managed.

### 7.1. Checks before deployment
1. Please run tests prior to any deployment and make sure that all tests have been passed. Don't forget to change `baseURL` in `frontend/src/api/axios.js` file. Then push code of the release candidate version to master branch, then start deployment procedure.

2. Complete missing fields in `deploy/docker-compose.yml` file such as volume configurations. These values are specific to production server.

3. Do NOT forget to change the correct base API url setting at `frontend/src/api/axios.js` before building and deploying the frontend. The value must be *'https://www.biomedical-challenges.org/api/v2/'*

4. If there isn't any, create missing certificate files into `nginx/certs` folder. The name of the files must be same as defined in `nginx/project.conf` file.


### 7.2. Docker compose services
 These are the services defined in the `deploy/docker-compose.yml` file:

- The `bmc-api` service uses the docker image defined in `backend/Dockerfile`. This image has multistage building. The `builder` image uses `python:3.13-bookworm`. First uv is installed, then uv install project with all dependencies. Then `production` image uses python:3.13-slim-bookworm as base image. Then it copies all necessary files from `builder` image.

- The `server` service manages [Nginx](https://www.nginx.com/) reverse proxy service that handles all network communications between all containers and the online access port. This service uses Docker image defined in `nginx/Dockerfile`. This image uses latest stable Docker image for Nginx server. Default Nginx configurations are modified via `nginx/nginx.conf` and `nginx/project.conf` files. The `project.conf` file contains all reverse proxy route information and SSL certificates.  Please be very careful when modifying any of these configuration files in this service.

- The `redis` service manages [Redis](https://redis.io/) caching database. The service is just an official Redis container built with Alpine Linux. 


### 7.3. Docker Compose volumes
There are five volume definitions: `database`, `logs`, `www`, `backups` and `outputs`. All are a kind of *bind* to local folders on the server. These local folders are `/opt/BMC/database`, `/opt/BMC/logs`, `/opt/BMC/www` and `/opt/BMC/outputs`. These defined volumes are mounted during service configuration. For example, in the `bmc-api` service, the `logs` and `database` folders are attached to the container's internal folders `/app/src/BMC_API/logs/` and `/app/src/BMC_API/database/`:
```
volumes:
    - database:/app/src/BMC_API/database/:Z 
    - logs:/app/src/BMC_API/logs/
    - outputs:/app/src/BMC_API/outputs/:Z
    - backups:/app/src/BMC_API/backups/:Z
```
`www` volume is mounted to `/opt/BMC/www` that keeps all files from frontend build located at `frontend/dist`. 

### 7.4. Docker Compose networks
`bmc-network` is defined and used by all services. There is no need for complicated settings here. Docker Compose handles all configurations automatically.

### 7.5. Deploying the project to server

Deployment contains two stages as deployment of frontend and backend. These two components can be deployed together(full stack) or separately as required. 

**Frontend deployment:** The Vue.js app must be built before deployment. Never use direct source code for deployment! Build stage optimizes the source code, compress it, removes commented lines, etc... After successful built, the ready to deploy code will be created at `frontend/dist` folder. All of these files will be uploaded to `www` volume defined in Docker Compose volumes


**Backend deployment:** It is handled by creating `bmc-api` service mentioned before. Simply, it will create necessary Python based docker images, put source code in it and run Gunicorn server. 

First we need to build the docker images with `docker compose --file docker-compose.yml --project-name "bmc-system" build` command. Then pack everything into the achieve file via `docker save bmc-api nginx_server | gzip > bmc-system.tar.gz` 

After that this single file can be uploaded to remote server, extracted here. 
```bash
docker load -i ./bmc-system.tar.gz
```
Finally Docker compose service can be run on the server:
```bash
docker compose -p "bmc-system" up -d --no-build --remove-orphans
```

If the deployment is successful, you can check status of containers via `docker container ls`. Then you will see similar messages on your terminal:

```bash
--- Project is being extracted on server ---
✔ Container bmc-system-redis-1      Started 0.5s
 ✔ Container bmc-system-redis-1     Started 1.9s 
 ✔ Container bmc-system-bmc-api-1   Started 2.3s 
 ✔ Container bmc-system-server-1    Started 1.6s 
CONTAINER ID   IMAGE                           COMMAND                  CREATED         STATUS                  PORTS                                                                                            NAMES
75cff4bb105a   nginx_server:stable             "/docker-entrypoint.…"   2 seconds ago   Up Less than a second   0.0.0.0:80->80/tcp, :::80->80/tcp, 0.0.0.0:443->443/tcp, :::443->443/tcp                         bmc-system-server-1
14af8979a7eb   bmc-api:2.0.0                   "bash -c 'alembic up…"   3 seconds ago   Up Less than a second   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                                        bmc-system-bmc-api-1
09911e9d2819   redis:latest                    "docker-entrypoint.s…"   4 days ago      Up 4 days (healthy)     0.0.0.0:6379->6379/tcp, :::6379->6379/tcp                                                        bmc-system-redis-1
356c5a4f4e8b   portainer/portainer-ce:latest   "/portainer"             11 months ago   Up 11 months            0.0.0.0:8000->8000/tcp, :::8000->8000/tcp, 0.0.0.0:9443->9443/tcp, :::9443->9443/tcp, 9000/tcp   portainer
```

