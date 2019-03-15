from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name="start"),
    path('graph/', views.graph, name="graph"),
    path('others/', views.others, name="others"),
    path('search/', views.search, name="search"),
]
