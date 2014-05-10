import datetime
import dateutil.parser

from flask import request, Response, g
from flask.ext import restful

from eactivities import EActivities
from eactivities.exceptions import AuthenticationFailed
from eactivities.models import PdfableModelMixin

from . import app, api, sess_encoder
from .decorators import login_required, select_role, error_catcher


def this_year():
    now = datetime.datetime.utcnow()
    year = now.year
    if now.month < 9:
        year -= 1
    return year


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
    method_decorators = [error_catcher, select_role, login_required()]


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


class Roles(Resource):
    def get(self):
        raw_roles = g.eactivities.roles()
        out_roles = [{k: v for (k, v) in x.items() if k in ('committee', 'id', 'position')} for x in raw_roles.values()]
        return out_roles


class Clubs(Resource):
    def get(self):
        restful.abort(501)


class Club(Resource):
    def get(self, club_id):
        return g.eactivities.club(club_id).marshal()


class Finances(Resource):
    def get(self, club_id, year):
        return g.eactivities.club(club_id).finances(year).marshal(trim_attributes=('club_id', 'year'))


class FinancialDocumentCollectionResource(Resource):
    documents = {
        'internal-charges': 'internal_charges',
        'transaction-corrections': 'transaction_corrections',
        'purchase-orders': 'purchase_orders',
        'claims': 'claims',
        'banking-records': 'banking_records',
        'sales-invoices': 'sales_invoices'
    }
    pdfable_documents = [
        'purchase-orders', 'sales-invoices'
    ]

    def get(self, club_id, year, document):
        if document not in self.documents.keys():
            restful.abort(404)

        finances = g.eactivities.club(club_id).finances(year)
        docs = getattr(finances, self.documents[document])()

        return docs.marshal(lazy_load=False, trim_attributes=('club_id', 'year'))

    def streaming_response(self, raw_resp, content_type=None):
        # eActivities occasionally makes up content types (e.g. application/x-download)
        content_type = content_type or raw_resp.headers['content-type']

        def generate():
            for chunk in raw_resp.iter_content(1024):
                yield chunk

        return Response(generate(), mimetype=content_type)


class FinancialDocumentResource(FinancialDocumentCollectionResource):
    def get(self, club_id, year, document, id):
        if document not in self.documents.keys():
            restful.abort(404)

        finances = g.eactivities.club(club_id).finances(year)
        doc = getattr(finances, self.documents[document])()[id]

        if isinstance(doc, PdfableModelMixin):
            best = request.accept_mimetypes.best_match([
                'application/pdf', 'application/json'
            ])
            if best == 'application/pdf' and \
                    request.accept_mimetypes[best] > \
                    request.accept_mimetypes['application/json']:
                return self.streaming_response(doc.pdf(), content_type='application/pdf')

        return doc.marshal(lazy_load=False, trim_attributes=('club_id', 'year'))


class FinancialDocumentAttachmentResource(FinancialDocumentResource):
    attachment_documents = {
        'claims': 'receipts',
        'purchase-orders': 'invoices',
        'sales-invoices': 'purchase_order_attachments'
    }

    def get(self, club_id, year, document, id, attachment_id):
        if document not in self.documents.keys():
            restful.abort(404)
        elif document not in self.attachment_documents.keys():
            restful.abort(404)

        finances = g.eactivities.club(club_id).finances(year)
        doc = getattr(finances, self.documents[document])()[id]
        attachments = getattr(doc, self.attachment_documents[document])
        for attachment in attachments:
            if str(attachment) == attachment_id:
                break
        else:
            restful.abort(404)

        return self.streaming_response(attachment.raw())


class MembershipList(Resource):
    def get(self, club_id, year):
        if year != this_year():
            if year < this_year():
                restful.abort(410)
            else:
                restful.abort(404)

        m_list = g.eactivities.club(club_id).membership.list(with_key_lists=True)
        out = {
            'full': [],
            'associate': []
        }
        for member in m_list.marshal():
            out[member['membership_type']].append(member)
        return out


