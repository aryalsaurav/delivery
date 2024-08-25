from django.urls import path

from . import views


app_name = "delivery"

urlpatterns = [
    path('login/',views.LoginView.as_view(),name="login"),

    ##user
    path('user/list/',views.UserListView.as_view(),name="user-list"),
    path('user/create/',views.UserCreateView.as_view(),name="user-create"),
    path('user/<int:id>/delete/',views.UserDeleteView.as_view(),name='user-delete'),
    path('user/<int:id>/update/',views.UserUpdateView.as_view(),name='user-update'),

    ##delivery location
    path('delivery/location/',views.DeliveryLocationCreateView.as_view(),name="delivery-location-requested-user "),
    path('delivery/location/<int:id>/',views.DeliveryLocationCreateView.as_view(),name="delivery-location-user"),
    path('delivery/location/<int:id>/update/',views.LocationUpdateView.as_view(),name="delivery-location-update"),
    path('delivery/location/<int:id>/delete/',views.LocationDeleteView.as_view(),name="delivery-location-delete"),


    ##age group
    path('age/distribution/',views.AgeGroupDistributionView.as_view(),name='age-distribution'),
    path('bar/chart/', views.MatplotlibView.as_view(),name="bar-chart"),


]
