#!/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of file based monitor.
It records all requests in a file.
"""

__author__ = "Kostas Zoumpatianos"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "zoumbatianos@gmail.com"

class FileBasedMonitor(object):
    """ Implementation of a file based monitor, stores all requests in a file """
    
    def __init__(self, filename):
        """ 
        Constructor with a filename as an argument 
        Parameters:
            filename (str): the target filename
        """
        self.filename = filename
        self.file = open(filename, "w")
        
    def __del__(self):
        """
        Destructor: closes the file.
        """

        self.file.close()
        
    def record(self, backend, job_id, status):
        """
        Writes the status of a job for a given backend in a file.
        
        Parameters:
            backend (str): the backend name
            job_id (int): the job id
            status (bool): the status of the job
        """
        self.file.write("%s;%d;%r\n" % (backend, job_id, status))
        self.file.flush()