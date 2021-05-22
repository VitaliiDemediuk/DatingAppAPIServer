from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics
from rest_framework import permissions

import DatingApp.services as services
import DatingApp.serializers as serializers
import DatingApp.permissions as my_permissions


# Country -------------------------------------------------
class CountryCreateView(generics.CreateAPIView):
    serializer_class = serializers.CountrySerializer
    permission_classes = (permissions.IsAdminUser, )


class CountryListView(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer
    queryset = services.get_countries()


class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CountrySerializer
    queryset = services.get_countries()
    permission_classes = (my_permissions.IsAdminUserOrReadOnly, )


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


# Interest ------------------------------------------------
class InterestCreateView(generics.CreateAPIView):
    serializer_class = serializers.InterestSerializer
    permission_classes = (permissions.IsAdminUser, )


class InterestListView(generics.ListAPIView):
    serializer_class = serializers.InterestSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        queryset = services.get_interests(user_id=user_id)
        return queryset


class InterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.InterestSerializer
    queryset = services.get_countries()
    permission_classes = (permissions.IsAdminUser, )


# User ----------------------------------------------------
class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserDetailSerializer


class UserListView(generics.ListAPIView):
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        queryset = services.get_users()
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = services.get_users()
