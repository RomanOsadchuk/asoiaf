from django.urls import path

from . import views

urlpatterns = [
    path('profiles/<int:profile>/days/<int:day>/', views.profile_ice_on_day, name='profile_ice_on_day'),
    path('profiles/<int:profile>/overview/<int:day>/', views.profile_cost_by_day, name='profile_cost_by_day'),
    path('profiles/overview/<int:day>/', views.total_cost_by_day, name='total_cost_by_day'),
    path('profiles/overview/', views.total_cost, name='total_cost'),
]
