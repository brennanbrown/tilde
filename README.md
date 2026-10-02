```
   ░██    ░██ ░██        ░██
   ░██        ░██        ░██
░████████ ░██ ░██  ░████████  ░███████  
   ░██    ░██ ░██ ░██    ░██ ░██    ░██ 
   ░██    ░██ ░██ ░██    ░██ ░█████████ 
   ░██    ░██ ░██ ░██   ░███ ░██        
    ░████ ░██ ░██  ░█████░██  ░███████  

    ░████      ░████      ░████        
   ░██ ░██ ░██░██ ░██ ░██░██ ░██ ░██   
        ░████      ░████      ░████    

```

# tilde

My files and assets from the Tildeverse and other public-access Unix-like
servers, mirrored locally with `rsync`/`tar` over SSH and tracked in git.

Each top-level directory is a mirror of a remote home directory (or the
equivalent web/gopher space). Syncs are **one-way, remote → local**.

## Layout

| Dir | Host | Login | Lives at |
|---|---|---|---|
| `town/` | tilde.town | `brennan` | https://tilde.town/~brennan |
| `pink/` | tilde.pink | `brennan` | gemini://tilde.pink/~brennan |
| `club/` | tilde.club | `brennan` | https://tilde.club/~brennan |
| `sdf/` | sdf.org | `bren` | https://bren.sdf.org |

### `town/`: tilde.town

- `public_html/`: homepage
- `.ttbp/`: [ttbp](https://github.com/modgethanc/ttbp) ("tilde.town
  blogging platform") feels blog: entries, rendered HTML (`www/`), and
  gopher output
- `.botany/`: tilde.town plant game data
- `.prosaic/`: poetry-generation templates (haiku, sonnet, etc.)
- `public_gopher/`, `public_gemini/`: gopherhole + capsule roots
- `guestbook.txt`, weechat/micro/elinks configs, assorted dotfiles

### `pink/`: tilde.pink

- `public_gemini/`: the main Gemini capsule: gemlog, guides (*Beginner's
  Guide to Gemini*, *Blogging on Gemini*, *Publishing Workflow*), poetry,
  book/film/music shelf pages, `.plan`/`.project`/`.finger`
- `public_gopher/`: gopher root
- `.byobu/`, `.irssi/`, `.config/micro/`: shell session + editor configs

### `club/`: tilde.club

- `public_html/`: homepage + bashblog-style blog (`blog/`, with `feed.rss`
  and gophermap)
- `public_gopher/blog`, `public_gemini/`: mirrors of the same posts
- `sieve/`: mail filter rules
- `.byobu/`, weechat/irssi/micro configs

### `sdf/`: SDF Public Access UNIX System

SDF (login `bren`, *not* `brennan`) keeps nearly
nothing in `$HOME`. The content lives at paths symlinked from `~`,
those targets are mirrored into real local directories instead:

- `html/` ← `/www/af/b/bren`: bren.sdf.org site: plain HTML+CSS, geek code,
  public keys page, `guestbook.cgi`
- `gopher/` ← `/ftp/pub/users/bren`: gopherhole

## Syncing

```sh
./sync.sh
```

Re-pulls every mirror:

- **town/pink/club** use `rsync -az --delete --exclude-from=sync.excludes`.
  `--delete` means files removed remotely disappear here too: the dirs are
  mirrors, not archives. Edit `sync.excludes` to skip paths (currently just
  `.cache/` and `.emacs.d/eln-cache/`).
- **sdf** doesn't permit `rsync` for this account class, so it's pulled via
  `ssh ... tar`. The `~/gopher` and `~/html` symlinks are excluded from the
  home tarball so re-syncs don't clobber the real `gopher/`/`html/` dirs.

Requirements: SSH key auth already configured (see `~/.ssh/config`: note
`sdf.org` maps to user `bren` with `id_ed25519_brennanbrown_ca`).

## What's Not Tracked

 `.gitignore` keeps these on disk, but out of git:

- **Credentials**: `.ssh/`, `.gnupg/`, `.keychain/`, `.google_authenticator`,
  `.alpine.passfile`, `.alpine-smime/`, `.twurlrc`, `.bbjrc`, `.bink/`,
  weechat `sec.conf`/`irc.conf`, `.irssi/`, `identity.pem`, `.pinerc`
- **Mail**: `mail/`, `Mail/`, `.mail/`, `mbox`
- **Logs & history**: shell histories, weechat logs, `.local/state/`
- **Caches**: `.cache/` (this alone is ~100M of dnf junk on club),
  `eln-cache/`

The files sync to disk and are never committed.

## Wiki

`wiki/` is a markdown wiki documenting what lives in each mirror and how
the accounts overlap (`architecture.md` is the cross-host map). Build it
to HTML with `./build.sh`, which needs `pandoc`. Output lands in `docs/`,
which is tracked and served by GitHub Pages at
[tilde.land](https://tilde.land). Links between pages are written as `.md`
so they work on GitHub; the build rewrites them to `.html`.

## License

Content is licensed under the GNU Affero General Public License
v3.0 or later (AGPL-3.0-or-later). See `LICENSE`. Dotfiles and
configs remain under whatever licenses their respective authors chose.
