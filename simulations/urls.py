from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="simulations"),
    path("userspace", views.userspace, name="userspace"),
    path("saved_simulations", views.saved_simulations, name="saved_simulations"),
    path("newsimulation", views.newsimulation, name="newsimulation"),
    path("view_simulation/<str:id>/", views.view_simulation, name="view_simulation"),
    path("save_simulation", views.save_simulation, name="save_simulation"),
    path("get_snapshots/<str:id>/<int:step>/", views.get_snapshots, name="get_snapshots"),
    path("resume_simulation/<str:id>/<int:step>/", views.resume_simulation, name="resume_simulation"),

]
