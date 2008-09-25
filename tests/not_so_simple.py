#!/usr/bin/python

import unittest
from treediff import DomTreeMatcher
from treediff.script_store import ScriptOp
from xml.dom.minidom import parse
import os, os.path

srcroot = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.path.pardir)

xml_file1 = os.path.join(srcroot, 'samples', 'ie.xml')
xml_file2 = os.path.join(srcroot, 'samples', 'firefox3.xml')

class TestSimpleTree(unittest.TestCase):
    def testtreescript(self):
        matcher = DomTreeMatcher(parse(xml_file1), parse(xml_file2))
        s = matcher.get_opcodes()
        print len(s)
        s = matcher.get_opcodes()
        print len(s)
        self.assertEqual(len(matcher.get_opcodes()), 0,
                         "Script is not accurate")
        

if __name__ == '__main__':
    unittest.main()
