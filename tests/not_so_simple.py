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
#        print matcher._tree1._dom.toprettyxml(' ')
#        print matcher._tree2._dom.toprettyxml(' ')
        s = matcher.get_opcodes()
#        print matcher._tree1._dom.toprettyxml(' ')
#        for o in s: print o
#        print len(s)
        s = matcher.get_opcodes()
#        print len(s)
        self.assertEqual(len(s), 0,
                         "Script is not accurate. "
                         "Second run returned a script (%d)" % len(s))
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        xml_file2 = sys.argv.pop(-1)
        xml_file1 = sys.argv.pop(-1)
    unittest.main()
