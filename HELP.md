`python katello-disconnected-configure --help`  
    Usage: katello-disconnected-configure [options]
    This will configure a disconnected environment for katello. Use --help for a list of options.
    
    Options:
      -h, --help            show this help message and exit
      -m FILE, --manifest=FILE
                            read manifest from FILE
      -v, --verbose         verbose mode
      -e, --everything      create repos for everything (beta, iso, srpms, debug
                            rpms)
      -s DIRECTORY, --script-output-dir=DIRECTORY
                            write generation scripts to DIRECTORY
      -o DIRECTORY, --output-dir=DIRECTORY
                            write repo tree to DIRECTORY
      -u, --uncommon        sync repos that are not commonly used (betas, srpms,
                            isos, debug rpms)
      -C FILE, --ca-cert=FILE
                            specify CA cert to use
      -f, --force           overwrite any existing directories and scripts
                            (output,script output)
      -a ARCHES, --arches=ARCHES
                            only create repos for a specific architecture (e.g.
                            x86_64,i386)
      -r RELEASES, --releases=RELEASES
                            Only create repos for specific versions (e.g.
                            6Server,5.4)
      -c CHANNELS, --channels=CHANNELS
                            Only create repos for specific channels (e.g. cf-
                            tools_1.0,subscription-asset-manager_1)
      -d, --dry-run         Do not create repos, only write scripts to show what
                            would be created
    
`python katello-disconnected-sync --help`  
    Usage: katello-disconnected-sync [options]
    This will sync and/or export repos to a specific directory. Use --help for a full list of options.
    
    Options:
      -h, --help            show this help message and exit
      -v, --verbose         verbose mode
      -s, --sync            Synchronize channels in file specified with --export-
                            dir
      -l, --status          obtain status
      -r REPO_LIST, --repo-list=REPO_LIST
                            File containing list of repositories to act on
      -e DIRECTORY, --export-dir=DIRECTORY
                            Directory to use as the disconnected synchronization
                            store
      -w, --watch           Loop through every 5 seconds watching status until
                            CTRL+C is pressed.
    
