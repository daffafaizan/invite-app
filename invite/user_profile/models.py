from django.db import models, models.Model as Model

class RegisteredUser(Model):
    email = models.EmailField(primary_key=True, max_length=250)
    password = 
    