class MembershipSubList(MembershipList):
    def get(self, club_id, year, membership_type):
        try:
            return super(MembershipSubList, self).get(club_id, year)[membership_type]
        except KeyError:
            restful.abort(404)


class Member(MembershipSubList):
    def get(self, club_id, year, membership_type, cid):
        for m in super(Member, self).get(club_id, year, membership_type):
            if m['cid'] == cid:
                return m
        else:
            restful.abort(404)


class Document(Resource):
    def get(self, club_id, year):
        if year != this_year():
            if year < this_year():
                restful.abort(410)
            else:
                restful.abort(404)

        c = g.eactivities.club(club_id).documentation()
        doc = getattr(c, self.document)()

        return doc.marshal(lazy_load=False, trim_attributes=('club_id', 'year'))


class DocumentItem(object):
    def get(self, club_id, year, id):
        for item in super(DocumentItem, self).get(club_id, year):
            if item['id'] == id:
                return item
        else:
            restful.abort(404)


class Assets(Document):
    document = 'inventory'


class Asset(DocumentItem, Assets):
    pass


class RiskAssessment(Document):
    document = 'risk_assessment'


class Risk(DocumentItem, RiskAssessment):
    pass


class KeyLists(Document):
    document = 'key_lists'

    def get(self, club_id, year):
        return super(KeyLists, self).get(club_id, year).values()


class KeyList(DocumentItem, KeyLists):
    def get(self, club_id, year, id):
        try:
            id = int(id)
            return super(KeyList, self).get(club_id, year, id)
        except ValueError:
            restful.abort(400)


class Products(Resource):
    def get(self, club_id, year):
        return g.eactivities.club(club_id).shop(year).products().marshal(lazy_load=False, trim_attributes=('club_id', 'year'))


class Product(Resource):
    def get(self, club_id, year, id):
        return g.eactivities.club(club_id).shop(year).products()[id].marshal(lazy_load=False, trim_attributes=('club_id', 'year'))


api.add_resource(Session, '/session')

api.add_resource(Roles, '/roles')

api.add_resource(Clubs, '/clubs')
api.add_resource(Club, '/clubs/<string:club_id>')

api.add_resource(Finances, '/clubs/<string:club_id>/<int:year>/finances')
api.add_resource(FinancialDocumentCollectionResource, '/clubs/<string:club_id>/<int:year>/finances/<string:document>')
api.add_resource(FinancialDocumentResource, '/clubs/<string:club_id>/<int:year>/finances/<string:document>/<string:id>')
api.add_resource(
    FinancialDocumentAttachmentResource, '/clubs/<string:club_id>/<int:year>/finances/<string:document>/<string:id>/<string:attachment_id>'
)

api.add_resource(MembershipList, '/clubs/<string:club_id>/<int:year>/members')
api.add_resource(MembershipSubList, '/clubs/<string:club_id>/<int:year>/members/<string:membership_type>')
api.add_resource(Member, '/clubs/<string:club_id>/<int:year>/members/<string:membership_type>/<string:cid>')

api.add_resource(Assets, '/clubs/<string:club_id>/<int:year>/assets')
api.add_resource(Asset, '/clubs/<string:club_id>/<int:year>/assets/<string:id>')
api.add_resource(RiskAssessment, '/clubs/<string:club_id>/<int:year>/risks')
api.add_resource(Risk, '/clubs/<string:club_id>/<int:year>/risks/<string:id>')
api.add_resource(KeyLists, '/clubs/<string:club_id>/<int:year>/keys')
api.add_resource(KeyList, '/clubs/<string:club_id>/<int:year>/keys/<string:id>')

api.add_resource(Products, '/clubs/<string:club_id>/<int:year>/products')
api.add_resource(Product, '/clubs/<string:club_id>/<int:year>/products/<string:id>')
