from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics

import DatingApp.services as services
import DatingApp.serializers as serializers


# Country -------------------------------------------------
class CountryCreateView(generics.CreateAPIView):
    serializer_class = serializers.CountrySerializer


class CountryListView(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer
    queryset = services.get_countries()


class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CountrySerializer
    queryset = services.get_countries()


# City ----------------------------------------------------
class CityCreateView(generics.CreateAPIView):
    serializer_class = serializers.CitySerializer


class CityListView(generics.ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        country_id = self.kwargs.get("country_id")
        queryset = services.get_cities(country_id=country_id)
        return queryset


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CitySerializer
    queryset = services.get_cities()


# User ----------------------------------------------------
class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserDetailSerializer


class UserListView(generics.ListAPIView):
    serializer_class = serializers.UserListSerializer

    def get_queryset(self):
        queryset = services.get_users()
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserDetailSerializer
    queryset = services.get_users()
