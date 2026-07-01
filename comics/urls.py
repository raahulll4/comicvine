from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('results/', views.results, name='results'),
    path('timeline/<int:volume_id>/', views.timeline, name='timeline'),
    path('timeline/<int:volume_id>/toggle/<int:issue_id>/', views.toggle_issue, name='toggle_issue'),
]