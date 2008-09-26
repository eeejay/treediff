#!/usr/bin/python

import unittest
from treediff import TreeMatcher
from treediff.script_store import ScriptOp

T1 = ['D', None, [
            ['P', None, [
                            ['S', 'a', []],
                            ['S', 'b', []],
                            ['S', 'c', []]]],
            ['P', None, [
                            ['S', 'd', []],
                            ['S', 'e', []]]], 
            ['P', None, [
                            ['S', 'f', []]]]]]

T2 = ['D', None, [
            ['P', None, [
                            ['S', 'a', []],
                            ['S', 'c', []]]],
            ['P', None, [
                            ['S', 'f', []]]],
            ['P', None, [
                            ['S', 'd', []],
                            ['S', 'e', []],
                            ['S', 'g', []]]]]]

EXPECTED_OPS = [
    ScriptOp(ScriptOp.MOVE, 
             'D:[1]/P:None', 'D:None', 2),
    ScriptOp(ScriptOp.INSERT, 
             'D:[2]/P:[2]/S:g', 'S', 'g', 'D:[2]/P:None', 2),
    ScriptOp(ScriptOp.DELETE, 
             'D:[0]/P:[1]/S:b')]

class TestSimpleTree(unittest.TestCase):
    def testtreediff(self):
        matcher = TreeMatcher(T1, T2)
        s = matcher.get_opcodes()
            
        self.assertEqual(len(s), len(EXPECTED_OPS), 
                         "Script has unexpected length.")

        for op, expected in zip(s, EXPECTED_OPS):
            self.assertEqual(op.op_type, expected.op_type,
                             "Op types don't match.")
            self.assertEqual(op.args, expected.args,
                             "Op args don't match.")

        self.assertEqual(len(matcher.get_opcodes()), 0,
                         "Script is not accurate")

if __name__ == '__main__':
    unittest.main()
