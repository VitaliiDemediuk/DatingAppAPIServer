import DatingApp.models as models


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
