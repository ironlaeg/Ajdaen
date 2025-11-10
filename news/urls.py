from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HeadlineListView.as_view(), name='headline_list'),
    path('<int:pk>/', views.HeadlineDetailView.as_view(), name='headline_detail'),
    path('create/', views.HeadlineCreateView.as_view(), name='headline_create'),
    path('<int:pk>/edit/', views.HeadlineUpdateView.as_view(), name='headline_edit'),
    path('<int:pk>/delete/', views.HeadlineDeleteView.as_view(), name='headline_delete'),
    path('drafts/', views.HeadlineDraftListView.as_view(), name='headline_drafts'),
    path('archive/', views.HeadlineArchiveView.as_view(), name='headline_archive'),
    path('archive/<int:year>/<int:month>/', views.HeadlineMonthArchiveView.as_view(), name='headline_month'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag_list'),
]