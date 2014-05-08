# vim: set fileencoding=utf-8

from .. import utils


class BaseParser(object):
    def __init__(self, eactivities):
        self.eactivities = eactivities

    @classmethod
    def fetch(cls, eactivities, **kwargs):
        return cls(eactivities).fetch_data(**kwargs)

    def parse_field(self, soup, alias, type='text', cell=False, form=False, form_datum=False):
        dt = {
            # I don't even, why does eActivities use \r for linebreaks?
            'text': lambda x: unicode(x).replace('\r\n', '\n').replace('\r', '\n'),
            'date': utils.parse_date,
            'datetime': utils.parse_datetime,
            'money': utils.format_price,
            'number': float,
            'int': int,
            'bit': lambda x: x.strip() == '1',
            'vat': utils.format_vat,
            'account': utils.split_account_bracket,
            'status': lambda x: x.replace(' ', '_').upper()
        }

        element = 'infofield'
        search = {'alias': alias}
        get_value = lambda x: x.get_text()
        if cell:
            element = 'infotablecell'
        elif form:
            element = 'field'
            search = {'name': alias}
            get_value = lambda x: x.attrs['value']
            if form_datum:
                get_value = lambda x: x.attrs['datum']

        x = soup.find(element, attrs=search)
        x_val = None if not x else get_value(x)

        if not x or x_val == u'\xa0':
            # don't even ask why eActivities \xa0 when it's "NULL" or whatever its equivalent is
            return None

        return dt[type](x_val)

    def image(self, image_id, **kwargs):
        self.fetch_data(**kwargs)
        return self.eactivities.file_handler(image_id)

    def pdf(self, image_id, **kwargs):
        """
        This function is slightly misnamed.
        It returns the "original file" for image_id.
        """
        self.fetch_data(**kwargs)
        return self.eactivities.file_handler(image_id, override=True)
