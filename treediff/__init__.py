from tree_matcher import TreeMatcher
from dom_tree_matcher import DomTreeMatcher

if __name__ == '__main__':
    def test_trees():
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
        return T1, T2

    def walk_raw_tree(tree, indent=0):
        print ' '*indent, tree[0], tree[1]
        for n in tree[2]:
            walk_raw_tree(n, indent+1)

    from visualizer import VisualTreeMatcher
    t1, t2 = test_trees()
#    walk_raw_tree(t2)
    matcher = VisualTreeMatcher(t2, t1)
#    matcher._match()
#    matcher.draw_trees(True)
    s = matcher.get_opcodes()
    for op in s:
        print op
    
