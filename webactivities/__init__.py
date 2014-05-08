import os

from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

app.config.from_object('webactivities.default_settings')
if os.getenv('WEBACTIVITIES_SETTINGS'):
    app.config.from_envvar('WEBACTIVITIES_SETTINGS')

from . import session
sess_encoder = session.ChainingEncoder([
    session.JsonSessionDataEncoder(),
    session.SessionDataEncryptor(app.config['FERNET_KEY'], lifetime=app.config['FERNET_TTL']),
])

from . import resources
__all__ = ['app', 'resources']
