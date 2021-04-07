import random
import string
# from django.utils.text import slugify


# funtion for otp


def random_string_otp_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_otp_generator(instance):
    order_new_otp = random_string_otp_generator()

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(otp=order_new_otp).exists()
    if qs_exists:
        return unique_otp_generator(instance)
    return order_new_otp
