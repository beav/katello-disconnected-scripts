#!/usr/share/python

"""
This script converts all pulp URLs from one hostname to another. Important
notes:

  * There is no way to convert anything besides the hostname and scheme
    (http/https). This is a limitation of pulp v1.

  * All feed URLs will get updated, even if they are being updated to the same
    URL again. This is a bug.

  * This should be using pulp's rest API, instead of executing pulp-admin
    directly

Example on how to use script (once you run pulp-admin login auth):
  python ./point-to-cdn.py -u http://192.168.122.1:8080

Note that other URLs without the port will work as well.

"""
import commands
import os
from optparse import OptionParser

CDN_URL = 'https://cdn.redhat.com'

parser = OptionParser()
parser.add_option("-u", "--url", dest="old_url",
    help="url to alter into CDN url. Example: http://10.11.xx.xx", metavar="URL")

(options, args) = parser.parse_args()

# this should really be using oauth + pulp's rest API
repos = commands.getoutput('pulp-admin repo list')

REPO_UPDATE_CMD = 'pulp-admin repo update --id %s --feed %s'

repo_name = ""
commands = []
for l in repos.splitlines():
  fields = l.split('\t')
  if fields[0].strip() == 'Id':
     repo_name = fields[1].strip()
  if fields[0].strip() == 'Feed URL':
     old_url = fields[1].strip()
     new_url = old_url.replace(options.old_url, CDN_URL)
     commands.append(REPO_UPDATE_CMD % (repo_name, new_url))

for cmd in commands:
  # there's nothing stopping you from just executing via the script, but it's
  # easier to test by piping to a sh file and running that
  print "%s" % cmd
  #os.system(cmd)


