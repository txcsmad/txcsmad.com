import hashlib
import hmac

import requests
from django.conf import settings
from django.shortcuts import render


# Create your views here.
def main_app(request):
    digest = _makedigest("labs", None, settings.UTCS_API_KEY)
    response = requests.get("https://www.cs.utexas.edu/users/mad/utcs-app-backend/1.0/cgi-bin/utcs.scgi?service=labs",
                            headers={"authentication": "hmac web:" + digest})
    json_values = response.json()["values"];

    return render(request, 'labstatus/main.html', {"data": json_values})


def _makedigest(service, arg, key):
    if arg is None:
        arg = ""
    keyasbytes = key.encode()
    message = (str(service) + str(arg)).encode()
    digester = hmac.new(keyasbytes, message, hashlib.sha1)

    return digester.hexdigest()
