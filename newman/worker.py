#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of a mailer worker.
It retrieves a pending email from the message broker
and sends it using a random backend. If that backend fails
it tries to select another one, until successful.
"""

import random
import logging
import json

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"


class MailerWorker(object):
    """
    This is a class that processes pending email jobs.
    It only contains static methods. Do not instantiate.
    """

    @classmethod
    def handle_next(cls, broker, backends, monitor=None):
        """
        Handles the next email in the queue.

        Parameters:
            broker: The message broker
            backends (dict): The various different backends to chose one randomly
        """

        job = broker.pull()
        job_dict = json.loads(job.body)
        sent = False
        # TODO: Here we should have a maximum retries policy. To be discussed.
        while not sent:
            chosen_backend = random.choice(list(backends.keys()))
            sent = backends[chosen_backend].send(**job_dict)
            if not sent:
                logging.warning("Job status for backend '%s' is '%r'" % (chosen_backend, sent))
            else:
                logging.info("Job status for backend '%s' is '%r'" % (chosen_backend, sent))
            if monitor:
                monitor.record(chosen_backend, job.id, sent)
        broker.delete(job)
        
    @classmethod
    def start(cls, broker, backends, monitor=None):
        """
        Starts waiting for messages in the queue to process until 
        Ctl-C is pressed.

        Parameters:
            broker: The message broker
            backends: The various different backends to chose one randomly
        """
        
        try:
            while True:
                cls.handle_next(broker, backends, monitor)
        except KeyboardInterrupt:
            pass
    