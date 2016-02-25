import os
import logging
from unladen_swallow.perf import SimpleBenchmark, MeasureGeneric
from unladen_swallow.perf import RawResult, ResultError, _FindAllBenchmarks
import subprocess

def relative(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def _register_new_bm(name, bm_name, d, **opts):
    def Measure(python, options, bench_data):
        bm_path = relative('own', name + '.py')
        return MeasureGeneric(python, options, bench_data, bm_path, **opts)
    Measure.func_name = 'Measure' + name.capitalize()

    def BM(*args, **kwds):
        return SimpleBenchmark(Measure, *args, **kwds)
    BM.func_name = 'BM_' + bm_name

    d[BM.func_name] = BM

def _register_new_bm_twisted(name, bm_name, d, **opts):
    def Measure(python, options, bench_data):
        def parser(line):
            number = float(line.split(" ")[0])
            if name == 'tcp':
                return 100*1024*1024/number
            elif name == 'iteration':
                return 10000/number
            else:
                return 100/number
        bm_path = relative('own', 'twisted', name + '.py')
        return MeasureGeneric(python, options, bench_data, bm_path,
                              parser=parser, **opts)
    Measure.func_name = 'Measure' + name.capitalize()

    def BM(*args, **kwds):
        return SimpleBenchmark(Measure, *args, **kwds)
    BM.func_name = 'BM_' + bm_name

    d[BM.func_name] = BM

def _register_new_bm_base_only(name, bm_name, d, **opts):
    def benchmark_function(python, options, bench_data):
        bm_path = relative('own', name + '.py')
        return MeasureGeneric(python, options, bench_data, bm_path, **opts)

    def BM(python, options, *args, **kwargs):
        try:
            data = benchmark_function(python, options,
                                      *args, **kwargs)
        except subprocess.CalledProcessError, e:
            return ResultError(e)
        return RawResult(data[0])
    BM.func_name = 'BM_' + bm_name

    d[BM.func_name] = BM

TWISTED = [relative('lib/twisted-trunk'), relative('lib/zope.interface-3.5.3/src'), relative('own/twisted')]

opts = {
    'pyxl_bench': {'bm_env': {'PYTHONPATH': relative('lib/pyxl')}},
    'eparse'  : {'bm_env': {'PYTHONPATH': relative('lib/monte')}},
    'bm_mako' : {'bm_env': {'PYTHONPATH': relative('lib/mako')}},
    'bm_dulwich_log': {'bm_env': {'PYTHONPATH': relative('lib/dulwich-0.9.1')}},
    'bm_chameleon': {'bm_env': {'PYTHONPATH': relative('lib/chameleon/src')}},
    'sqlalchemy_declarative': {'bm_env': {'PYTHONPATH': relative('lib/sqlalchemy/lib')}},
    'sqlalchemy_imperative': {'bm_env': {'PYTHONPATH': relative('lib/sqlalchemy/lib')}},
}

for name in ['expand', 'integrate', 'sum', 'str']:
    _register_new_bm('bm_sympy', 'sympy_' + name,
                     globals(), bm_env={'PYTHONPATH': relative('lib/sympy')},
                     extra_args=['--benchmark=' + name])

for name in ['xml', 'text']:
    _register_new_bm('bm_genshi', 'genshi_' + name,
                     globals(), bm_env={'PYTHONPATH': relative('lib/genshi')},
                     extra_args=['--benchmark=' + name])

for name in ['nbody_modified', 'meteor-contest', 'fannkuch',
             'spectral-norm', 'chaos', 'telco', 'go', 'pyflate-fast',
             'raytrace-simple', 'crypto_pyaes', 'bm_mako', 'bm_chameleon',
             'json_bench', 'pidigits', 'hexiom2', 'eparse',
             'bm_dulwich_log', 'bm_krakatau', 'bm_mdp', 'pypy_interp',
             'sqlitesynth', 'pyxl_bench', 'sqlalchemy_declarative',
             'sqlalchemy_imperative']:
    _register_new_bm(name, name, globals(), **opts.get(name, {}))

for name in ['names', 'iteration', 'tcp', 'pb', ]:#'web']:#, 'accepts']:
    _register_new_bm_twisted(name, 'twisted_' + name,
                     globals(), bm_env={'PYTHONPATH': os.pathsep.join(TWISTED)})

_register_new_bm('spitfire', 'spitfire', globals(),
    extra_args=['--benchmark=spitfire_o4'])
_register_new_bm('spitfire', 'spitfire_cstringio', globals(),
    extra_args=['--benchmark=python_cstringio'])

# =========================================================================
# translate.py benchmark
# =========================================================================

def parse_timer(lines):
    prefix = '[Timer] '
    n = len(prefix)
    lines = [line[n:] for line in lines if line.startswith(prefix)]
    timings = []
    for line in lines:
        if (line == 'Timings:' or
            line.startswith('============') or
            line.startswith('Total:') or
            'stackcheck' in line):
            continue
        name, _, time = map(str.strip, line.partition('---'))
        name = name.replace('_lltype', '')
        name = name.replace('_c', '')
        assert time.endswith(' s')
        time = float(time[:-2])
        timings.append((name, time))
    return timings

def test_parse_timer():
    lines = [
        'foobar',
        '....',
        '[Timer] Timings:',
        '[Timer] annotate                       --- 1.3 s',
        '[Timer] rtype_lltype                   --- 4.6 s',
        '[Timer] stackcheckinsertion_lltype     --- 2.3 s',
        '[Timer] database_c                     --- 0.4 s',
        '[Timer] ========================================',
        '[Timer] Total:                         --- 6.3 s',
        'hello world',
        '...',
        ]
    timings = parse_timer(lines)
    assert timings == [
        ('annotate', 1.3),
        ('rtype', 4.6),
        ('database', 0.4)
        ]

def BM_translate(python, options, bench_data):
    """
    Run translate.py and returns a benchmark result for each of the phases.
    Note that we run it only with ``base_python`` (which corresponds to
    pypy-c-jit in the nightly benchmarks, we are not interested in
    ``changed_python`` (aka pypy-c-nojit) right now.
    """
    translate_py = relative('lib/pypy/rpython/bin/rpython')
    target = relative('lib/pypy/pypy/goal/targetpypystandalone.py')
    #targetnop = relative('lib/pypy/pypy/translator/goal/targetnopstandalone.py')
    args = python + [translate_py, '--source', '--dont-write-c-files', '-O2', target]
    logging.info('Running %s', ' '.join(args))
    environ = os.environ.copy()
    environ['PYTHONPATH'] = relative('lib/pypy')
    proc = subprocess.Popen(args, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, env=environ)
    out, err = proc.communicate()
    retcode = proc.poll()
    if retcode != 0:
        if out is not None:
            print '---------- stdout ----------'
            print out
        if err is not None:
            print '---------- stderr ----------'
            print err
        raise Exception("translate.py failed, retcode %r" % (retcode,))

    lines = err.splitlines()
    timings = parse_timer(lines)

    result = []
    for name, time in timings:
        data = RawResult([time])
        result.append((name, data))
    return result
BM_translate.benchmark_name = 'trans2'

def BM_cpython_doc(python, options, bench_data):
    from unladen_swallow.perf import RawResult
    import subprocess, shutil

    maindir = relative('lib/cpython-doc')
    builddir = os.path.join(os.path.join(maindir, 'tools'), 'build')
    try:
        shutil.rmtree(builddir)
    except OSError:
        pass
    build = relative('lib/cpython-doc/tools/sphinx-build.py')
    os.mkdir(builddir)
    docdir = os.path.join(builddir, 'doctrees')
    os.mkdir(docdir)
    htmldir = os.path.join(builddir, 'html')
    os.mkdir(htmldir)
    args = python + [build, '-b', 'html', '-d', docdir, maindir, htmldir]
    proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    retcode = proc.poll()
    if retcode != 0:
        print out
        print err
        raise Exception("sphinx-build.py failed")
    res = float(out.splitlines()[-1])
    return RawResult([res], None)

BM_cpython_doc.benchmark_name = 'sphinx'

# Scimark
_register_new_bm_base_only('scimark', 'scimark_SOR', globals(),
                 extra_args=['--benchmark=SOR', '100', '5000', 'Array2D'])
_register_new_bm_base_only('scimark', 'scimark_SparseMatMult', globals(),
                 extra_args=['--benchmark=SparseMatMult', '1000', '50000', '2000'])
_register_new_bm_base_only('scimark', 'scimark_MonteCarlo', globals(),
                 extra_args=['--benchmark=MonteCarlo', '5000000'])
_register_new_bm_base_only('scimark', 'scimark_LU', globals(),
                 extra_args=['--benchmark=LU', '100', '200'])
_register_new_bm_base_only('scimark', 'scimark_FFT', globals(),
                 extra_args=['--benchmark=FFT', '1024', '1000'])

if __name__ == '__main__':
    print sorted(_FindAllBenchmarks(globals()).keys())
