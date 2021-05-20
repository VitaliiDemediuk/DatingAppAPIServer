from rest_framework import serializers
import DatingApp.models as models


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = '__all__'


class PhotoForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhotoForUser
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    photos = PhotoForUserSerializer(many=True)

    class Meta:
        model = models.CustomUser
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = '__all__'
