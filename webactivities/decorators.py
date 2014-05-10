import functools

from flask import request, g, Response
from flask.ext.restful import abort

from eactivities import EActivities, exceptions

from . import sess_encoder

REQUIRES_AUTHENTICATION_RESPONSE = Response(status=401, headers={
    'WWW-Authenticate': 'Token realm="eHacktivities"'
})


def login_required(must_create_eactivities=True):
    def fun(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            ah = request.headers.get('Authorization')
            if not ah or not ah.startswith('Token '):
                return REQUIRES_AUTHENTICATION_RESPONSE

            token = str(ah[len('Token '):])
            try:
                u = sess_encoder.decode(token)
            except Exception:
                return REQUIRES_AUTHENTICATION_RESPONSE

            g.user = u
            try:
                g.eactivities = EActivities(session=u['session'])
            except exceptions.NotLoggedIn:
                if must_create_eactivities:
                    return Response('Credentials must be provided.', 449)

            return f(*args, **kwargs)
        return inner
    return fun


def select_role(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        chosen_role = request.headers.get('X-EHacktivities-Role', None)

        if hasattr(g, "eactivities") and chosen_role is not None:
            g.eactivities.switch_role(chosen_role)

        return f(*args, **kwargs)
    return inner


def error_catcher(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except exceptions.DoesNotExist:
            return abort(404)
        except exceptions.AccessDenied:
            return REQUIRES_AUTHENTICATION_RESPONSE
        except exceptions.EActivitiesHasChanged:
            return abort(502)
        except exceptions.EActivitiesError:
            return abort(502)
    return inner
