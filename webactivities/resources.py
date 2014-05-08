import datetime
import dateutil.parser

from flask import request, Response, g
from flask.ext import restful

from eactivities import EActivities
from eactivities.exceptions import AuthenticationFailed

from . import app, api, sess_encoder
from .decorators import login_required


def create_token(username, password):
    e = EActivities(credentials=(username, password))
    session = e.session.cookies['ICU_eActivities']
    now = datetime.datetime.utcnow()
    expiry = now + datetime.timedelta(seconds=app.config['FERNET_TTL'])

    return sess_encoder.encode({
        'username': username,
        'password': password,
        'session': session,
        'created': now.isoformat()
    }), expiry


class Resource(restful.Resource):
    method_decorators = [login_required]


class Session(restful.Resource):
    @login_required()
    def get(self):
        created = dateutil.parser.parse(g.user['created'])
        return {
            'username': g.user['username'],
            'created': g.user['created'],
            'expires': (created + datetime.timedelta(seconds=app.config['FERNET_TTL'])).isoformat()
        }

    def post(self):
        auth = request.authorization
        if not auth:
            return Response('Credentials must be provided.', 401, {'WWW-Authenticate': 'Basic realm="eHacktivities"'})

        try:
            token, expiry = create_token(auth.username, auth.password)
        except AuthenticationFailed:
            return Response('Invalid password. You suck.', 401, {'WWW-Authenticate': 'Basic realm="eHacktivities"'})

        return {
            'token': token,
            'expires': expiry.isoformat()
        }

    @login_required(must_create_eactivities=False)
    def put(self):
        try:
            g.eactivities.logout()
        except:
            pass  # you know, I don't really care

        try:
            token, expiry = create_token(g.user['username'], g.user['password'])
        except AuthenticationFailed:
            return Response('Token is now invalid (possibly because you changed your password). Oops.', 401, {})

        return {
            'token': token,
            'expires': expiry.isoformat()
        }

    @login_required()
    def delete(self):
        g.eactivities.logout()

api.add_resource(Session, '/session')
