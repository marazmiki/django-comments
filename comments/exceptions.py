# -*- coding: utf-8 -*-

class AlreadyRegistered(Exception):
    """
    Raise when tries to register plugin that has being registered
    """

class NoSuchPlugin(Exception):
    """
    Raises when tries get non-existant plugin class
    """

