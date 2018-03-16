Automator
==========================

[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)
[![Requires.io](https://requires.io/github/mtchavez/python-package-boilerplate/requirements.svg?branch=master)](https://requires.io/github/mtchavez/python-package-boilerplate/requirements?branch=master)

:fire: Data cleaning made easy

80% of data scientists' time is spent finding, cleansing and organizing data, which leaves only 20 percent to actually perform analysis. Keep a pipeline of SQL statements in a Postgres table that can be automatically called to clean data.

You get:

- Easy management for everyone on your team from engineering to product to marketing
- Table for organizing SQL queries from category to order (rank) to status (ex: Draft, Live, etc.)
- Log of every time the SQL queries are run

Battle-tested at [Keel](https://www.keel.io), where it's categorized over $700 million in user transactions.

## Installation

The latest stable release (and older versions) can be installed from PyPI:

```sh
pip install automator
```

And run:

```sh
python
from automator import Cleaner
myAutomator = Cleaner('postgres://database_username:database_password@database_url:5432/database_name')
# Creates two tables (automator_queries and automator_logs)
myAutomator.runInstaller()
```

If you wish to uninstall, run:

```sh
python
from automator import Cleaner
myAutomator = Cleaner('postgres://database_username:database_password@database_url:5432/database_name')
myAutomator.runUninstaller()
```

## Usage

Execute the SQL queries that have a status of 'Live' ordered by 'rank':

```python
from automator import Cleaner
myAutomator = Cleaner('postgres://database_username:database_password@database_url:5432/database_name')
# All Queries
myAutomator.runQueries()
# Queries with a category of 'Users'
myAutomator.runQueries('Users')
```

To save an SQL query (Web UI coming Soon):

```sql
INSERT INTO public.automator_queries (code, rank, status, category)
VALUES ('DELETE FROM users WHERE email ILIKE ''%test.com''', 1, 'Draft', 'Users');
```

To update an SQL query (Web UI coming Soon):

```sql
UPDATE automator_queries
SET status = 'Live'
WHERE id = 1;
```

### Automator_queries

Queries are stores in your database with the following fields.

- **id** - primary key
- **title**
- **category**
- **description**
- **status** - automator_queries are only run if they have a status of 'Live'
- **code**
- **created_at**
- **updated_at**
- **rank** - ascending integers

### Automator_logs

When you run your SQL queries, Automator creates a log with useful information (more details coming soon).

- **category**
- **start_time**
- **end_time**
- **error**

## Security

It's a great practice to create a separate Postgres user that Automator uses. Once created, you can restrict which tables it has access to (see tutorial)[https://www.tutorialspoint.com/postgresql/postgresql_privileges.htm].

## Package

Basic structure of package is

```
├── README.md
├── automator
│   ├── __init__.py
│   ├── Cleaner.py
│   └── version.py
├── pytest.ini
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    ├── fixtures
    │   ├── state_1-5.py
    ├── helpers
    │   ├── __init__.py
    │   └── my_helper.py
    ├── tests_helper.py
    └── unit
        ├── __init__.py
        ├── test_cleaner.py
        └── test_version.py
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

## Travis CI

There is a ```.travis.yml``` file that is set up to run your tests for python 2.7
and python 3.2, should you choose to use it.
