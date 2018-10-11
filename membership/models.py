from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *

class FirebaseToken(models.Model):
    student = models.ForeignKey(Student)
    token = models.CharField(max_length = 500)

    def __str__(self):
        return str(self.student) + ' ' + str(self.token)
 
