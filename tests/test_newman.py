#!/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests the worker class.
"""
import unittest
import json
from newman.backends.backend import MailerBackend
from newman.broker import MailerBroker
from newman.worker import MailerWorker
from newman.config import Configuration

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class FakeBackend(MailerBackend):
    emails = []
    def send(self, from_email, to_emails, subject, body):
        self.emails += [[from_email, to_emails, subject, body]]
        return True

class NewmanTests(unittest.TestCase):
    def test_broker(self):
        """ Tests if the broker works as expected """

        # Start a broker and place 100 emails 
        broker = MailerBroker(**Configuration["DEFAULT"]["MessageBroker"])
        for i in range(100):
            message = {"from_email": "test@test.tst", 
                       "to_emails": ["dest@test.tst", "dest2@test.tst"], 
                       "subject": "testsubj-" + str(i), 
                       "body": "testbody-" + str(i)}
            broker.push(json.dumps(message))
        # Test that we can retrieve them
        for i in range(100):
            message = broker.pull()
            message_dict = json.loads(message.body)
            self.assertEqual(message_dict["subject"], "testsubj-" + str(i))
            self.assertEqual(message_dict["body"], "testbody-" + str(i))
            broker.delete(message)

    def test_worker(self):
        """ Tests if the worker works as expected """

        # Create a broker and place 100 emails in it
        broker = MailerBroker(**Configuration["DEFAULT"]["MessageBroker"])
        for i in range(100):
            message = {"from_email": "test@test.tst", 
                       "to_emails": ["dest@test.tst", "dest2@test.tst"], 
                       "subject": "testsubj-" + str(i), 
                       "body": "testbody-" + str(i)}
            broker.push(json.dumps(message))
        # Create a fake backend and make sure that it processed all of them
        fake = FakeBackend()
        backends = {}
        backends["fake"] = fake
        for i in range(100):
            MailerWorker.handle_next(broker, backends)
        for i in range(len(fake.emails)):
            email = fake.emails[i]
            self.assertEqual(email[0], "test@test.tst")
            self.assertEqual(email[1], ["dest@test.tst", "dest2@test.tst"])
            self.assertEqual(email[2], "testsubj-" + str(i))
            self.assertEqual(email[3], "testbody-" + str(i))
            


if __name__ == '__main__':
    unittest.main()