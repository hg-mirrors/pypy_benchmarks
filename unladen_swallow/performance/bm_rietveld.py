#!/usr/bin/env python

"""Wrapper script for testing the performance of the Rietveld templates.

This is intended to support Unladen Swallow's perf.py

This will have Django render templates from Rietveld with canned data as many
times as you specify (via the -n flag). The raw times to generate the template
will be dumped to stdout. This is more convenient for Unladen Swallow's uses:
it allows us to keep all our stats in perf.py.

The data used for this benchmark was generated by running a simple development
copy of Rietveld on the App Engine SDK, and invoking upload.py on the Rietveld
source tree several times with trivial changes.  The main template rendering
routine was modified to pickle the relevant parts of the context dictionary and
dump it to the log.  Certain parameters such as the 'request' and 'form' keys
had to be deleted, since the would not pickle.  However, they are not used in
the template, so this should have no effect.

The following code block was inserted into the respond function in views.py
before the call to render_to_response:

    ...
    try:
        # START INSERTED CODE
        import pickle
        interesting_params = params.copy()
        interesting_params.pop("request", None)
        interesting_params.pop("form", None)
        logging.info(pickle.dumps((template, interesting_params)))
        # END INSERTED CODE
        return render_to_response(template, params)
    ...
"""

from __future__ import division, print_function

__author__ = "rnk@google.com (Reid Kleckner)"

# Python imports
import optparse
import os
import time
import sys
import logging

if sys.version_info[0] < 3:
    import cPickle as pickle
else:
    import pickle

# Local imports
import util

# Django imports
from django.template import Context, loader
import django

# Appengine imports
from google.appengine.tools import dev_appserver


def rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def setup():
    # Appengine needs this setup.
    os.environ["SERVER_SOFTWARE"] = "Dev"
    os.environ["AUTH_DOMAIN"] = "gmail.com"
    os.environ["USER_EMAIL"] = "test@example.com"
    datastore_path = rel_path("rietveld_datastore")
    history_path = rel_path("rietveld_datastore_history")
    options = {"datastore_path": datastore_path,
               "history_path": history_path,
               "clear_datastore": False,
               "login_url": "/_ah/login",
               }
    dev_appserver.SetupStubs("codereview", **options)


def get_benchmark_data():
    # Load data.
    data_file = rel_path("rietveld_data.pickle")
    templ_name, canned_data = pickle.load(open(data_file))
    context = Context(canned_data)
    # rebuild the data as a dictionary, let django build the context
    context = {
        'issue': {},
        'email': 'me@you.com',
        'is_dev': True,
        'user': 'me@you.com',
        'codereview': {'views': {'settings':3}},
    }

    # Load template.
    tmpl = loader.get_template(templ_name)
    return tmpl, context


def test_rietveld(count, tmpl, context):
    # Warm up Django.
    tmpl.render(context)
    tmpl.render(context)

    times = []
    for _ in xrange(count):
        t0 = time.time()
        # 30 calls to render, so that we don't measure loop overhead.
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        tmpl.render(context)
        t1 = time.time()
        times.append(t1 - t0)
    return times


if __name__ == "__main__":
    logger = logging.getLogger('django.template')
    setup()
    django.setup()
    logger.setLevel(logging.DEBUG)
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of Django templates using "
                     "Rietveld's front page template."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    tmpl, context = get_benchmark_data()
    util.run_benchmark(options, options.num_runs, test_rietveld, tmpl, context)
