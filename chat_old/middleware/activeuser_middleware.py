import datetime
from django.core.cache import cache
from django.conf import settings
print('hrejbnjk')
class ActiveUserMiddleware:

    def process_request(self, request):
        current_user = request.user
        print(current_user)
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            print(now)
            cache.set('seen_%s' % (current_user.username), now, 
                           settings.USER_LASTSEEN_TIMEOUT)