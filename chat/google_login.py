from django.shortcuts import redirect
from django.conf import settings


def google_login_redirect(request):
    client_id = settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"]
    redirect_uri = settings.SOCIALACCOUNT_PROVIDERS["google"]["APP"]["redirect_uri"]
    scope = "email profile"

    auth_url = f"""https://accounts.google.com/o/oauth2/v2/auth
          ?client_id={client_id}"
          &redirect_uri={redirect_uri}"
          &response_type=code"
          &scope={scope}"""

    return redirect(auth_url)
