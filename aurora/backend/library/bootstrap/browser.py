import os
from django.http import JsonResponse
from django.conf import settings


RELOAD_FILENAME = os.path.join(settings.CACHE_DIR, '.reload_signer')

def create_reload_signer():
    with open(RELOAD_FILENAME, 'w') as writer:
        writer.write("DO_AUTO_RELOAD")
        writer.close()


def auto_reload(request):
    response = {'auto_reload': False}
    if request.is_ajax():
        debug = request.POST.get('debug')
        if debug == 'auto_reload':
            if os.path.isfile(RELOAD_FILENAME):
                response['auto_reload'] = True
                os.remove(RELOAD_FILENAME)
    return JsonResponse(response)
