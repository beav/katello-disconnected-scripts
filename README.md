katello-disconnected-scripts
============================

how to use
----------

* install `pulp` and `pulp-admin` (see http://pulpproject.org/ug/UGInstallation.html)
* set hostname to match in `/etc/pulp/pulp.conf` and `/etc/pulp/admin/admin.conf`
* initialize the pulp server with `service pulp-server init` and `service pulp-server start`
* run `pulp-admin auth login --username admin` (this step will go away once I get oauth working). You can get the password from `/etc/pulp/pulp.conf`
* run the script: `python katello-disconnected-configure -m manifest.zip -o /path/to/export/location/ -s /path/to/output/scripts/`.<del>Not all of the command-line arguments listed in `--help` currently work.</del>
* once `katello-disconnected-configure` runs, you will have three files in your output script dir: `sync_all.sh`, `export_all.sh`, and `repos.list`. If you run `bash -x sync_all.sh`, it will sync everything from your manifest but will take awhile. You can pare it down a bit before running if you want, but make sure you make the same changes to export.sh. Alternatively, edit down repos.list (or create a new list from this) and use `katello-disconnected-sync -r repos.list --sync`
* once the sync completes, run `bash -x export.sh`. This will not take as much time as the sync. Alternatively, use `katello-disconnected-sync -r repos.list --export-dir /path/to/export/location/`
* NOTE: `katello-disconnected-sync` can take both `--sync` and `--export-dir` options at the same time; however, the sync will most likely not be completed when the export attempts to run. In this case, use `--status` with `--sync` to determine when the repos are done syncing before starting the export

Once a full export is complete, you can <del>copy the export directory over to the katello server in `/var/www/html/content`</del> (acts weird, needs work), or just host it off your laptop if that's easier by running `python -m SimpleHTTPServer` from the export root.

You can then alter the CDN location in the katello web ui to the right place, and perform a manifest import. Once that is complete, you can sync over whichever repos you selected earlier in sync.sh, and the sync should occur.

If you want to toggle back to the CDN later, you can run `point-to-cdn.py`

TODO
----

* replace one-liner with a small script
* <del>allow configuration of CA cert location via command-line</del>
* get oauth working, replace shell calls to pulp-admin
* implement a better way to do repo selection, perhaps with python-okaara
* maybe have some way to tell CFSE which repos you want to sync without having to click through the UI
* export from a CFSE instead of/in addition to the CDN
* make importing work from httpd, odd cert issue
* pulp might be re-downloading after changing hostname, need to look into
* ability to specify --version=6Server --arch=x86_64 --arch=i386 --version=5Server and so on
