from django.db import models

# Create your models here.
class Newsletter(models.Model):
    email = models.EmailField(default=None, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email, self.created_at
