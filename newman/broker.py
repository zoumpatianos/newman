#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of a message broker wrapper.
In its current version it uses beanstalkd. 

Beanstalkd notes (https://github.com/beanstalkd/): 
If started with the -b option then all pending jobs are persisted, 
thus making the system fault tolerant.
"""

import greenstalk

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class MailerBroker(object):
    """
    Wrapper for the beanstalkd queue server.
    Tries to connect to a beanstlkd server on a given host and port.

    Attributes:
        client: A greenstalk client
    """

    def __init__(self, host="127.0.0.1", port=11300):
        """
        Initializes the client, connecting to a given host and port
        """

        try:
            self.client = greenstalk.Client(host=host, port=11300)
        except:
            self.client = None
            raise
    
    def __del__(self):
        """
        Closes the connection when the broker is destroyed.
        """

        if self.client:
            self.client.close()

    def push(self, body):
        """
        Pushes a job in the queue.

        Parameters:
        body (str): The job content in JSON text.
        """

        # TODO: encrypt (to be discussed)
        self.client.put(body)

    def pull(self):
        """
        Pulls the next job from the queue.

        Returns:
            str: The job content in JSON text.
        """

        # TODO: decrypt (to be discussed)
        return self.client.reserve()

    def delete(self, job):
        """
        Deletes a given job from the queue.

        Parameters:
        job (Job): A given job to delete.
        """

        self.client.delete(job)