import os.path

root = os.path.abspath(os.path.join(__file__, '..', '..'))
util_py = os.path.join(root, 'unladen_swallow', 'performance', 'util.py')
with open(util_py) as fid:
    exec(fid.read())
