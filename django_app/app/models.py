from django.db import models
from django.contrib.auth.models import User


class Groups(models.Model):
    group = models.CharField(max_length=25, default="Default")

class RusChineHistory(models.Model):
    group = models.ForeignKey(to=Groups, on_delete=models.SET(2), default=1)
    rus = models.CharField(max_length=1023)
    chine = models.CharField(max_length=1023)





class Languages(models.Model):
    language = models.CharField(max_length=1023)


class NewConnectionsForGroup(models.Model):
    pass


class NewConnections(models.Model):
    group = models.ForeignKey(to=NewConnectionsForGroup, on_delete=models.CASCADE, default=2)
    is_group = models.BooleanField(default=False)



class NewPhrases(models.Model):
    is_group = models.BooleanField(default=False)
    word = models.CharField(max_length=1023)
    language = models.ForeignKey(to=Languages, on_delete=models.CASCADE)
    connections = models.ForeignKey(to=NewConnections, on_delete=models.CASCADE, default=2)


class UserSetting(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    current_group = models.ForeignKey(to=NewConnectionsForGroup, on_delete=models.SET(1), default=1)
    language_from = models.ForeignKey(to=Languages, default=1, on_delete=models.CASCADE, related_name='fitst')
    language_to = models.ForeignKey(to=Languages, default=2, on_delete=models.CASCADE, related_name='second')
