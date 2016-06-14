# coding=utf-8
import datetime
from django import forms


class CustomerForm(forms.Form):
    GENDER_CHOICES = (
        ('n', '-'),
        ('m', 'Мужской'),
        ('f', 'Женский')
    )

    MONTHS_CHOICES = (
        (0, "Месяц"),
        (1, "Январь"),
        (2, "Февраль"),
        (3, "Март"),
        (4, "Апрель"),
        (5, "Май"),
        (6, "Июнь"),
        (7, "Июль"),
        (8, "Август"),
        (9, "Сентябрь"),
        (10, "Октябрь"),
        (11, "Ноябрь"),
        (12, "Декабрь"),
    )
    YEARS_CHOICES = [(0, "Год")] + [(x, x) for x in xrange(1930, datetime.date.today().year + 1, 1)]
    DAYS_CHOICES = [(0, "День")] + [(x, x) for x in xrange(1, 31 + 1)]

    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'id': "first_name"}))
    patronymic_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'id': "patronymic_name"}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class': "form-control", 'id': "last_name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "email"}))
    login = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "login"}))

    club = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "club"}))
    group = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "group"}))
    role = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "role"}))

    day_of_birth = forms.ChoiceField(required=False,
                                     choices=DAYS_CHOICES,
                                     widget=forms.Select(attrs={'class': "form-control selectpicker", 'id': "day"}))
    month_of_birth = forms.ChoiceField(required=False,
                                       choices=MONTHS_CHOICES,
                                       widget=forms.Select(attrs={'class': "form-control selectpicker", 'id': "month"}))
    year_of_birth = forms.ChoiceField(required=False,
                                      choices=YEARS_CHOICES,
                                      widget=forms.Select(attrs={'class': "form-control selectpicker", 'id': "year"}))
    gender = forms.ChoiceField(required=False,
                               choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': "form-control selectpicker", 'id': "gender"}))