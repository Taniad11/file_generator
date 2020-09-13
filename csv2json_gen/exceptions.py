"""Custom Exceptions used while parsing CSV data"""


class InvalidArgs(BaseException):
    """Raise this exception if CSV file is not passed as arg"""


class EmptyCSV(BaseException):
    """Raise this exception if CSV file is empty"""


class InvalidCSVFormat(BaseException):
    """Raise this exception if CSV column format is invalid"""
