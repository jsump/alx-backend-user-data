#!/usr/bin/env python3
"""
Module: filtered_logger.py

Return log message obfuscated
"""


import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        for field in self.fields:
            record.msg = self.filter_datum(
                    field, self.REDACTION, record.msg, self.SEPARATOR)
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
