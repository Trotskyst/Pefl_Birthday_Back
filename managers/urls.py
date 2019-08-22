from django.urls import path, include
from managers.views import *


urlpatterns = [
    # path("manager/create/", ManagerCreateView.as_view()),
    path("all/", ManagersListAllView.as_view()),
    path("count/", ManagersCountView.as_view()),
    # path("manager/detail/<int:pk>/", ManagerDetailView.as_view()),
    path("date/<str:month>/<str:day>/", ManagersListDayView.as_view()),
    path("date/<str:month>/", ManagersListMonthView.as_view()),
    path("letter/<str:letter>/", ManagersListLetterView.as_view()),
    path("countries/", ChempsCountriesView.as_view()),
    path("country/<str:country>/", ManagersCountryView.as_view()),
    path("woman/", ManagersWomanView.as_view()),
]