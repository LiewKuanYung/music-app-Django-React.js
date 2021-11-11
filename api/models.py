from django.db import models
import string
import random

# generate unique code for room model
def generate_unique_code():
    length = 6
    while True:
        # generate random code with length of 6
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        # if this code doesn't exist yet (count == 0), break
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

# room model
class Room(models.Model):
    # take note that the id field is auto generated
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models. IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


