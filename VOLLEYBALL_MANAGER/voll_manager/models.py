from __future__ import unicode_literals

from django.db import models
from django.core import validators

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.postgres.fields import ArrayField

import datetime


CUSTOMER_GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('n', '-')
)

CUSTOMER_MONTHS = (
    (0, "Month"),
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
)

CUSTOMER_YEARS = [(0, "Year")] + [(x, x) for x in xrange(1930, datetime.date.today().year + 1, 1)]
CUSTOMER_DAYS = [(0, "Day")] + [(x, x) for x in xrange(1, 31)]


class Country(models.Model):
    short_name = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = u'Countries'

    def __str__(self):
        return u"{}".format(self.full_name)

    @classmethod
    def get_by_name(cls, country_name):
        return cls.objects.filter(full_name=country_name).first() \
            or cls.objects.filter(short_name=country_name).first()


class City(models.Model):
    short_name = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=60, unique=True)
    country = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Cities'

    def __str__(self):
        return u"{}".format(self.full_name)

    @classmethod
    def get_by_name(cls, city_name):
        return cls.objects.filter(full_name=city_name).first() \
            or cls.objects.filter(short_name=city_name).first()


class Address(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    address_line_1 = models.CharField(max_length=200, blank=True)
    address_line_2 = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=60, default="")
    postcode = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = u'Address'
        verbose_name_plural = u'Addresses'

    def __str__(self):
        return u"{}; {}; {}".format(self.address_line_1, self.city, self.country)


class MainTeam(models.Model):
    date = models.DateField(blank=True)
    players = ArrayField(models.PositiveIntegerField(), blank=True)


class Club(models.Model):
    title = models.CharField(max_length=50, blank=True)
    id_couch = models.PositiveIntegerField(default=0, blank=True)
    description = models.CharField(max_length=200, blank=True)
    address = models.ForeignKey(Address, related_name="club_address", null=True, blank=True)
    main_team = models.ForeignKey(MainTeam, related_name="main_team", null=True, blank=True)


class Group(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    level = models.PositiveIntegerField(default=0, blank=True)


class Category(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)


class Priority(models.Model):
    title = models.CharField(max_length=50, blank=True)
    level = models.PositiveIntegerField(default=0, blank=True)


class Role(models.Model):
    title = models.CharField(max_length=50, blank=True)


class CustomerUser(AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=254, unique=True,
                                help_text=_('Required. 254 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })

    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    patronymic_name = models.CharField(max_length=100, blank=True)

    email = models.EmailField(_('email address'), blank=True)

    day_of_birth = models.PositiveIntegerField(default=0, choices=CUSTOMER_DAYS, blank=True)
    month_of_birth = models.PositiveSmallIntegerField(default=0, choices=CUSTOMER_MONTHS, blank=True)
    year_of_birth = models.PositiveIntegerField(default=0, choices=CUSTOMER_YEARS, blank=True)

    gender = models.CharField(max_length=1, choices=CUSTOMER_GENDER, blank=True)

    address = models.ForeignKey(Address, related_name="address", null=True, blank=True)

    avatar = models.ImageField(upload_to='static/media/images/avatars/', null=True, blank=True)

    club = models.ForeignKey(Club, related_name="club", null=True, blank=True)
    group = models.ForeignKey(Group, related_name="group", null=True, blank=True)
    category = models.ForeignKey(Category, related_name="category", null=True, blank=True)
    role = models.ForeignKey(Role, related_name="role", null=True, blank=True)
    priority = models.ForeignKey(Priority, related_name="priority", null=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class Unit(models.Model):
    title = models.CharField(max_length=100, blank=True)
    short_title = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)


class Parameter(models.Model):
    title = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    unit = models.ForeignKey(Unit, related_name="unit", null=True, blank=True)


class Metric(models.Model):
    value = models.CharField(max_length=50, blank=True)
    date = models.DateField(blank=True)
    user = models.ForeignKey(CustomerUser, related_name="user", null=True, blank=True)
    parameter = models.ForeignKey(Parameter, related_name="parameter", null=True, blank=True)




