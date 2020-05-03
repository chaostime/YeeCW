# YeeCW



#### Getting started

##### Requirements:

Python 3



##### Steps

Clone the repository, then run ```virtualenv venv``` to create a virtual environment.

Activate the venv with ```. venv/bin/activate``` and install the required packages with ```pip install -r requirements.txt``` 

Optionally, change to the yeecw project directory and run ```python manage.py createsuperuser``` to create yourself an admin account for your local dev environment

From the yeecw project directory, the web app can be launched with ```python manage.py runserver```


#### Testing environment

Ubuntu 20.04 VM
Nginx installed from system packages
Gunicorn installed into django virtualenv



Nginx:

Create a config file under /etc/nginx/sites-available

Minimum config:

```nginx
server {
  listen 80;
  server_name django;
  access_log /var/log/nginx/django.log;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  location /static {
    alias /home/vagrant/yeecw/yeecw/static/;
  }
}

```

Symbolic link the config from sites-available into ../sites-enabled (also delete the default symbolic link)

Reload nginx with systemctl reload nginx



Gunicorn: activate the django virtualenv and go into the root project directory (where manage.py is found)

Launch gunicorn with:

```
gunicorn -b 127.0.0.1:8000 yeecw.wsgi
```



Nginx will now proxy application requests to Gunicorn, and serve static files from the /static location alias as specified in the nginx config.

**ENSURE** that the static files location matches up with the project settings.py e.g.

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
```

From the project root directory, collect all static files with **python manage.py collectstatic**

Good to go!
