TODO
============================
* replace one-liner with a small script
* <del>allow configuration of CA cert location via command-line</del>
* get oauth working, replace shell calls to pulp-admin
* implement a better way to do repo selection, perhaps with python-okaara
* maybe have some way to tell CFSE which repos you want to sync without having to click through the UI
* export from a CFSE instead of/in addition to the CDN
* make importing work from httpd, odd cert issue
* pulp might be re-downloading after changing hostname, need to look into
* <del>ability to specify --version=6Server --arch=x86_64 --arch=i386 --version=5Server and so on</del>
* suppress messages and prevent dir creation for repos not matched with --releases, --arches, --channels
* <del>add KeyboardInterrupt detection in both scripts</del>
* clean up --dry-run (currently only supresses repo create, need to add it throughout)
* change point-to-cdn.py to take a url as an argument (default cdn)
* investigate issues with a couple of new manifests that it give SSL errors (may be related to size issue)
