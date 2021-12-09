from django.db import models


class CustomerInfo(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}-{self.user_id}'