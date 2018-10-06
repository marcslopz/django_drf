from rest_framework import routers
from users import views


users_router = routers.DefaultRouter()
users_router.register(r'users', views.UserViewSet)
users_router.register(r'groups', views.GroupViewSet)
