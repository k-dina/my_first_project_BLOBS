from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="simulations"),
    path("userspace", views.userspace, name="userspace"),
    path("saved_simulations", views.saved_simulations, name="saved_simulations"),
    path("view_saved_simulation", views.view_saved_simulation, name="view_saved_simulation"),
    path("newsimulation", views.newsimulation, name="newsimulation"),
    path("view_simulation/<str:id>/", views.view_simulation, name="view_simulation"),
    path("save_simulation", views.save_simulation, name="save_simulation"),
]