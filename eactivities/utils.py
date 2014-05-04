# vim: set fileencoding=utf-8

import decimal
import datetime


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
    dvat_rate = decimal.Decimal(vat_rate)
    dvat_rate /= 100
    dvat_rate += 1

    return {'rate': vat_type, 'value': dvat_rate}


def munge_value(value):
    if 'vat' not in value:
        return value

    if 'gross' in value and 'net' in value:
        return value
    elif 'gross' in value:
        dgross = decimal.Decimal(value['gross'])
        dnet = dgross / value['vat']['value']
        value['net'] = quantize_decimal(dnet)
    elif 'net' in value:
        dnet = decimal.Decimal(value['net'])
        dgross = dnet * value['vat']['value']
        value['gross'] = quantize_decimal(dgross)

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
            return text[:pos-1], text[pos+1:-1]
        elif cnt < 0:
            raise ValueError("BRACKETS MISMATCH")
    raise ValueError("Couldn't find brackets enclosed value?!?")


def format_price(text_price):
    price = u''.join([
        x for x in unicode(text_price) if x in u'0123456789.-'
    ])
    return decimal.Decimal(price)


def quantize_decimal(dprice):
    return int(dprice.quantize(
        decimal.Decimal('1.'), rounding=decimal.ROUND_HALF_UP
    ))


def parse_date(date):
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y").date()
    except UnicodeEncodeError:
        return None