#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import re
import operator

discussion = "970324526351303"
access_token = sys.argv[1]
url = 'https://graph.facebook.com/v2.4/%s?fields=comments&access_token=%s' % (discussion, access_token)

def u(s):
  return unicode(s, "utf-8")

keywords = [
  u("transport"),
  u("jobb"),
  u("billig"),
  [u("miljövänlig"), u("miljö vänlig"), u("miljön")],
  u("snabb"),
  u("frihet"),
  u("hälsa"), u("mår bra"),
  u("roligt"),
  [u("bestämma"), u("styr")],
  u("enkel"),
  u("vackrast"),
  u("överallt"),
  [u("träning"), u("motion"), u("stark")],
  u("natur"),
]

user_stats = {}
counts = {}

while url:
  r = requests.get(url)
  if r.status_code != 200:
    sys.exit(1)
  data = r.json()

  if not "comments" in data:
    break

  comments = data["comments"]
  for comment in comments["data"]:

    user_id = comment["from"]["id"]
    user_stat = user_stats.get(user_id, {})
    user_stats[user_id] = user_stat

    message = comment["message"].lower()
    for x in keywords:
      if not isinstance(x, list):
        x = [x]
      for keyword in x:
        if keyword in message:
          user_stat[x[0]] = 1
          counts[x[0]] = 0

  paging = comments["paging"]
  url = paging["next"]
  print
  print url
  print

for user_stat in user_stats.itervalues():
  for keyword, count in user_stat.iteritems():
    counts[keyword] += count

sorted_stats = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
for (word, count) in sorted_stats:
  if count > 1: print word, count

