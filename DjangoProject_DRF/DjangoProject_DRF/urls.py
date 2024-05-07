"""
URL configuration for DjangoProject_DRF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from CBVpractice import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('publish', views.PublishViewSet)
router.register('author', views.AuthorViewSet)
router.register('book', views.BookViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    #
    # ####################################
    # # View + APIView
    path('sers/book/', views.BookView.as_view()),
    re_path('sers/book/(\d+)', views.BookDetailView.as_view()),
    # ####################################
    #
    # ####################################
    # GenericAPIView
    path('sers/generic/book/', views.BookGenericApiView.as_view()),
    re_path('sers/generic/book/(?P<pk>\d+)', views.BookDetailGenericApiView.as_view()),
    path('sers/generic/publish/', views.PublishGenericApiView.as_view()),
    re_path('sers/generic/publish/(?P<pk>\d+)', views.PublishDetailGenericApiView.as_view()),
    path('sers/generic/author/', views.AuthorGenericApiView.as_view()),
    re_path('sers/generic/author/(?P<pk>\d+)', views.AuthorDetailGenericApiView.as_view()),
    # ####################################
    #
    # ###################################
    # Mixin
    path('sers/mixin/auth/', views.AuthorMixinView.as_view()),
    re_path('sers/mixin/auth/(?P<pk>\d+)', views.AuthorDetailMixinView.as_view()),
    path('sers/mixin/book/', views.BookMixinView.as_view()),
    re_path('sers/mixin/book/(?P<pk>\d+)', views.BookDetailMixinView.as_view()),
    path('sers/mixin/publish/', views.PublishMixinView.as_view()),
    re_path('sers/mixin/publish/(?P<pk>\d+)', views.PublishDetailMixinView.as_view()),
    # ###################################
    #
    # ###################################
    # MixinSimple
    path('sers/mixinsimple/auth/', views.AuthorMixinSimpleView.as_view()),
    re_path('sers/mixinsimple/auth/(?P<pk>\d+)', views.AuthorDetailMixinSimpleView.as_view()),
    path('sers/mixinsimple/book/', views.BookMixinSimpleView.as_view()),
    re_path('sers/mixinsimple/book/(?P<pk>\d+)', views.BookDetailMixinSimpleView.as_view()),
    path('sers/mixinsimple/publish/', views.PublishMixinSimpleView.as_view()),
    re_path('sers/mixinsimple/publish/(?P<pk>\d+)', views.PublishDetailMixinSimpleView.as_view()),
    # ###################################
    #
    # ###################################
    # ViewSet
    path('sers/viewset/book/', views.BookViewSet.as_view(
        {"get": "list", "post": "create"})
         ),
    re_path('sers/viewset/book/(?P<pk>\d+)', views.BookViewSet.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"})
            ),
    path('sers/viewset/publish/', views.PublishViewSet.as_view(
        {"get": "list", "post": "create"})
         ),
    re_path('sers/viewset/publish/(?P<pk>\d+)', views.PublishViewSet.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"})
            ),
    path('sers/viewset/author/', views.AuthorViewSet.as_view(
        {"get": "list", "post": "create"})
         ),
    re_path('sers/viewset/author/(?P<pk>\d+)', views.AuthorViewSet.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"})
            ),
    # ###################################

]
urlpatterns += router.urls
