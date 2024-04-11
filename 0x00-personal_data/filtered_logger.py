#!/usr/bin/env python3
"""
Module: filtered_logger.py

Return log message obfuscated
"""


import re
import logging
import mysql.connector
import os
from typing import List, Tuple, Optional
from mysql.connector.connection import MySQLConnection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization"""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Create correct frormat for output"""
        for field in self.fields:
            record.msg = self.filter_datum(
                    self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)

    def filter_datum(
            self,
            fields: List[str],
            redaction: str,
            message: str,
            separator: str) -> str:
        """
        This method returns the message obfuscated

        fields: list of strings representing fields to obfuscate
        redaction: string representing what fields will be obfucated
        message: string representing the log line
        separator: string representing by which character is
        separatingall fiends in the log line(message)
        """
        new_msg = re.sub(
                r'({})=([^{}]+)'.format('|'.join(fields), separator),
                lambda m: m.group(1) + '=' + redaction * min(1, len(
                    m.group(2))), message)
        return new_msg


def get_logger() -> logging.Logger:
    """
    Return logging.Logger object
    """
    logger = logging.getLogger('use_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    pii_fields = ('name', 'email', 'phone', 'ssn', 'password')
    formatter = RedactingFormatter(pii_fields)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def get_db() -> Optional[MySQLConnection]:
    """Connect to db"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if db_name:
        try:
            conn = mysql.connector.connect(
                    user=username,
                    password=password,
                    host=host,
                    database=db_name
            )
            return conn
        except mysql.connector.Error as e:
            raise ConnecionError(f"Error connecting to database: {e}")
    else:        raise ValueError("Database name not provided in environment \                variable PERSONAL_DATA_DB_NAME")


PII_FIELDS: Tuple[str, ...] = (
        'name', 'email', 'phone', 'ssn', 'password')
