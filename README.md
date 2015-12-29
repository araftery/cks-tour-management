## Setting Up Environment
* Clone repo
* Make a virtual environment, and then:

```
pip install -r requirements.txt
```

* Add this to your virtual environment's `postactivate` hook (located at `path/to/venv/bin/postactivate`):

```
export DJANGO_SETTINGS_MOUDLE="settings.dev"
```
* Deactivate, and then reactivate the venv
* Create a Postgres database called `cks_new`

```
createdb cks_new --template=template0 --encoding=utf8 --locale=en_US.utf8
```

* Create a Postgres user with username `cks_new` and password `password` with full permissions to this db. Open the Postgres shell (`psql`), then:

```
CREATE USER cks_new WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE cks_new TO cks_new;
```

* Run migrations

```
./manage.py migrate
```
* Create a superuser

```
./manage.py createsuperuser
```

* Run server

```
./manage.py runserver
```