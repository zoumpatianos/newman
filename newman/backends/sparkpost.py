#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the sparkpost mailer backend.
"""

import os
import logging
from newman.backends.backend import MailerBackend
from sparkpost import SparkPost
from sparkpost import SparkPostException

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class SparkPostBackend(MailerBackend):
    """
    This is the sparkpost backend class, it gets as input a settings vector
    that contains the API key, and initializes a client.
    """

    def __init__(self, settings):
        """
        Initializes the backend. Gets as input a dictionary with settings.
        At the moment the only setting that has to be specified is the:
        "SPARKPOST_API_KEY".

        Parameters:
            settings (dict): {"SPARKPOST_API_KEY": "...."}
        """

        self.client = SparkPost(settings['SPARKPOST_API_KEY'])

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

        try:
            response = self.client.transmissions.send(
                        use_sandbox=False,
                        recipients=to_emails,
                        html=body,
                        from_email=from_email,
                        subject=subject
                        )
            return True
        except SparkPostException as e:
            logging.warning(str(e).replace("\n", " "))
            return False
