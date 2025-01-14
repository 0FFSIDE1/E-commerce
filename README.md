# E Commerce Backend
E commerce version one

## Setup

1. Clone the repo.
 ```sh
 git clone "<repo_url>"
```



2. Create a virtual environment.
 ```bash
    python3 -m venv .venv
 ```

3. Activate virtual environment.
```bash
    source /path/to/venv/bin/activate`
```

4. Install project dependencies `pip install -r requirements.txt`

5. Create your own branch.
 ```sh
 git branch <branch-name>
```

6. Pull from origin/dev branch.
 ```sh
 git fetch origin dev
 git merge origin/dev

```
7. Create a .env file by copying the .env.sample file
`cp .env.sample .env`

8. Make makemigrations.
 ```sh
 python manage.py makemigrations
```

9. Migrate.
 ```sh
 python manage.py migrate
```


## Issues
if you encounter the following Error, when you run the code below

**Superuser creation skipped due to not running in a TTY. You can run `manage.py createsuperuser` in your project to create one manually.
'**

## Solutions using command line
Run the following code below first to createsuperuser
**python manage.py createsuperuser --noinput**



## Updates 
Always keep your branch updated with the dev branch

