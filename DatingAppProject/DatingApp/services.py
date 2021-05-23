import DatingApp.models as models
from django.db import IntegrityError, transaction


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
        return False, "Field interest_ids is required."
    if interest_ids is not list:
        return False, "Field interest_ids should be a list."

    try:
        with transaction.atomic():
            user = models.CustomUser.objects.get(pk=user_id)
            models.PhotoForUser.objects.filter(user=user).delete()
            for interest_id in interest_ids:
                interest = models.Interest.objects.get(pk=interest_id)
                models.InterestForUser(user=user, interest=interest).save()

    except IntegrityError:
        return False, "User does not exist."
    except models.CustomUser.DoesNotExist:
        return False, "User does not exist."
    except models.InterestForUser.DoesNotExist:
        return False, "Interest does not exist."

    return True, "Interests successfully added."
