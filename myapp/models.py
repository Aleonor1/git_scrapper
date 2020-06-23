from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models

class Search (models.Model):
    search = models.CharField(max_length=500)
    user = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = "Searches"

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name","password1", "password2"]
