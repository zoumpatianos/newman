#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains an abstract frontend definition.
A frontend listens for incoming jobs and propagates them to the broker
"""

import re
import json as pyjson
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text, json
from newman.frontends.frontend import MailerFrontend

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

# This regex is used to control if an email address is valid or not
VALID_EMAIL_REGEX = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")

class HTTPFrontendView(HTTPMethodView):
    """ HTTP email frontend service accepts a get request and brokers it to the workers. """

    def get(self, request):
        """
        Reads an email message submitted using a get request and propagates to the broker.
        
        Parameters:
            request: The get request contents.
        """

        # Prepair brokered message
        message = {"from_email": "", "to_emails": [], "subject": "", "body": ""}
        
        # Check input arguments
        args = request.args
        errors = []
        
        # Check "from" email
        if "from" not in args:
            errors.append("Missing from email")
        else:
            if not VALID_EMAIL_REGEX.match(args["from"][0]):
                errors.append("From email is not valid")
            else:
                message["from_email"] = args["from"][0]
        
        # Check "to" email
        if "to" not in args:
            errors.append("Missing to email")
        else:
            for email in args["to"]:
                if not VALID_EMAIL_REGEX.match(email):
                    errors.append("To email is not valid")
                else:
                    message["to_emails"] += [email]

        # Check subject and body
        if "subject" not in args:
            errors.append("Missing subject")
        else:
            message["subject"] = args["subject"][0] # Here we may need to do some sanitization?
        if "body" not in args:
            errors.append("Missing body")
        else:
            message["body"] = args["body"][0] # Here we may need to do some sanitization?
        
        # If no errors found, deliver the message to the broker for consumption
        if not errors:
            status = "sending"
            HTTPFrontendView.broker.push(pyjson.dumps(message))
        else:
            status = "error"

        return json({"status": status, "errors": errors})


class HTTPFrontend(MailerFrontend):
    """
    This class listens to a given port and on a given hostname, serving the HTTP api.
    """

    def start(self, settings={"host":"0.0.0.0", "port":"8000", "debug": False}):
        """ 
        This function starts the web server, listening to a given port.
        
        Parameters:
            settings (dict): A dictionary with settings, 
                             including the keys "host": str, "port": str and "debug": bool
        """
        if "host" not in settings:
            raise("No hostname set for HTTP frontend")
        if "host" not in settings:
            raise("No port set for HTTP frontend")
        if "debug" not in settings:
            settings["debug"] = False
        mailer_app = Sanic('mailer')
        HTTPFrontendView.broker = self.broker
        mailer_app.add_route(HTTPFrontendView.as_view(), '/')
        mailer_app.run(settings["host"], settings["port"], settings["debug"])