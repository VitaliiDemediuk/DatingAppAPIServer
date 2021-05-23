from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from DatingApp.managers import CustomUserManager


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=False)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    email = models.EmailField('email address', unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the "
                                         "format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    birthdate = models.DateField()
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, null=True)
    information = models.TextField(blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    seen_users = models.ManyToManyField('CustomUser', through='SeenUsers', related_name='seen_user_list')
    liked_users = models.ManyToManyField('CustomUser', through='LikedUsers', related_name='liked_user_list')
    messages = models.ManyToManyField('CustomUser', through='Message', related_name='message_list')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'phone_number',
                       'birthdate', 'city', 'gender', 'information']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class PhotoForUser(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    file_name = models.ImageField(upload_to="photos_for_user/%Y/%m/%d/")
    position = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "User's photo"
        verbose_name_plural = "User's photos"

    def __str__(self):
        return str(self.file_name)


class SeenUsers(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_who_seen')
    seen_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='seen_user')

    class Meta:
        verbose_name = "Seen user"
        verbose_name_plural = "Seen users"
        unique_together = (('user', 'seen_user'),)


class LikedUsers(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_who_liked')
    liked_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='liked_user')

    class Meta:
        verbose_name = "Liked user"
        verbose_name_plural = "Liked users"
        unique_together = (('user', 'liked_user'),)


class Message(models.Model):
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['add_date']

    def __str__(self):
        return str(self.message)


class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __str__(self):
        return str(self.name)


class InterestForUser(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    interest = models.ForeignKey('Interest', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"
        unique_together = (('user', 'interest'),)