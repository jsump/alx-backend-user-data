#!/usr/bin/env pythin3
"""
Module: filtered_logger.py

Return log message obfuscated
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    This method returns the message obfuscated
    """
    pattern = re.compile(
            r'({})=([^{}]+)'.format('|'.join(fields), separator))
    return pattern.sub(
            lambda m: m.group(1) + '=' + redaction * len(m.group(2)),
            message
        )
