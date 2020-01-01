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

"""URL mappings for the codereview package."""

# NOTE: Must import *, since Django looks for things here, e.g. handler500.
from django.conf.urls.defaults import *

from codereview import feeds, views

urlpatterns = patterns(
    'codereview.views',
    (r'^$', views.index),
    (r'^all$', views.all),
    (r'^mine$', views.mine),
    (r'^starred$', views.starred),
    (r'^new$', views.new),
    (r'^upload$', views.upload),
    (r'^(\d+)$', views.show),
    (r'^(\d+)/show$', views.show),
    (r'^(\d+)/add$', views.add),
    (r'^(\d+)/edit$', views.edit),
    (r'^(\d+)/delete$', views.delete),
    (r'^(\d+)/close$', views.close),
    (r'^(\d+)/mail$', views.mailissue),
    (r'^(\d+)/publish$', views.publish),
    (r'^download/issue(\d+)_(\d+)\.diff', views.download),
    (r'^download/issue(\d+)_(\d+)_(\d+)\.diff', views.download_patch),
    (r'^(\d+)/patch/(\d+)/(\d+)$', views.patch),
    (r'^(\d+)/image/(\d+)/(\d+)/(\d+)$', views.image),
    (r'^(\d+)/diff/(\d+)/(\d+)$', views.diff),
    (r'^(\d+)/diff2/(\d+):(\d+)/(\d+)$', views.diff2),
    (r'^(\d+)/diff_skipped_lines/(\d+)/(\d+)/(\d+)/(\d+)/([tb])/(\d+)$',
     views.diff_skipped_lines),
    (r'^(\d+)/diff2_skipped_lines/(\d+):(\d+)/(\d+)/(\d+)/(\d+)/([tb])/(\d+)$',
     views.diff2_skipped_lines),
    (r'^(\d+)/upload_content/(\d+)/(\d+)$', views.upload_content),
    (r'^(\d+)/upload_patch/(\d+)$', views.upload_patch),
    (r'^(\d+)/description$', views.description),
    (r'^(\d+)/star$', views.star),
    (r'^(\d+)/unstar$', views.unstar),
    (r'^(\d+)/draft_message$', views.draft_message),
    (r'^user/(.+)$', views.show_user),
    (r'^inline_draft$', views.inline_draft),
    (r'^repos$', views.repos),
    (r'^repo_new$', views.repo_new),
    (r'^repo_init$', views.repo_init),
    (r'^branch_new/(\d+)$', views.branch_new),
    (r'^branch_edit/(\d+)$', views.branch_edit),
    (r'^branch_delete/(\d+)$', views.branch_delete),
    (r'^settings$', views.settings),
    (r'^user_popup/(.+)$', views.user_popup),
    (r'^(\d+)/patchset/(\d+)$', views.patchset),
    (r'^account$', views.account),
    (r'^use_uploadpy$', views.use_uploadpy),
    (r'^update_accounts$', views.update_accounts),
    )

feed_dict = {
  'reviews': feeds.ReviewsFeed,
  'closed': feeds.ClosedFeed,
  'mine' : feeds.MineFeed,
  'all': feeds.AllFeed,
  'issue' : feeds.OneIssueFeed,
}

from django.contrib.syndication.feeds import Feed

urlpatterns += patterns(
    'codereview.feeds',
    (r'^rss/(?P<url>.*)$', Feed,
     {'feed_dict': feed_dict}),
    )
