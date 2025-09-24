from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.CreateShortLinkView.as_view(), name='link_create'),
    path("link/<str:code>/", views.LinkDetailView.as_view(), name="link_detail"),
    path("<str:code>/", views.GoView.as_view(), name="go"),
    path("link/<str:code>/toggle/", views.LinkToggleActiveView.as_view(), name="link_toggle"),

]
