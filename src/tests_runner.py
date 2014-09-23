# -*- coding: utf-8 -*-


__author__ = "K. Kulikov"
__date__ = "$Jun 06, 2014 10:30:15 AM$"


import doctest
from rissile.tools import angles
from rissile.tools import assistants
from rissile.tools import quaternion
from rissile.tools import vector
from rissile.wo import world_object
from rissile.wo import data_generator


def start_doc_strings_testing():
    print(u'START DOCS TESTING')
    print(doctest.testmod(vector))
    print(doctest.testmod(assistants))
    print(doctest.testmod(angles))
    print(doctest.testmod(quaternion))
    print(doctest.testmod(world_object))
    print(doctest.testmod(data_generator))
    print(u'END DOCS TESTING')


import unittest
def start_unittesting():
    suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    start_doc_strings_testing()
    start_unittesting()