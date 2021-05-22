from django.urls import path, re_path, include

import DatingApp.views as views

urlpatterns = [
    # Country -------------------------------------------------
    path('country/', views.CountryCreateView.as_view()),
    path('country/<int:pk>/', views.CountryDetailView.as_view()),
    path('country/all/', views.CountryListView.as_view()),
    # City ----------------------------------------------------
    path('city/', views.CityCreateView.as_view()),
    path('city/<int:pk>', views.CityListView.as_view()),
    path('city/all/', views.CityListView.as_view()),
    path('city/all/<int:country_id>', views.CityListView.as_view()),
    # Interest ----------------------------------------------------
    path('interest/', views.InterestCreateView.as_view()),
    path('interest/<int:pk>/', views.InterestDetailView.as_view()),
    path('interest/all/', views.InterestListView.as_view()),
    path('interest/all/<int:user_id>/', views.InterestListView.as_view()),
    # User ----------------------------------------------------
    path('user/', views.UserCreateView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('user/all/', views.UserListView.as_view()),
]