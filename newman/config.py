#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the configuration for newman mailer.
"""

import os

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

Configuration = {
    "DEFAULT": {
        "MessageBroker": {"host": "0.0.0.0", "port": 11300},
        "HttpFrontend": {"host": "0.0.0.0", "port": 8080, "debug": False},
        "Backends": {
            "MailGun": {
                "ACTIVE": True,
                "MAILGUN_API_KEY": "",
                "MAILGUN_SANDBOX_URL": "" 
            }, 
            "SendGrid": {
                "ACTIVE": True,
                "SENDGRID_API_KEY": "SG."
            },
            "SparkPost": {
                "ACTIVE": True,
                "SPARKPOST_API_KEY": ""
            }
        },
        "Workers": 10
    }
}