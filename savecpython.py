#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import urllib, urllib2
from datetime import datetime
import optparse

#SPEEDURL = 'http://127.0.0.1:8000/'
SPEEDURL = 'https://speed.pypy.org/'

def save(project, revision, results, options, executable, host, testing=False,
         base=False):
    testparams = []
    #Parse data
    data = {}
    current_date = datetime.today()
        
    for b in results:
        bench_name = b[0]
        res_type = b[1]
        results = b[2]
        value = 0
        if res_type == "SimpleComparisonResult"
            if base:
                value = results['base_time']
            else:
                value = results['changed_time']
            if value is None:
                continue
            value = value[0]
        elif res_type == 'RawResult':
            if base:
                value = results['base_times']
            else:
                value = results['changed_times']
            if value is None or len(value) == 0:
                continue
            value = value[0]
        elif res_type == "ComparisonResult":
            if base:
                value = results['avg_base']
            else:
                value = results['avg_changed']
        else:
            print("ERROR: result type unknown " + b[1])
            return 1
        data = [{
            'commitid': revision,
            'project': project,
            'executable': executable,
            'benchmark': bench_name,
            'environment': host,
            'result_value': value,
            'branch': 'default',
        }]
        if res_type == "ComparisonResult":
            if base:
                data[0]['std_dev'] = results['std_base']
            else:
                data[0]['std_dev'] = results['std_changed']
        if testing: testparams.append(data)
        else: send(data)
    if testing: return testparams
    else: return 0
    
def send(data):
    #save results
    params = urllib.urlencode({'json': json.dumps(data)})
    f = None
    response = "None"
    info = str(datetime.today()) + ": Saving result for " + data[0]['executable'] + " revision "
    info += str(data[0]['commitid']) + ", benchmark " + data[0]['benchmark']
    print(info)
    try:
        f = urllib2.urlopen(SPEEDURL + 'result/add/json/', params)
        response = f.read()
        f.close()
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            response = '\n  We failed to reach a server\n'
            response += '  Reason: ' + str(e.reason)
        elif hasattr(e, 'code'):
            response = '\n  The server couldn\'t fulfill the request\n'
            response += '  Error code: ' + str(e)
        print("Server (%s) response: %s\n" % (SPEEDURL, response))
        if hasattr(e, 'fp'):
            print e.fp.read(), "\n"
        return 1
    return 0

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-b', '--base', action='store_true',
                      help='take base values instead of modified')
    parser.add_option('--revision', help='revision number (100 for cpythono 2.6.2, 101 for 2.7.2, edit admin interface to add more)', type=int,
                      default=100)
    options, args = parser.parse_args(sys.argv)
    if len(args) != 2:
        print parser.usage
        sys.exit(1)
    results = json.load(open(args[1]))['results']
    save('cpython', options.revision, results, None, 'cpython', 'benchmarker',
         testing=False,
         base=options.base)
