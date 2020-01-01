# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Minimal Django settings."""

import os

APPEND_SLASH = False
DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
INSTALLED_APPS = (
    'codereview',
    'django.contrib.sites',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'codereview.middleware.AddUserToRequestMiddleware',
)
ROOT_URLCONF = 'urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS' : [
                os.path.join(os.path.dirname(__file__), 'templates'),
               ],
        'APP_DIRS': True
    },
]
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
)
FILE_UPLOAD_MAX_MEMORY_SIZE = 1048576  # 1 MB

# Django requires that settings.SECRET_KEY be defined.  According to the docs,
# It is used by django.core.signing, which we do not use in our app.
# We could just set it to 'foo' and ignore it, but that would not be secure.
# So, we make sure that it is never used for anything.
class MakeSureNothingReadsThisString(object):
  """If Django reads this string for any reason, fail loudly."""
  def __str__(self):
    logging.error('SECRET_KEY was never meant to be used')
    raise NotImplementedError()

SECRET_KEY = MakeSureNothingReadsThisString()
