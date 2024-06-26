from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('list/', views.CommissionListView.as_view(), name='commission_list'),
    path('detail/<int:pk>/', views.CommissionDetailView.as_view(), name='commission_detail'),
    path('add/', views.CommissionCreateView.as_view(), name='commission_create'),
    path('<int:pk>/edit/', views.CommissionUpdateView.as_view(), name='commission_update'),
    path('<int:pk>/apply', views.JobApplicationCreateView.as_view(), name='commission_apply'),

]
