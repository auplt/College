from datetime import datetime


class DateConverter:
    regex = '[0-9]{2}.[0-9]{2}.[0-9]{4}'
    format = '%d.%m.%Y'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)