from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework import exceptions

import DatingApp.services as services
import DatingApp.serializers as serializers
import DatingApp.permissions as my_permissions


# Country -------------------------------------------------
class CountryCreateView(generics.CreateAPIView):
    serializer_class = serializers.CountrySerializer
    permission_classes = (permissions.IsAdminUser, )


class CountryListView(generics.ListAPIView):
    serializer_class = serializers.CountrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = services.get_countries()


class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CountrySerializer
    permission_classes = (my_permissions.IsAdminUserOrReadOnly,)
    queryset = services.get_countries()


# City ----------------------------------------------------
class CityCreateView(generics.CreateAPIView):
    serializer_class = serializers.CityDetailSerializer
    permission_classes = (permissions.IsAdminUser, )


class CityListView(generics.ListAPIView):
    serializer_class = serializers.CityListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        country_id = self.kwargs.get('country_id')
        queryset = services.get_cities(country_id=country_id)
        return queryset


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CityDetailSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = services.get_cities()


# Interest ------------------------------------------------
class InterestCreateView(generics.CreateAPIView):
    serializer_class = serializers.InterestSerializer
    permission_classes = (permissions.IsAdminUser, )


class InterestListView(generics.ListAPIView):
    serializer_class = serializers.InterestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = services.get_interests(user_id=user_id)
        return queryset


class InterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.InterestSerializer
    queryset = services.get_countries()
    permission_classes = (permissions.IsAdminUser, )


# User ----------------------------------------------------
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


class InterestForUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request):
        data: dict = request.data

        user_id = data.get('user')
        interest_ids = data.get('interests')

        did_set, detail = False, ''
        if request.user.id is user_id:
            did_set, detail = services.set_interests_for_user(user_id, interest_ids)
        else:
            did_set, detail = False, 'Field user is not similar to authenticated user'

        return Response(data={'detail': detail}, status=(201 if status.HTTP_201_CREATED else
                                                                status.HTTP_400_BAD_REQUEST))


# Message -------------------------------------------------
class MessageCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request):
        data: dict = request.data

        sender_id = data.get('sender')
        receiver_id = data.get('receiver')
        message = data.get('message')

        if type(sender_id) is not int or \
           type(receiver_id) is not int or \
           type(message) is not str:
            return Response(data={'detail': "Invalid param."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            services.send_message(sender_id, receiver_id, message)
        except exceptions.ValidationError as err:
            return Response(data={'detail': err.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'detail': "Message sent successfully."}, status=status.HTTP_201_CREATED)


class MessageListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MessageListSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        sender_id = self.request.data.get('sender')
        receiver_id =  self.request.data.get('receiver')
        if type(sender_id) is not int or \
           type(receiver_id) is not int:
            raise exceptions.ValidationError(detail='Invalid params')

        if self.request.user.id is sender_id:
            pass
        else:
            raise exceptions.ValidationError(detail='Field sender_id is not similar to authenticated user')

        queryset = services.get_messages(sender_id, receiver_id)
        return queryset
