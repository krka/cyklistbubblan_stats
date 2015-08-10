#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import re
import operator

discussion = "970324526351303"
access_token = sys.argv[1]
url = 'https://graph.facebook.com/v2.4/%s?fields=comments&access_token=%s' % (discussion, access_token)

def u(l):
  if isinstance(l, str): l = [l]
  return [unicode(s, "utf-8") for s in l]

def format(l):
  return [u(x) for x in l]

keywords = format([
  "transport",
  "jobb",
  "billig",
  ["miljövänlig", "miljö vänlig", "miljön"],
  "snabb",
  "frihet",
  ["hälsa", "mår bra"],
  "roligt",
  ["bestämma", "styr"],
  "enkel",
  "vackrast",
  "överallt",
  ["träning", "motion", "stark"],
  "natur",
])

user_stats = {}
counts = {}

num_comments = 0
while url is not '':
  r = requests.get(url)
  if r.status_code != 200:
    print r.text
    sys.exit(1)
  data = r.json()

  if "comments" in data:
    data = data["comments"]

  if not "data" in data: 
    print r.text
    sys.exit(1)

  for comment in data["data"]:
    num_comments += 1
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

  paging = data["paging"]
  if not "next" in paging:
    break

  url = paging["next"]

print url

print "Total number of comments", num_comments

for user_stat in user_stats.itervalues():
  for keyword, count in user_stat.iteritems():
    counts[keyword] += count

sorted_stats = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
for (word, count) in sorted_stats:
  if count > 1: print word, count

