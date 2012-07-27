katello-disconnected-scripts
============================

what they are
-------------
* katello-disconnected-configure - reads a manifest, creates pulp repos, generates scripts for syncing
* katello-disconnected-sync - syncs and exports repos
* point-to-cdn.py - change pulp repos to change feed to a url

how to use
----------

* enable the katello repo (see https://fedorahosted.org/katello/wiki/Install for the repo info)
* install `pulp` and `pulp-admin` (see http://pulpproject.org/ug/UGInstallation.html)
* set proper hostname in `/etc/pulp/pulp.conf` and `/etc/pulp/admin/admin.conf`
* initialize the pulp server with `service pulp-server init` and `service pulp-server start`
* run `pulp-admin auth login --username admin` (this step will go away once I get oauth working). You can get the password from `/etc/pulp/pulp.conf`
* run the script: `python katello-disconnected-configure -m manifest.zip -o /path/to/export/location/ -s /path/to/output/scripts/`.<del>Not all of the command-line arguments listed in `--help` currently work.</del> To restrict what architectures, release versions and channels are used, see --help.
* once `katello-disconnected-configure` runs, you will have three files in your output script dir: `sync_all.sh`, `export_all.sh`, and `repos.list`. If you run `bash -x sync_all.sh`, it will sync everything from your manifest but will take awhile. You can pare it down a bit before running if you want, but make sure you make the same changes to export.sh. Alternatively, edit down repos.list (or create a new list from this) and use `katello-disconnected-sync -r repos.list --sync`
* once the sync completes, run `bash -x export.sh`. This will not take as much time as the sync. Alternatively, use `katello-disconnected-sync -r repos.list --export-dir /path/to/export/location/`
NOTE: `katello-disconnected-sync` can take both `--sync` and `--export-dir` options at the same time; however, this will invoke the --watch option, which will loop continuously after the sync has started. You must cancel the status loop once all repos are synced to begin the export.
* once a full export is complete, copy the exported directory to the destination katello server, if it will be on a different system
* serve out the exported content with:`python -m SimpleHTTPServer` from the export root
* alter the CDN location in katello web ui or shell to the exported server and port
* perform a manifest import (ensure the exported content is accessible before doing this)
* once the import is complete, enable and sync over whichever repos you selected earlier
* if desired, toggle back to the CDN with `point-to-cdn.py`

examples
--------
`python katello-disconnected-configure -m manifest.zip -s scripts -o /var/katello-content/ -r 6.2,6Server -a x86_64 -c cf-tools,supplementary`

This will only process repos matching the specified criteria, though many more repositories are available for this menifest.

`cat scripts/repos.list`  

    6.2_server_x86_64	/content/dist/rhel/server/6/6.2/x86_64/os
    6Server_server_x86_64	/content/dist/rhel/server/6/6Server/x86_64/os
    6.2_server_x86_64_supplementary	/content/dist/rhel/server/6/6.2/x86_64/supplementary/os
    6Server_server_x86_64_supplementary	/content/dist/rhel/server/6/6Server/x86_64/supplementary/os
    6.2_server_x86_64_cf-tools_1.0	/content/dist/rhel/server/6/6.2/x86_64/cf-tools/1.0/os
    6Server_server_x86_64_cf-tools_1.0	/content/dist/rhel/server/6/6Server/x86_64/cf-tools/1.0/os

`python katello-disconnected-sync --sync -r scripts/repos.list --export-dir /var/katello-content/`  

    Sync for repository 6Server_server_x86_64 started
    Use "repo status" to check on the progress
    Sync for repository 6.2_server_x86_64 started
    Use "repo status" to check on the progress
    Sync for repository 6Server_server_x86_64_supplementary started
    Use "repo status" to check on the progress
    Sync for repository 6.2_server_x86_64_supplementary started
    Use "repo status" to check on the progress
    Sync for repository 6Server_server_x86_64_cf-tools_1.0 started
    Use "repo status" to check on the progress
    Sync for repository 6.2_server_x86_64_cf-tools_1.0 started
    Use "repo status" to check on the progress
    
    
    +------------------------------------------+
          Status for 6Server_server_x86_64
    +------------------------------------------+
    Repository: 6Server_server_x86_64
    Number of Packages: 8344
    Last Sync: 2012-07-26 02:28:21-05:00
    Currently syncing: Downloading Items or Verifying (56 of 8351 items downloaded. 11781386640.0 bytes remaining)
    
    +------------------------------------------+
            Status for 6.2_server_x86_64
    +------------------------------------------+
    Repository: 6.2_server_x86_64
    Number of Packages: 0
    Last Sync: never
    Currently syncing: Downloading Items or Verifying (407 of 7287 items downloaded. 10158267388.0 bytes remaining)
    
    +------------------------------------------+
     Status for 6Server_server_x86_64_supplementary
    +------------------------------------------+
    Repository: 6Server_server_x86_64_supplementary
    Number of Packages: 0
    Last Sync: never
    Currently syncing: progress unknown
    
    +------------------------------------------+
     Status for 6.2_server_x86_64_supplementary
    +------------------------------------------+
    Repository: 6.2_server_x86_64_supplementary
    Number of Packages: 0
    Last Sync: never
    Currently syncing: progress unknown
    
    +------------------------------------------+
     Status for 6Server_server_x86_64_cf-tools_1.0
    +------------------------------------------+
    Repository: 6Server_server_x86_64_cf-tools_1.0
    Number of Packages: 26
    Last Sync: 2012-07-26 02:01:54-05:00
    Currently syncing: progress unknown
    
    +------------------------------------------+
      Status for 6.2_server_x86_64_cf-tools_1.0
    +------------------------------------------+
    Repository: 6.2_server_x86_64_cf-tools_1.0
    Number of Packages: 0
    Last Sync: never
    Currently syncing: progress unknown
    
    =========================================================================
    | Waiting 10 seconds (press CTRL+C to cancel when all repos are synced) |
    =========================================================================

You can also run operation independently:  
`python katello-disconnected-sync --sync -r scripts/repos.list`  
`python katello-disconnected-sync --export-dir /var/katello-content/ -r scripts/repos.list --status`  
`python katello-disconnected-sync --sync -r scripts/repos.list --watch`  


todo
----

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
