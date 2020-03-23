from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create-user'),
    path('token/', views.CreateTokenView.as_view(), name='user-token'),
    path('me/', views.ManageUserView.as_view(), name='user-me'),

    path('supervisor/create/', views.CreateSupervisorView.as_view(), name='create-supervisor'),
    path('supervisor/token/', views.CreateTokenView.as_view(), name='supervisor-token'),
    path('supervisor/me/', views.ManageSupervisorView.as_view(), name='supervisor-me'),

    path('superuser/create/', views.CreateSuperuserView.as_view(), name='create-superuser'),
    path('superuser/token/', views.CreateTokenView.as_view(), name='superuser-token'),
    path('superuser/me/', views.ManageSuperuserView.as_view(), name='superuser-me'),

    path('deliveryguy/create/', views.CreateDeliveryGuyView.as_view(), name='create-deliveryguy'),
    path('deliveryguy/token/', views.CreateTokenView.as_view(), name='deliveryguy-token'),
    path('deliveryguy/me/', views.ManageDeliveryGuyView.as_view(), name='deliveryguy-me'),
]
