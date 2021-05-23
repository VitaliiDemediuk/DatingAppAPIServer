import DatingApp.models as models
from django.db.models import Q
from django.db import IntegrityError, transaction
from rest_framework import exceptions


def get_countries():
    countries = models.Country.objects.all()
    return countries


def get_cities(country_id=None):
    cities = None
    if country_id:
        cities = models.City.objects.filter(country=country_id)
    else:
        cities = models.City.objects.all()

    return cities


def get_users():
    users = models.CustomUser.objects.all()
    return users


def get_user(user_id: int):
    try:
        return models.CustomUser.objects.get(pk=user_id)
    except models.CustomUser.DoesNotExist:
        return None


def get_interests(user_id=None):
    users = None
    if user_id:
        users = models.Interest.objects.filter(country=user_id)
    else:
        users = models.Interest.objects.all()

    return users


def get_photos(user_id):
    photos = models.PhotoForUser.objects.filter(user=user_id)
    return photos


def set_interests_for_user(user_id, interest_ids) -> (bool, str):
    if not interest_ids:
        return False, 'Field interest_ids is required.'
    if interest_ids is not list:
        return False, 'Field interest_ids should be a list.'

    try:
        with transaction.atomic():
            user = models.CustomUser.objects.get(pk=user_id)
            models.PhotoForUser.objects.filter(user=user).delete()
            for interest_id in interest_ids:
                interest = models.Interest.objects.get(pk=interest_id)
                models.InterestForUser(user=user, interest=interest).save()

    except IntegrityError:
        return False, 'User does not exist.'
    except models.CustomUser.DoesNotExist:
        return False, 'User does not exist.'
    except models.InterestForUser.DoesNotExist:
        return False, 'Interest does not exist.'

    return True, 'Interests successfully added.'


def did_users_like_each_other(first_user, second_user: int) -> bool:
    try:
        models.LikedUsers.objects.get(user=first_user, liked_user=second_user)
        models.LikedUsers.objects.get(user=second_user, liked_user=first_user)
        return True
    except ...:
        return False


def send_message(sender_id: int, receiver_id: int, message: str):
    try:
        with transaction.atomic():
            sender = models.CustomUser.objects.get(pk=sender_id)
            receiver = models.CustomUser.objects.get(pk=receiver_id)
            if did_users_like_each_other(sender, receiver):
                models.Message(sender=sender, receiver=receiver, message=message).save()
            else:
                raise exceptions.ValidationError(detail='Sender and receiver did not like each other.')
    except ...:
        raise exceptions.ValidationError(detail='Something wend wrong.')


def get_messages(sender_id: int, receiver_id: int):
    try:
        with transaction.atomic():
            sender = models.CustomUser.objects.get(pk=sender_id)
            receiver = models.CustomUser.objects.get(pk=receiver_id)
            if did_users_like_each_other(sender, receiver):
                return models.Message.objects.filter(Q(sender=sender, receiver=receiver) |
                                                     Q(sender=receiver, receiver=sender))
            else:
                raise exceptions.ValidationError(detail='Sender and receiver did not like each other.')
    except ...:
        raise exceptions.ValidationError(detail='Something wend wrong.')