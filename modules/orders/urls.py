from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/update_status/<int:order_id>/', views.update_order_status, name='update_status'),
    path('search_orders/', views.search_orders, name='search_orders'),
    path('calculate_revenue/', views.calculate_revenue, name='calculate_revenue'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
]