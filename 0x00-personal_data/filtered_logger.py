#!/usr/bin/env python3
"""Filter the logs"""
from typing import List
import re
from os import getenv
import mysql.connector
import logging


PIL_FIELDS = ('name', 'email',' phone', 'ssn','password', 'ip')

def filter_datum(fields: List[str], redaction: str, messages: str, separator: str):
    """fileter data"""
    for field in fields:
        pattern = rf"(?<={field}=)(.*?)(?={separator})"
        messages = re.sub(pattern, redaction, messages)
    return messages

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.field = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the string with redaction"""
        log_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.field, RedactingFormatter.REDACTION, log_message, RedactingFormatter.SEPARATOR)
    

def get_logger()-> logging.Logger:
    """returns a logging.logger object and takes no argumnebt"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PIL_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """connect to a database"""
    user = getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    pwd = getenv('PERSONAL_DATA_DB_PASSWORD')or ""
    host = getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db = getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(user=user, password=pwd,
                                   host=host, database=db)
    return conn



