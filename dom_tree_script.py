from xml.dom import Node
from xml.dom.minidom import getDOMImplementation
from script_store import ScriptStore

class XupdateScriptStore(ScriptStore):
    def __init__(self, tree):
        self._tree = tree
        self._xupdate_doc = getDOMImplementation().createDocument(
            'http://www.xmldb.org/xupdate', 'xupdate:modifications', None)
        self._inserted_ancestor = None
        list.__init__(self)

    def append(self, val):
        list.append(self, val)

    def _append_instruction(self, instruction, select):
        element = self._xupdate_doc.createElement('xupdate:' + instruction)
        element.setAttribute('select', select)
        self._xupdate_doc.documentElement.appendChild(element)
        return element

    def _append_comment(self, comment):
        c = self._xupdate_doc.createComment(comment)
        self._xupdate_doc.documentElement.appendChild(c)
        return c

    def _flush_inserts(self):
        if self._inserted_ancestor:
            self._append_comment('Insert')
            sibling = self._inserted_ancestor.previousSibling
            if sibling:
                element = self._append_instruction(
                    'insert-after', 
                    self._tree.node_repr(sibling))
            else:
                element = self._append_instruction(
                    'append', 
                    self._tree.node_repr(
                        self._tree.get_parent(self._inserted_ancestor) or '/'))
            if self._inserted_ancestor.nodeType == \
                    self._inserted_ancestor.ATTRIBUTE_NODE:
                element.setAttributeNode(
                    self._inserted_ancestor.cloneNode(True))
            else:
                element.appendChild(self._inserted_ancestor.cloneNode(True))
            self._inserted_ancestor = None

    def _is_ancestor(self, node, ancestor):
        parent = self._tree.get_parent(node)
        while parent:
            if parent == ancestor:
                return True
            parent = self._tree.get_parent(parent)
        return False
            

    def move(self, node, parent, index):
        self._flush_inserts()

        self._append_comment('Move')

        element = self._append_instruction('variable', 
                                           self._tree.node_repr(node))
        element.setAttribute('name', node.nodeName.split(':')[-1])

        self._append_instruction('remove', 
                                           self._tree.node_repr(node))

        try:
            sibling = parent.childNodes[index + 1]
        except IndexError:
            element = self._append_instruction('append', 
                                     self._tree.node_repr(parent))
        else:
            element = self._append_instruction('insert-before', 
                                     self._tree.node_repr(sibling))

        val_of = self._xupdate_doc.createElement('xupdate:value-of')
        val_of.setAttribute('select', '$' + node.nodeName.split(':')[-1])
        element.appendChild(val_of)

            
        self.append(
            'MOV(%s, %s, %s)' % \
                (self._tree.node_repr(node), 
                 self._tree.node_repr(parent), index))



    def insert(self, node, label, value, parent, index):
        if not self._inserted_ancestor:
            self._inserted_ancestor = node
        elif not self._is_ancestor(node, self._inserted_ancestor):
            self._flush_inserts()

        self.append(
            'INS((%s, %s, %s), %s, %s)' % \
                (self._tree.node_repr(node), label, value, 
                 self._tree.node_repr(parent), index))

    def update(self, node, value):
        self._flush_inserts()
        self._append_comment('Update')
        element = self._append_instruction('update', self._tree.node_repr(node))

        self._flush_inserts()

        self.append('UPD(%s, %s)' % (self._tree.node_repr(node), value))

    def delete(self, node):
        self._flush_inserts()
        self._append_comment('Delete')
        element = self._append_instruction('remove', self._tree.node_repr(node))

        self.append('DEL(%s)' % self._tree.node_repr(node))

class SideBySideScript(ScriptStore):
    def __init__(self, tree):
        self._orig_tree = tree.deep_copy()
        ScriptStore.__init__(self, tree)

    def get_trees(self):
        doc = getDOMImplementation().createDocument('', 'sidebyside', None)
        left = doc.createElement('left')
        left.appendChild(self._orig_tree.get_root())
        doc.documentElement.appendChild(left)
        right = doc.createElement('right')
        right.appendChild(self._tree.get_root())
        doc.documentElement.appendChild(right)
        return doc

    def _append_comment(self, doc, comment):
        c = doc.createComment(comment)
        doc.documentElement.appendChild(c)
        return c

    def _path_template(self, doc, xpath, attribs={}):
        template = doc.createElement('xsl:template')
        template.setAttribute('match', xpath)
        copy = doc.createElement('xsl:copy')
        copy.setAttribute('select', '@*')
        template.appendChild(copy)
        for key, value in attribs.items():
            a = doc.createElement('xsl:attribute')
            a.setAttribute('name', key)
            copy.appendChild(a)
            a.appendChild(doc.createTextNode(value))
        copy.appendChild(doc.createElement('xsl:apply-templates'))
        return template

    def _node_type_from_xpath(self, xpath):
        n_str = xpath.split('/')[-1]
        if n_str.startswith('@'):
            return Node.ATTRIBUTE_NODE
        elif n_str == 'text()':
            return Node.TEXT_NODE
        else:
            return Node.ELEMENT_NODE 

    def get_xsl(self):
        doc = getDOMImplementation().createDocument(
            'http://www.w3.org/1999/XSL/Transform', 'xsl:stylesheet', None)
        # BUG: The namespace thingy doesn't work.
        doc.documentElement.setAttribute(
            'xmlns:xsl', 'http://www.w3.org/1999/XSL/Transform')
        for op in self:
            if op.op_type == op.DELETE:
                del_path = op.args[0]
                if self._node_type_from_xpath(del_path) == Node.ELEMENT_NODE:
                    self._append_comment(doc, 'Delete Element')
                    template = self._path_template(
                        doc, 'left' +del_path, {'revised' : 'deleted'})
                    doc.documentElement.appendChild(template)
                elif self._node_type_from_xpath(del_path) == Node.TEXT_NODE:
                    self._append_comment(doc, 'Delete Text')
                    del_path = del_path[:del_path.rindex('/')]
                    template = self._path_template(
                        doc, 'left' +del_path, {'revised' : 'deleted-text'})
                    doc.documentElement.appendChild(template)
                    
        self._append_comment(doc, 'Generic')
        template = self._path_template(doc, '*')
        doc.documentElement.appendChild(template)
        return doc
            

if __name__ == '__main__':
    from sys import argv
    fn = ['tests/simple_tree1.xml', 'tests/simple_tree2.xml']
    if len(argv[1:]) == 2:
        fn = argv[1:]

    from xml.dom.minidom import parse
    from dom_tree_matcher import DomTreeMatcher
    dom1 = parse(fn[0])
    dom2 = parse(fn[1])
    tm = DomTreeMatcher(dom1, dom2, script_store=SideBySideScript)
    
    s = tm.get_opcodes()
    a = open('/tmp/t.xsl', 'w')
    xsl = s.get_xsl()
    xsl.writexml(a)
    a.close()

    a = open('/tmp/t.xml', 'w')
    s.get_trees().writexml(a, ' ',' ', '\n')
    a.close()
    

