from django.db import models

# Create your models here.
class Feedback(models.Model):
    email = models.EmailField(default=None, max_length=50, blank=False, null=False)
    message = models.TextField(default=None, max_length=None, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email