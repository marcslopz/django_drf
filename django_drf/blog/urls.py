from rest_framework import routers

from blog import views


blog_router = routers.DefaultRouter()
blog_router.register(r'posts', views.PostViewSet)
blog_router.register(r'tags', views.TagViewSet)
