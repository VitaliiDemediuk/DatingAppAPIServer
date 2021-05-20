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
