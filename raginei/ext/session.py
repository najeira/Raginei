# -*- coding: utf-8 -*-

import datetime
from werkzeug.contrib.securecookie import SecureCookie
from raginei.app import current_app, request, local, request_middleware, response_middleware


@request_middleware
def load_session_from_cookie(request):
  secret = current_app.config.get('session_secret')
  if secret:
    local.session = SecureCookie.load_cookie(request,
      current_app.config.get('session_cookie_name') or 'session', secret_key=secret)


@response_middleware
def save_session_to_cookie(response):
  secret = current_app.config.get('session_secret')
  if secret:
    session = local.session
    if session:
      if not isinstance(session, SecureCookie):
        session = SecureCookie(session, secret)
      expires = None
      lifetime = current_app.config.get('session_lifetime')
      if lifetime:
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=lifetime)
      session.save_cookie(response,
        current_app.config.get('session_cookie_name') or 'session', expires=expires)


def flash(message, category='message'):
  local.session.setdefault('_flashes', []).append((category, message))


def get_flashed_messages(with_categories=False):
  try:
    flashes = request._flashes
  except AttributeError:
    flashes = request._flashes = local.session.pop('_flashes', [])
  if not with_categories:
    return [x[1] for x in flashes]
  return flashes