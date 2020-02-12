# LoansBot - Database

This repository contains the LoansBot initialization, migration, and backup
scripts.

## Setup for Development (Ubuntu 18.04)

Prerequesites:

- python 3.7.5 or higher
- docker

Setup your python environment:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Setup postgres:

```bash
docker pull postgres
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=dev -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
```

## Contributing

Pull requests go against the develop branch, and releases go to the master
branch.

Migrations must be named such that the order of the migrations is the
alphabetical ascending ordering of the filenames. If a migration filename
(without the suffix) is A, then the following files should exist:

- src/migrations/A.py: The main migration file, which is a module containing
  an up and down function which accept a single argument: a psycopg2 database
  cursor.
- tests/migrations/A_down.py - This should contain a `unittest.TestCase`
  that should pass before the migration is applied.
- tests/migrations/A_up.py - This should contain a `unittest.TestCase` that
  should pass after the migration is applied.

## Auto-generated Files

This script stores the current database migrations in `migrations.json`.
In order to run migrations, there must only be newer migrations (i.e.,
this will fail before doing anything if a migration was skipped).

## Automatic Actions

Releases in the master branch are automatically deployed to the
production server; specifically, the production database is migrated,
the backup scripts are updated, and the cronjob is destroyed and recreated.

The actual deploy cycle is done using AWS CodePipeline.

## Testing

Migrations are expected to be tested, and this is facilitated via GitHub
actions. There are two types of tests, one of which doesn't need per-migration
logic and one of which does.

- Migrations should not raise errors on fresh installs
  - Run src/run_migrations.py and get no errors.
- Each individual migration should have some basic up/down tests - i.e.,
  if the migration creates a table then the up test should check it doesn't
  exist and the down test should check it does and has the expected columns.
  The test for before the migration is applied should fail after the migration
  is applied, and the test after the migration is applied should fail before
  the migration is applied.
- We should be able to backup the database
  - Create backup and upload it to S3 using src/create_backup.py
  - Download the last uploaded backup using src/download_backup.py
  - Restore the downloaded backup using src/restore_from_backup.py

Pull requests to the master branch will be rejected until tests pass.
