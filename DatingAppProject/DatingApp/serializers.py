from rest_framework import serializers
import DatingApp.models as models
from DatingApp import services


# Country -------------------------------------------------
class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = ('id', 'name')


# City ----------------------------------------------------
class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ('id', 'name')


# Interest-------------------------------------------------
class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Interest
        fields = ('id', 'name')


# User ----------------------------------------------------
class PhotoForUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PhotoForUser
        fields = ('id', 'file_name', 'position')


class UserDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        photos_query_set = services.get_photos(obj.id)
        photos = map(lambda photo: PhotoForUserSerializer(photo).data, photos_query_set)
        return photos

    class Meta:
        model = models.CustomUser
        fields = ('id', 'first_name', 'second_name',
                  'email', 'phone_number', 'photos',
                  'gender', 'city',
                  'birthdate', 'information')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ('id', 'first_name', 'second_name',
                  'email', 'gender', 'city')
