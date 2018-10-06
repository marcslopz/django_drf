# django_drf
Small Django Rest Framework project

## To start django server
### Requirements
- docker
- docker-compose

### Instructions
To start the server
```
docker-compose up
```

To create admin user
```
docker-compose run django_drf django_drf/manage.py createsuperuser --email email@example.com --username admin_username
```