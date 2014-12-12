import os.path
import time, random

import Krakatau
import Krakatau.ssa
from Krakatau.environment import Environment
from Krakatau.java import javaclass
from Krakatau.verifier.inference_verifier import verifyBytecode
from Krakatau import script_util
from util import Timer

def makeGraph(m):
    v = verifyBytecode(m.code)
    s = Krakatau.ssa.ssaFromVerified(m.code, v)

    # print _stats(s)
    if s.procs:
        # s.mergeSingleSuccessorBlocks()
        # s.removeUnusedVariables()
        s.inlineSubprocs()

    s.condenseBlocks()
    s.mergeSingleSuccessorBlocks()
    # print _stats(s)
    s.removeUnusedVariables()
    s.constraintPropagation()
    s.disconnectConstantVariables()
    s.simplifyJumps()
    s.mergeSingleSuccessorBlocks()
    s.removeUnusedVariables()
    # print _stats(s)
    return s

def decompileClass(path=[], targets=None):
    e = Environment()
    for part in path:
        e.addToPath(part)

    with e, Timer('warming up'):
        for i,target in enumerate(targets):
            for _ in range(100):
                c = e.getClass(target)
                source = javaclass.generateAST(c, makeGraph).print_()

    with e, Timer('testing'):
        for i,target in enumerate(targets):
            for _ in range(500):
                c = e.getClass(target)
                source = javaclass.generateAST(c, makeGraph).print_()

if __name__== "__main__":
    print 'Krakatau  Copyright (C) 2012-13  Robert Grosse'

    import argparse
    parser = argparse.ArgumentParser(description='Krakatau decompiler and bytecode analysis tool')
    parser.add_argument('-path',action='append',help='Semicolon seperated paths or jars to search when loading classes')
    args = parser.parse_args()

    path = []
    if args.path:
        for part in args.path:
            path.extend(part.split(';'))

    targets = ['javax/swing/plaf/nimbus/ToolBarSouthState']
    for i in range(5):
        decompileClass(path, targets)
