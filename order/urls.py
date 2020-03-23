from django.urls import path, include

from order import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('me', views.ManageOrderView)
router.register('supervisor/view-orders', views.SupervisorOrderManage)

app_name = 'order'

urlpatterns = [
    path('new/', views.CreateOrder.as_view(), name='order-list'),
    path('', include(router.urls))
]
