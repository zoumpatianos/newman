#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains an abstract frontend definition.
A frontend listens for incoming jobs and propagates them to the broker
"""

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class MailerFrontend(object):
    """
    This is an abstract frontend
    
    Arguments:
        broker: A broker for the messages to be propagated to.
    """

    def __init__(self, broker):
        """
        Initialize the class with a given broker.
        
        Parameters:
            broker: A given broker where the messages are propagated to.
        """

        self.broker = broker

    def start(self, settings):
        """
        Starts the frontend.
        To be implemented by sub-classes.
        """
        raise("Not yet implemented")