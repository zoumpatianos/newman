#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the sendgrid mailer backend.
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from newman.backends.backend import MailerBackend

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class SendGridBackend(MailerBackend):
    """
    This is the sendgrid backend class, it gets as input a settings vector
    that contains the API key, and initializes a client.
    """

    def __init__(self, settings):
        """
        Initializes the backend. Gets as input a dictionary with settings.
        At the moment the only setting that has to be specified is the:
        "SENDGRID_API_KEY".

        Parameters:
            settings (dict): {"SENDGRID_API_KEY": "...."}
        """
       
        self.client = SendGridAPIClient(settings['SENDGRID_API_KEY'])

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
        message = Mail(
            from_email=from_email,
            to_emails=";".join(to_emails),
            subject=subject,
            html_content=body)
        try:
            response = self.client.send(message)
            return True
        except Exception as e:
            logging.warning(str(e).replace("\n", " "))
            return False