import codecs
import csv

""" Utilities to read eActivities CSVs with correct character encodings """


class EActivitiesEncodingRecoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('cp850').decode('iso8859-1').encode("utf-8")


class EActivitiesCsvReader(object):

    def __init__(self, f, dialect=csv.excel, encoding="iso8859-1", **kwds):
        f = EActivitiesEncodingRecoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

    @property
    def line_num(self):
        return self.reader.line_num


class EActivitiesDictCsvReader(csv.DictReader):
    def __init__(
        self, f, fieldnames=None, restkey=None, restval=None, dialect="excel",
        encoding="iso8859-1",
        *args, **kwargs
    ):
        csv.DictReader.__init__(
            self,
            f, fieldnames, restkey, restval, dialect, *args, **kwargs
        )
        self.reader = EActivitiesCsvReader(f, dialect, encoding, *args, **kwargs)
