```
   ░██    ░██ ░██        ░██
   ░██        ░██        ░██
░████████ ░██ ░██  ░████████  ░███████  
   ░██    ░██ ░██ ░██    ░██ ░██    ░██ 
   ░██    ░██ ░██ ░██    ░██ ░█████████ 
   ░██    ░██ ░██ ░██   ░███ ░██        
    ░████ ░██ ░██  ░█████░██  ░███████  

   ░████       ░████        ░████        
  ░██ ░██ ░██ ░██ ░██  ░██ ░██ ░██ ░██   
       ░████       ░████       ░████     

```

# tilde

My files from the Tildeverse and other public-access Unix-like
servers, mirrored locally over SSH and tracked in git.

Each top-level directory is a mirror of one of my remote home
directories (or the equivalent web/gopher space). Syncs are
**one-way, remote → local**.

## Layout

| Dir | Host | Login | Lives at |
|---|---|---|---|
| [`town/`](town/) | tilde.town | `brennan` | https://tilde.town/~brennan |
| [`pink/`](pink/) | tilde.pink | `brennan` | gemini://tilde.pink/~brennan |
| [`club/`](club/) | tilde.club | `brennan` | https://tilde.club/~brennan |
| [`green/`](green/) | tilde.green | `brennan` | https://tilde.green/~brennan |
| [`sdf/`](sdf/) | sdf.org | `bren` | http://bren.sdf.org |
| [`cosmic/`](cosmic/) | cosmic.voyage | `brennan` | https://cosmic.voyage/Genawaaboonagak |
| [`envs/`](envs/) | envs.net | `brennan` | https://envs.net/~brennan |

### [`town/`](town/): tilde.town

The account I use most.

