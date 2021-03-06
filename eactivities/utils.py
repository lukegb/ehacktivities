# vim: set fileencoding=utf-8

import decimal
import datetime

DEFAULT_VAT = {
    'S1': decimal.Decimal('1.20'),  # Standard
    'P1': decimal.Decimal('1.20'),
    'SL': decimal.Decimal('1.05'),  # Reduced
    'PL': decimal.Decimal('1.05'),
    'S0': decimal.Decimal('1'),  # 0%
    'P0': decimal.Decimal('1'),
    'SE': decimal.Decimal('1'),  # Exempt
    'PE': decimal.Decimal('1'),
    'SN': decimal.Decimal('1'),  # No VAT
    'PN': decimal.Decimal('1'),
}


def format_year(year):
    start_year = year % 100
    end_year = (int(start_year) + 1) % 100
    return "%02d-%02d" % (start_year, end_year)


def split_account_bracket(bracketed_text):
    thing_name, thing_id = split_role(bracketed_text)
    return {'id': thing_id, 'name': thing_name}


def format_vat(vat_str):
    vat_type, vat_rate = split_role(vat_str)
    vat_type = vat_type[:vat_type.find(' ')]

    vat_rate = ''.join([
        x for x in unicode(vat_rate) if x in '0123456789.-'
    ])
    if vat_rate != '':
        dvat_rate = decimal.Decimal(vat_rate)
        dvat_rate /= 100
        dvat_rate += 1
    else:
        dvat_rate = DEFAULT_VAT[vat_type]

    return {'rate': vat_type, 'value': dvat_rate}


def munge_value(value):
    if 'vat' not in value:
        return value

    if 'gross' in value and 'net' in value:
        return value
    elif 'gross' in value:
        dgross = decimal.Decimal(value['gross'])
        dnet = dgross / value['vat']['value']
        value['net'] = dnet
    elif 'net' in value:
        dnet = decimal.Decimal(value['net'])
        dgross = dnet * value['vat']['value']
        value['gross'] = dgross

    return value


def split_role(text):
    pos = len(text)
    cnt = 0
    for c in text[::-1]:
        pos -= 1
        if c == ')':
            cnt += 1
        elif c == '(':
            cnt -= 1
        if cnt == 0:
            return text[:pos - 1], text[pos + 1:-1]
        elif cnt < 0:
            raise ValueError("BRACKETS MISMATCH")
    raise ValueError("Couldn't find brackets enclosed value?!?")


def format_price(text_price):
    price = u''.join([
        x for x in unicode(text_price) if x in u'0123456789.-'
    ])
    if price == '':
        return None
    return decimal.Decimal(price)


def quantize_decimal(dprice):
    return int(dprice.quantize(
        decimal.Decimal('1.'), rounding=decimal.ROUND_HALF_UP
    ))


def output_money(dprice):
    return quantize_decimal(dprice * 100)


def parse_date(date):
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y").date()
    except UnicodeEncodeError:
        return None


def parse_datetime(date):
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
    except UnicodeEncodeError:
        return None


def marshal(data):
    if isinstance(data, dict):
        out = {}
        for k, v in data.iteritems():
            out[marshal(k)] = marshal(v)
        return out
    elif isinstance(data, list):
        out = []
        for v in data:
            out.append(marshal(v))
        return out
    elif isinstance(data, decimal.Decimal):
        # assume money
        return output_money(data)
    elif isinstance(data, datetime.datetime) or \
            isinstance(data, datetime.date) or \
            isinstance(data, datetime.time):
        return data.isoformat()
    else:
        return data
