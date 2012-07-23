katello-disconnected-scripts
============================

how to use
----------

* install pulp and pulp-admin (see http://pulpproject.org/ug/UGInstallation.html)
* Initialize the pulp server with `service pulp-server init` and `service pulp-server start`
* run `pulp-admin auth login --username admin` (this step will go away once I get oauth working). You can get the password from `/etc/pulp/pulp.conf`
* run the script: `python katello-disconnected-configure -m manifest.zip -o /path/to/export/location -s sync_output_script_dir`.<del>Not all of the command-line arguments listed in `--help` currently work.</del>

* once the script runs,  you will have two files in your output script dir: sync.list and export.list. If you run `bash -x sync.list`, it will sync everything but will take awhile. You can pare it down a bit before running if you want, but make sure you make the same changes to export.list
* once the sync completes, run `bash -x export.list`. This will not take as much time as the sync.

At this point, you can copy the export directory over to the katello server in `/var/www/html/content`, or just host it off your laptop if that's easier by running `python -m SimpleHTTPServer` from the export root.

You can then alter the CDN location in the katello web ui to the right place, and perform a manifest import. Once that is complete, you can sync over whichever repos you selected earlier in sync.list, and the sync should occur.

If you want to toggle back to the CDN later, you can run the following gnarly one-liner:
```bash
pulp-admin repo list | awk 'BEGIN{RS="Id";FS="\n" } {split($1,a," ");split($4,b," ");printf"%s\t%s\n",a[1],b[3] }' \
 | sed 's/http:\/\/local.url.here:port/https:\/\/cdn.redhat.com/' | tail -n +2 \
 | awk '{printf"pulp-admin repo update --id %s  --feed %s\n",$1,$2}' > cdn.sh; bash -x cdn.sh
```

TODO
----

* replace one-liner with a small script
* <del>allow configuration of CA cert location via command-line</del>
* get oauth working, replace shell calls to pulp-admin
* implement a better way to do repo selection, perhaps with python-okaara
* maybe have some way to tell CFSE which repos you want to sync without having to click through the UI
* export from a CFSE instead of/in addition to the CDN

 
