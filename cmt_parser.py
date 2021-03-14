# coding = utf-8

import sys
import os

# make soure pycparser are contained by PYTHONPATH
sys.path.extend([os.getcwd() + os.sep + 'pycparser'])

from pycparser import c_parser, c_ast, parse_file


# A simple visitor for CommentCond nodes that prints the struct 
# of Conditional Comment.
class CommentCondVisitor(c_ast.NodeVisitor):
    def __init__(self, dot_fp):
        '''
            initialization
        '''
        c_ast.NodeVisitor.__init__(self)
        self.dot_fp = dot_fp
        self.reset()

    def reset(self):
        '''
            reset all parameters
        '''
        self.nodeInfo = dict()
        self.edgeInfo = list()
        self.currentParent = None
        self.nodeGVN = 0
    
    def genNewNode(self, type_name, label_name):
        '''
            generate new node
        '''
        shape = 'box'
        if type_name == 'start':
            shape = 'Mdiamond'
        elif type_name == '#cond':
            shape = 'diamond'
        self.nodeGVN += 1
        return 'node%d'%self.nodeGVN, 'shape=%s,label=%s'%(shape, str(label_name)) 


    def visit_FuncDef(self, node):
        # print('%s at %s' % (node.decl.name, node.decl.coord))
        start_name, start_info = self.genNewNode('start', node.decl.name)
        self.nodeInfo[start_name] = start_info
        self.currentParent = start_name

        for child in node:
            self.visit(child)
        
        self.node_to_dot(node.decl.name)
        self.nodeInfo.clear()
    
    def visit_Compound(self, node):
        '''
            visit Compound Node
        '''
        for child in node:
            self.visit(child)
    
    def visit_If(self, node):
        '''
            visit If node
        '''
        tmpParent = self.currentParent
        
        if node.iftrue:
            self.currentParent = tmpParent
            self.visit(node.iftrue)
        if node.iffalse:
            self.currentParent = tmpParent
            self.visit(node.iffalse)
        self.currentParent = tmpParent
    
    def visit_Switch(self, node):
        '''
            visit switch node
        '''
        tmpParent = self.currentParent

        child = node.stmt

        if child and isinstance(child, c_ast.Compound):
            for subchild in child:
                self.currentParent = tmpParent
                self.visit(subchild)
            self.currentParent = tmpParent


    def visit_CommentCond(self, node):
        # print(node.type + '->' + node.name)
        newNodeName, newNodeInfo = self.genNewNode(node.type, node.name)
        self.nodeInfo[newNodeName] = newNodeInfo
        self.edgeInfo.append((self.currentParent, newNodeName))
        self.currentParent = newNodeName
    
    def node_to_dot(self, name):
        '''
            dot render/output
        '''
        if self.dot_fp is None:
            return
        self.dot_fp.write('subgraph %s{\n'%name)
        self.dot_fp.write('label = %s;\n'%name)
        self.dot_fp.write('stype = dotted;\n')
        for node_name, node_info in self.nodeInfo.items():
            self.dot_fp.write('%s[%s];\n'%(node_name, node_info))
        self.dot_fp.write('}\n')
    
    def edge_to_edge(self):
        if self.dot_fp is None:
            return
        for edge in self.edgeInfo:
            self.dot_fp.write('%s->%s;\n'%(edge[0], edge[1]))




def show_comment_cond_info(filename, outfile):
    # Note that cpp is used. Provide a path to your own cpp or
    # make sure one exists in PATH.
    ast = parse_file(filename, use_cpp=False,
                     cpp_args=r'-Iutils/fake_libc_include')

    with open('tmp.dot', 'w') as dot_fp:
        dot_fp.write('digraph G {\n')
        v = CommentCondVisitor(dot_fp)
        v.visit(ast)
        v.edge_to_edge()
        dot_fp.write('}')
    
    if os.path.exists('tmp.dot'):
        os.system('dot tmp.dot -Tsvg -o %s'%outfile)
        os.remove('tmp.dot')  


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python3 %s c_source_file out_put_file(svg)')
        exit(0)
    
    filename  = sys.argv[1]
    # filename = 'examples/testFunc.c'
    outfile = sys.argv[2]
    if not outfile.endswith('.svg'):
        outfile += '.svg'

    show_comment_cond_info(filename, outfile)
