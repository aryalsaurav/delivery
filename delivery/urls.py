from django.urls import path

from . import views


app_name = "delivery"

urlpatterns = [
    path('login/',views.LoginView.as_view(),name="login"),


    path('user/list/',views.UserListView.as_view(),name="user-list"),
    path('user/create/',views.UserCreateView.as_view(),name="user-create"),
    path('user/<int:id>/delete/',views.UserDeleteView.as_view(),name='user-delete'),
    path('user/<int:id>/update/',views.UserUpdateView.as_view(),name='user-update'),

]
