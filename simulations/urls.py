from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="simulations"),
    path("login", views.login, name="login"),
    path("new_user", views.new_user, name="new_user"),
    path("userspace", views.userspace, name="userspace"),
    path("saved_simulations", views.saved_simulations, name="saved_simulations"),
    path("view_saved_simulation", views.view_saved_simulation, name="view_saved_simulation"),
    path("newsimulation", views.newsimulation, name="newsimulation"),
    path("new_anonymous_simulation", views.new_anonymous_simulation, name="new_anonymous_simulation"),
    path("view_simulation", views.view_simulation, name="view_simulation"),
    path("save_simulation", views.save_simulation, name="save_simulation"),
]