import sys, os, cStringIO
import time
import util, optparse

this_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(this_dir, 'krakatau/Krakatau'))

import Krakatau.ssa
from Krakatau.environment import Environment
from Krakatau.java import javaclass
from Krakatau.verifier.inference_verifier import verifyBytecode


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

def decompileClass():
    path = [os.path.join(this_dir, 'krakatau/rt.jar')]
    targets = ['javax/swing/plaf/nimbus/ToolBarSouthState']
    e = Environment()
    for part in path:
        e.addToPath(part)

    with e:
        for i,target in enumerate(targets):
            for _ in range(100):
                c = e.getClass(target)
                source = javaclass.generateAST(c, makeGraph).print_()


WARMUP_ITERATIONS = 30 # Krakatau needs a number of iterations to warmup...

def main(n):
    l = []
    old_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    try:
        for i in range(WARMUP_ITERATIONS + n):
            t0 = time.time()
            for j in range(4):
                decompileClass()
            time_elapsed = time.time() - t0
            l.append(time_elapsed)
    finally:
        sys.stdout = old_stdout
    return l[WARMUP_ITERATIONS:]

if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the krakatau benchmark")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
