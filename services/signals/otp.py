import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import OneTimePassword

@receiver(post_save, sender=OneTimePassword)
def generate_code(sender, instance, created, **kwargs):
    if created:
        code_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(code_list)
            code_items.append(num)
        code = "".join(str(n) for n in code_items)
        OneTimePassword.objects.filter(pk=instance.pk).update(code=code)
       