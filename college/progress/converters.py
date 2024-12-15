from datetime import datetime


class DateConverter:
    regex = '[0-9]{2}.[0-9]{2}'
    format = '%d.%m'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

