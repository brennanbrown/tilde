#!/bin/sh
# Mirror tildeverse home directories into this repo.
# rsync mirrors use --delete: files removed remotely are removed here too.
set -eu
cd "$(dirname "$0")"

rsync -az --timeout=60 --delete --exclude-from=sync.excludes brennan@tilde.town:~/ town/
rsync -az --timeout=60 --delete --exclude-from=sync.excludes brennan@tilde.pink:~/ pink/
rsync -az --timeout=60 --delete --exclude-from=sync.excludes brennan@tilde.club:~/ club/
# cosmic's ~/ships entries are symlinks into /var/gopher (the QEC relay
# tree); the symlink is excluded and its target is pulled as a real dir.
rsync -az --timeout=60 --delete --exclude-from=sync.excludes --exclude=/ships/ brennan@cosmic.voyage:~/ cosmic/
rsync -azL --timeout=60 --delete brennan@cosmic.voyage:~/ships/Genawaaboonagak/ cosmic/ships/Genawaaboonagak/
rsync -az --timeout=60 --delete --exclude-from=sync.excludes brennan@envs.net:~/ envs/
rsync -az --timeout=60 --delete --exclude-from=sync.excludes brennan@tilde.green:~/ green/

# SDF does not permit rsync for this account class; pull via tar over SSH.
# ~/gopher and ~/html are symlinks outside $HOME — their real contents are
# pulled into sdf/gopher/ and sdf/html/, and the symlinks are excluded so
# re-syncing does not clobber those directories.
ssh sdf.org 'tar czf - -C ~ --exclude=./gopher --exclude=./html .' | tar xzf - -C sdf/
ssh sdf.org 'tar czf - -C /ftp/pub/users/bren .' | tar xzf - -C sdf/gopher/
ssh sdf.org 'tar czf - -C /www/af/b/bren .' | tar xzf - -C sdf/html/
