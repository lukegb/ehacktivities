import functools

from flask import request, g, abort, Response

from eactivities import EActivities, exceptions

from . import sess_encoder


def login_required(must_create_eactivities=True):
    def fun(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            ah = request.headers.get('Authorization')
            if not ah or not ah.startswith('Token '):
                return abort(401)

            token = str(ah[len('Token '):])
            try:
                u = sess_encoder.decode(token)
            except Exception:
                return abort(401)

            g.user = u
            try:
                g.eactivities = EActivities(session=u['session'])
            except exceptions.NotLoggedIn:
                if must_create_eactivities:
                    return Response('Credentials must be provided.', 449)

            return f(*args, **kwargs)
        return inner
    return fun
