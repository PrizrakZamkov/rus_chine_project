from django.db import models


class Groups(models.Model):
    group = models.CharField(max_length=25, default="Default")


class RusChineHistory(models.Model):
    #group = models.ForeignKey(to=Groups, on_delete=Groups.objects.get(id = 1))
    group = models.ForeignKey(to=Groups, on_delete=models.CASCADE, default=1)
    rus = models.CharField(max_length=1023)
    chine = models.CharField(max_length=1023)
