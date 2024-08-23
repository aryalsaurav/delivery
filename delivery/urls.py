from django.urls import path

from . import views


app_name = "delivery"

urlpatterns = [
    path('user/list/',views.UserListView.as_view(),name="user-list"),
    path('user/create/',views.UserCreateView.as_view(),name="user-create"),
    path('login/',views.LoginView.as_view(),name="login"),

]
