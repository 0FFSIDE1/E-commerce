# E Commerce Backend
E commerce version one

## Setup

1. Clone the repo.
 ```sh
 git clone "<repo_url>"
```

2. Navigate to v1 folder.
 ```sh
 cd v1
```

3. Create a virtual environment.
 ```bash
    python3 -m venv .venv
 ```

4. Activate virtual environment.
```bash
    source /path/to/venv/bin/activate`
```

5. Install project dependencies `pip install -r requirements.txt`

6. Create your own branch.
 ```sh
 git branch <branch-name>
```

7. Pull from origin/dev branch.
 ```sh
 git fetch origin dev
 git merge origin/dev

```
8. Create a .env file by copying the .env.sample file
`cp .env.sample .env`

9. Make makemigrations.
 ```sh
 python manage.py makemigrations
```

10. Migrate.
 ```sh
 python manage.py migrate
```


## Issues
if you encounter the following Error, when you run the code below

**Superuser creation skipped due to not running in a TTY. You can run `manage.py createsuperuser` in your project to create one manually.
'**

## Solutions using command line
Run the following code below first to createsuperuser
**python manage.py createsuperuser --noinput --username <your_username> --email <your_email>**

then, run this.
**python manage.py shell**


then, run this.
**from django.contrib.auth.models import User

>>> # Retrieve the user
>>> user = User.objects.get(username="<your_username>")
>>>
>>> # Set the password
>>> user.set_password("your_new_password")
>>>
# Save the user
user.save()

print("Password updated successfully!")**

then, run this again.
**python manage.py runserver**


## Updates always keep ypur branch updated with the dev branch

