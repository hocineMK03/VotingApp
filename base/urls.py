from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.login_page,name="loginpage"),
    path('register',views.register_page,name='registerpage'),
    path('logout',views.logout_page,name="logoutpage"),
    path('poll/<int:pk>',views.poll_voting,name="poll_visit"),
    path('create',views.poll_create,name="poll_create"),
    path('ccreate/<int:pk>',views.choice_create,name="choice_create"),
    path('edit/<int:pk>',views.editvote,name="editvote"),
]
