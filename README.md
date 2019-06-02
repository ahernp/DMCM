# dmcm

Django Markdown Content Manager

Inspired by [TiddlyWiki](https://tiddlywiki.com/) and based on the Django implementation
of my personal website [ahernp.com](http://ahernp.com), this is a Django project
meant to be run locally using a `docker-compose` file to manage my notes and files.

The text content is written in [markdown](https://daringfireball.net/projects/markdown/syntax).

Tested on Ubuntu 18.04.

## Setup

1. Make a copy of this project: `git clone https://github.com/ahernp/dmcm.git`
1. Create a `.env` file in the root directory of the project with the following structure:

        DJANGO_SECRET_KEY=
        DMCM_DATABASE_NAME=
        DMCM_DATABASE_USER=
        DMCM_DATABASE_PASSWORD=
        POSTGRES_PASSWORD=

1. In the root directory of the project run: `docker-compose up`
1. In another terminal run:
   1. Create database: `docker-compose exec db createdb -U postgres dmcm`
   1. In `docker-compose exec db psql -U postgres dmcm`:
      1. `CREATE USER dmcm WITH PASSWORD 'database password from .env';`
      1. `GRANT ALL PRIVILEGES ON DATABASE dmcm to dmcm;`
      1. `ALTER USER dmcm CREATEDB;`
      1. `CREATE DATABASE test_dmcm;`
      1. `GRANT ALL PRIVILEGES ON DATABASE test_dmcm to dmcm;`
      1. `DROP DATABASE test_dmcm;`
   1. In `docker-compose exec webapp bash`:
      1. `python manage.py makemigrations core pages timers`
      1. `python manage.py migrate`
      1. `python manage.py loaddata project/fixtures/initial.json`
      1. `python manage.py collectstatic`
      1. Create `admin` user: `python manage.py createsuperuser`
1. Access dmcm at: http://localhost:4313
