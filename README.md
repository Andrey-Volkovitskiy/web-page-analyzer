# Web page analyzer

**This is the 3rd training project of the Hexlet "Python Developer" course.**

Flask app that analyzes web pages for basic SEO suitability.

Deployed at: https://web-page-analyzer.up.railway.app/

---
### Hexlet tests and linter status:
[![Actions Status](https://github.com/Andrey-Volkovitskiy/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-project-83/actions)    [![Lint](https://github.com/Andrey-Volkovitskiy/python-project-83/actions/workflows/flake8_linter.yml/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-project-83/actions/workflows/flake8_linter.yml)    [![Pytest (with postgres)](https://github.com/Andrey-Volkovitskiy/python-project-83/actions/workflows/pytest_with_postgres.yml/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-project-83/actions/workflows/pytest_with_postgres.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/b8dd81abde1b444e80e2/maintainability)](https://codeclimate.com/github/Andrey-Volkovitskiy/python-project-83/maintainability)    [![Test Coverage](https://api.codeclimate.com/v1/badges/b8dd81abde1b444e80e2/test_coverage)](https://codeclimate.com/github/Andrey-Volkovitskiy/python-project-83/test_coverage)


---
This project was built using these tools:

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [Flask](https://flask.palletsprojects.com/)         | Micro web framework  |
| [Jinja2](https://jinja.palletsprojects.com)         | Web template engine  |
| [PostgreSQL](https://www.postgresql.org)         | Database management system  |
| [Beautiful Soup](www.crummy.com/software/BeautifulSoup/)       | HTML parsing package  |
| [Docker](https://www.docker.com)       | Container-based platform for building apps  |
| [Poetry](https://poetry.eustace.io/)         | Python dependency manager  |
| [Pytest](https://docs.pytest.org/)               | Testing framework |
| [Flake8](https://flake8.pycqa.org/)               | Linter to check code style |
| [Code Climate](https://codeclimate.com/)               | Clean Code verification system |
| [Github Actions](https://github.com/features/actions)               | Continuous Integration (CI) |
| [Railway](https://railway.app)               | Ddeployment platform |


---
### Installation and running

The application stores data using PostgresSQL. The database schema is described in *database.sql*

- *make install* - comand to install dependencies
- *make start* - command to start the application
