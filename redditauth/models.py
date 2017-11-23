from django.db import models


class AuthToken(models.Model):
    token = models.TextField()
    username = models.TextField()
