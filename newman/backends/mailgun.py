#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the mailgun mailer backend.
"""

import os
import requests
import logging
from newman.backends.backend import MailerBackend

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"


class MailGunBackend(MailerBackend):
    def __init__(self, settings):
        """
        Initializes the backend. Gets as input a dictionary with settings.
        At the moment the only settings that have to be specified are:
        "MAILGUN_API_KEY" and "MAILGUN_SANDBOX_URL".

        Parameters:
            settings (dict): {"MAILGUN_API_KEY": "...", "MAILGUN_SANDBOX_URL", "..."}
        """
        self.api_key = settings['MAILGUN_API_KEY']
        self.sandbox_url = settings['MAILGUN_SANDBOX_URL']

    def send(self, from_email, to_emails, subject, body):
        """
        Sends an email. 
        
        Parameters:
            from_email (str): the sender email
            to_emails (list): a list of recipients
            subject (str): subject
            body (str): body
        Returns:
            True in case of success, false in case of failure
        """

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox_url)
        request = requests.post(request_url, auth=('api', self.api_key), data={
            'from': from_email,
            'to': to_emails,
            'subject': subject,
            'text': body
        })
        success = request.status_code == 200 
        if not success:
            logging.warning("Mailgun failed with status code: %d" % request.status_code)
        return success


