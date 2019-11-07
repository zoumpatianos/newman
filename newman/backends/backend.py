#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains an abstract mailer backend implementation.
"""

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class MailerBackend(object):
    """ Abstract mailer backend class """

    def send(self, from_email, to_emails, subject, body):
        """ Sub-classes should send emails using this function """
        pass