- [`public_html/`](town/public_html/): homepage
- [`.ttbp/`](town/.ttbp/): [ttbp](https://github.com/modgethanc/ttbp) ("tilde.town
  blogging platform") feels blog: entries, rendered HTML ([`www/`](town/.ttbp/www/)), and
  gopher output
- [`.botany/`](town/.botany/): tilde.town plant game data
- [`.prosaic/`](town/.prosaic/): poetry-generation templates (haiku, sonnet, etc.)
- [`public_gopher/`](town/public_gopher/), [`public_gemini/`](town/public_gemini/): gopherhole + capsule roots
- [`guestbook.txt`](town/guestbook.txt), [weechat](town/.config/weechat/)/[micro](town/.config/micro/)/[elinks](town/.config/elinks/) configs, assorted dotfiles

### [`pink/`](pink/): tilde.pink

- [`public_gemini/`](pink/public_gemini/): the main Gemini capsule: gemlog, guides (*Beginner's
  Guide to Gemini*, *Blogging on Gemini*, *Publishing Workflow*), poetry,
  book/film/music shelf pages, [`.plan`](pink/public_gemini/.plan)/[`.project`](pink/public_gemini/.project)/[`.finger`](pink/public_gemini/.finger)
- [`public_gopher/`](pink/public_gopher/): gopher root
- [`.byobu/`](pink/.byobu/), `.irssi/`, [`.config/micro/`](pink/.config/micro/): shell session + editor configs

### [`club/`](club/): tilde.club

- [`public_html/`](club/public_html/): homepage + bashblog-style blog ([`blog/`](club/public_html/blog/), with [`feed.rss`](club/public_html/blog/feed.rss)
  and [`gophermap`](club/public_html/blog/gophermap))
- [`public_gopher/blog`](club/public_gopher/blog), [`public_gemini/`](club/public_gemini/): mirrors of the same posts
- [`sieve/`](club/sieve/): mail filter rules
- [`.byobu/`](club/.byobu/), [weechat](club/.config/weechat/)/irssi/[micro](club/.config/micro/) configs

### [`sdf/`](sdf/): SDF Public Access UNIX System

SDF (login `bren`, *not* `brennan`) keeps nearly
nothing in `$HOME`. The content lives at paths symlinked from `~`,
those targets are mirrored into real local directories instead:

- [`html/`](sdf/html/) ← `/www/af/b/bren`: bren.sdf.org site: plain HTML+CSS, geek code,
  public keys page, [`guestbook.cgi`](sdf/html/guestbook.cgi)
- [`gopher/`](sdf/gopher/) ← `/ftp/pub/users/bren`: gopherhole

### [`cosmic/`](cosmic/): cosmic.voyage

Newest account (October 2026), on the tilde built around a
collaborative science-fiction story. My ship,
[`Genawaaboonagak`](wiki/genawaaboonagak.md), is at
`~/ships/Genawaaboonagak` on the server, a symlink into `/var/gopher/`
(the relay's publish tree); `sync.sh` pulls its target into
[`cosmic/ships/`](cosmic/ships/) like SDF's symlinked dirs. See
[`wiki/cosmic.md`](wiki/cosmic.md).

### [`envs/`](envs/): envs.net

Configured for mail and chat (mutt, weechat, byobu)
but the `public_*` dirs were never filled in. See
[`wiki/envs.md`](wiki/envs.md).

### [`green/`](green/): tilde.green

Newest account (October 2026). Web pages generated from
[`template/`](template/). See [`wiki/green.md`](wiki/green.md).

### [`template/`](template/): shared pubnix pages

Single source of truth for the unstyled sites (**green**, **cosmic**,
**envs**, town/club/sdf keep their own pages, pink is gemini-only):

- [`tilde.css`](template/tilde.css): shared stylesheet, copied into each
  `public_html/`; per-host tint via `<body class="envs|green|cosmic">`
- [`pages/`](template/pages/): shared body fragments
- [`art/`](template/art/): per-host ASCII banner for the index page
- [`skel.html`](template/skel.html): page skeleton (`{{TOKEN}}` placeholders)
- [`generate.py`](template/generate.py): host registry (the `HOSTS` table
  drives the "Tildeverse Homes" table) + generator. Run:

```sh
python3 template/generate.py
```

to (re)write each host's `public_html/{index,writing,keys,support}.html`
and copy `tilde.css`. Edit template files, re-run, re-upload.

## Syncing

```sh
./sync.sh
```

Pulls everything again:

- **town/pink/club/envs/green** use `rsync -az --delete --exclude-from=`[`sync.excludes`](sync.excludes);
  **cosmic** does the same for `~`, plus a follow-the-symlink pull for
  its ship dir.
  `--delete` means files removed remotely disappear here too: the dirs are
  mirrors, not archives. Edit [`sync.excludes`](sync.excludes) to skip paths (currently just
  `.cache/` and `.emacs.d/eln-cache/`).
- **sdf** doesn't permit `rsync` for this account class, so it's pulled via
  `ssh ... tar`. The `~/gopher` and `~/html` symlinks are excluded from the
  home tarball so re-syncs don't overwrite the [`gopher/`](sdf/gopher/)/[`html/`](sdf/html/) dirs.

Assumes ssh key auth is already set up for each host. `~/.ssh/config`
has the specifics: `sdf.org` maps to user `bren`, and `cosmic.voyage`,
`envs.net`, and `tilde.green` to `brennan`, all on
`id_ed25519_brennanbrown_ca`.

## What's Not Tracked

 [`.gitignore`](.gitignore) keeps these on disk, but out of git:

- **Credentials**: `.ssh/`, `.gnupg/`, `.keychain/`, `.google_authenticator`,
  `.alpine.passfile`, `.alpine-smime/`, `.twurlrc`, `.bbjrc`, `.bink/`,
  weechat `sec.conf`/`irc.conf`, `.irssi/`, `identity.pem`, `.pinerc`,
  `.muttrc` (envs IMAP password)
- **Mail**: `mail/`, `Mail/`, `.mail/`, `mbox`
- **Logs & history**: shell histories, weechat logs, `.local/state/`
- **Caches**: `.cache/` (this alone is ~100M of dnf junk on club),
  `eln-cache/`

The files sync to disk and are never committed.

## Wiki

[`wiki/`](wiki/) (under construction) is a markdown wiki documenting each mirror and how
the accounts overlap ([`architecture.md`](wiki/architecture.md) is the cross-host map). Build it
to HTML with [`build.sh`](build.sh), which needs `pandoc`. Output lands in [`docs/`](docs/),
which is tracked and served by GitHub Pages at
[tilde.land](https://tilde.land). Links between pages are written as `.md`
so they work on GitHub; the build rewrites them to `.html`.

## License

Content is licensed under the GNU Affero General Public License
v3.0 or later (AGPL-3.0-or-later). See [`LICENSE`](LICENSE). Dotfiles and
configs remain under whatever licenses their respective authors chose.
