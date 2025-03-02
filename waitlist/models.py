from django.db import models

# Create your models here.
class Waitlist(models.Model):
    email = models.EmailField(max_length=50, default=None, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email