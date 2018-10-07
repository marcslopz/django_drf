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

To run tests:
```
docker-compose run django_drf django_drf/manage.py test blog
```

### Urls
default API router page:
```
http://localhost:8000/
```

Blog rendered version:
- list
```
http://localhost:8000/posts/?render=true
```
- detail
```
http://localhost:8000/posts/<id>/?render=true
```

Posts API:
- list
```
http://localhost:8000/posts/
```
- detail
```
http://localhost:8000/posts/<id>/
```

Tags API:
- list
```
http://localhost:8000/tags/
```
- detail
```
http://localhost:8000/tags/<id>/
```

