#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################
# This script saves result data                       #
# It expects the format of unladen swallow's perf.py  #
#######################################################

"""
Upload a json file generated by runner.py.

Revision, name and host are required.

Example usage:

  $ ./saveresults.py result.json -r '45757:fabe4fc0dc08' -n pypy-c-jit \
    -H tannit

  OR

  $ ./saveresults.py result.json -r '45757:fabe4fc0dc08' -n pypy-c-jit-64 \
    -H tannit
"""
from __future__ import division, print_function

from datetime import datetime
import optparse
import sys
import time
import urllib
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
import json


def save(project, revision, results, executeable, host, url, testing=False,
         changed=True, branch='default'):
    testparams = []
    #Parse data
    data = {}
    error = 0

    for b in results:
        bench_name = b[0]
        res_type = b[1]
        results = b[2]
        value = 0
        if res_type == "SimpleComparisonResult":
            if changed:
                value = results['changed_time']
            else:
                value = results['base_time']
        elif res_type == "ComparisonResult":
            if changed:
                value = results['avg_changed']
            else:
                value = results['avg_base']
        elif res_type == "RawResult":
            if changed:
                value = results["changed_times"]
            else:
                value = results["base_times"]
            if value:
                assert len(value) == 1
                value = value[0]
        else:
            print("ERROR: result type unknown " + b[1])
            return 1
        data = [{
            'commitid': revision,
            'project': project,
            'executable': executeable,
            'benchmark': bench_name,
            'environment': host,
            'result_value': value,
            'branch': branch,
        }]
        if value is None:
            print("Ignoring skipped result", data)
            continue
        if res_type == "ComparisonResult":
            if changed:
                data[0]['std_dev'] = results['std_changed']
            else:
                data[0]['std_dev'] = results['std_base']
        if testing:
            testparams.append(data)
        else:
            error |= send(data, url)

    if error:
        raise IOError("Saving failed.  See messages above.")
    if testing:
        return testparams
    else:
        return 0


def send(data, url):
    #save results
    params = urllib.urlencode({'json': json.dumps(data)})
    f = None
    response = "None"
    info = ("%s: Saving result for %s revision %s, benchmark %s" %
            (str(datetime.today()), data[0]['executable'],
             str(data[0]['commitid']), data[0]['benchmark']))
    print(info)
    try:
        retries = [1, 2, 3, 6]
        while True:
            try:
                print('result/add')
                f = urllib2.urlopen(url + 'result/add/json/', params)
                print('urlopen')
                response = f.read()
                print('response')
                f.close()
                break
            except urllib2.URLError:
                if not retries:
                    raise
                d = retries.pop(0)
                print("retrying in %d seconds..." % d)
                time.sleep(d)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            response = '\n  We failed to reach a server\n'
            response += '  Reason: ' + str(e.reason)
        elif hasattr(e, 'code'):
            response = '\n  The server couldn\'t fulfill the request'
        if hasattr(e, 'readlines'):
            response = "".join([response] + e.readlines())
        print(response)
        with open('error.html', 'w') as error_file:
            error_file.write(response)
        print("Server (%s) response written to error.html" % (url,))
        print('  Error code: %s\n' % (e,))
        return 1
    print("saved correctly!", end='\n\n')
    return 0


def main(jsonfile, options):
    import simplejson
    with open(jsonfile) as f:
        data = simplejson.load(f)
    results = data['results']
    print('uploading results...', end='')
    save(options.project, options.revision, results, options.executable,
                options.host, options.url, changed=options.changed)
    print('done')


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog result.json [options]")
    parser.add_option('-r', '--revision', dest='revision',
                      default=None, type=str, help='VCS revision (required)')
    parser.add_option('-n', '--name', dest='executable',
                      default=None, type=str,
                      help=('Name of the executable for codespeed.'
                            'Deprecated. Use --e/--executable instead'))
    parser.add_option('-e', '--executable', dest='executable',
                      default=None, type=str,
                      help='Name of the Executable for codespeed (required).')
    parser.add_option('-H', '--host', dest='host', default=None, type=str)
    parser.add_option('-b', '--baseline', dest='changed', default=True,
                      action='store_false',
                      help='upload the results as baseline instead of changed')
    parser.add_option('-P', '--project', dest='project', default='PyPy')
    parser.add_option('-u', '--url', dest='url',
                      default="https://speed.pypy.org/",
                      help=('Url of the codespeed instance '
                            '(default: https://speed.pypy.org/)'))
    parser.format_description = lambda fmt: __doc__
    parser.description = __doc__
    options, args = parser.parse_args()
    if (options.revision is None or options.executable is None or
        options.host is None or len(args) != 1):
        parser.print_help()
        sys.exit(2)
    main(args[0], options)
