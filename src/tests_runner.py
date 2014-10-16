 # -*- coding: utf-8 -*-

__author__ = "K. Kulikov"
__date__ = "$Jun 06, 2014 10:30:15 AM$"

def start_doc_strings_testing():
    """
    Docs string testing.
    """
    from auxiliary import imp_py
    import doctest
    
    for module in imp_py.get_imported_py_modules('.', ('test')):
        print(doctest.testmod(module))

def start_unittesting():
    """
    Unit testing.
    """
    import unittest
    
    suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    start_doc_strings_testing()
    start_unittesting()