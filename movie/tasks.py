import random
import string

from celery import shared_task

from .models import Category


# @shared_task
# def create_new_object():
#     random_name = ''.join((random.choice(string.ascii_letters) for _ in range(10)))
#     new_object = Category.objects.create(name=random_name, description=random_name, url=random_name)
#     return new_object.name
