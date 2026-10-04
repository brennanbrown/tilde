#!/usr/bin/env python3
"""Generate ~brennan's pubnix pages from this template folder.

  python3 template/generate.py

Single source of truth:
  skel.html          page skeleton (tokens are {{LIKE_THIS}})
  pages/*.html       shared body fragments, one per page
  art/{host}.txt     ASCII banner for the index page (optional)
  tilde.css          copied verbatim into each host's public_html/
  HOSTS below        host registry: drives the tilde table AND decides
                     which hosts get pages (gen=True)

Writes {host}/public_html/{index,writing,keys,support}.html for every
host with gen=True. town/club/sdf keep their own established pages.
"""
import html
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent

# Table order = row order in the "Tildeverse Homes" table.
HOSTS = [
    dict(key="town",   name="tilde.town",    url="https://tilde.town/~brennan",  login="brennan", email="brennan@tilde.town",    note="intentional digital community built around shared tools"),
    dict(key="pink",   name="tilde.pink",    url="gemini://tilde.pink/~brennan", login="brennan", email="brennan@tilde.pink",    note="small tilde with strong gemini/gopher culture"),
    dict(key="club",   name="tilde.club",    url="https://tilde.club/~brennan",  login="brennan", email="brennan@tilde.club",    note="the tilde that started the modern wave (2014)"),
    dict(key="sdf",    name="sdf.org",       url="http://bren.sdf.org",         login="bren",    email="bren@sdf.org",          note="public access unix system running since 1987"),
    dict(key="cosmic", name="cosmic.voyage", url="https://cosmic.voyage/Genawaaboonagak", login="brennan", email="brennan@cosmic.voyage", note="pubnix built around a shared science-fiction story", gen=True, host_url="https://cosmic.voyage"),
    dict(key="envs",   name="envs.net",      url="https://envs.net/~brennan",    login="brennan", email="brennan@envs.net",      note="minimalist tilde with a long service list", gen=True, host_url="https://envs.net"),
    dict(key="green",  name="tilde.green",   url="https://tilde.green/~brennan", login="brennan", email="brennan@tilde.green",   note="2022 tilde focused on creativity and wildness", gen=True, host_url="https://tilde.green"),
]

# Per-host paragraph inserted at {{FLAVOR}} in pages/index.html.
FLAVOR = {
    "cosmic": """<p><a href="https://cosmic.voyage">cosmic.voyage</a> is a pubnix built around a
collaborative science-fiction story told through ships' logs. I crew the
Genawaaboonagak &mdash; my
<a href="https://cosmic.voyage/ships/Genawaaboonagak">entries</a> live on the relay.</p>""",
    "envs": """<p><a href="https://envs.net">envs.net</a> is the minimalist one: a long
service list and little fuss. My account is configured mostly for mail
(mutt) and chat (weechat), so consider this page a signpost more than a home.</p>""",
    "green": """<p>This is my fresh page on <a href="https://tilde.green">tilde.green</a>, a
2022 tilde focused on creativity and wildness.</p>""",
}

# Per (host, page) fragment inserted at {{EXTRA}}.
EXTRA = {
    ("cosmic", "writing"): """<li><a href="https://cosmic.voyage/ships/Genawaaboonagak">Genawaaboonagak</a>: my
  ship's logs on the cosmic.voyage relay</li>
""",
}

# page -> (title, h1, meta description, has_ascii_art)
PAGES = {
    "index":   ("~brennan @ {name}", "~brennan @ {name}",
                "Brennan Kenneth Brown on {name}: writer, web developer, small web.", True),
    "writing": ("Writing | ~brennan @ {name}", "Writing | ~brennan",
                "Where Brennan Kenneth Brown writes: blogs, mirrors, and recommended articles.", False),
    "keys":    ("Keys | ~brennan @ {name}", "Keys | ~brennan",
                "Brennan Kenneth Brown's public keys: SSH, PGP, age, Cosign, Minisign, Keyoxide.", False),
    "support": ("Support | ~brennan @ {name}", "Support | ~brennan",
                "Support Brennan Kenneth Brown's writing and open-source work.", False),
}

NAV = [("index.html", "Home"), ("writing.html", "Writing"),
       ("keys.html", "Keys"), ("support.html", "Support")]

# Extra nav links appended after NAV, per host key.
EXTRA_NAV = {
    "cosmic": [("https://cosmic.voyage/ships/Genawaaboonagak", "Logs")],
}


def nav(active, extra=()):
    return " &middot;\n".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV + list(extra))


def tilde_table(current):
    rows = ["<table>",
            "<tr><th>Host</th><th>Login</th><th>Mail</th><th>What It Is</th></tr>"]
    for h in HOSTS:
        if h["key"] == current:
            cell = f'<td><strong>{h["name"]}</strong></td>'
            note = h["note"] + " (you are here)"
        else:
            cell = f'<td><a href="{h["url"]}">{h["name"]}</a></td>'
            note = h["note"]
        rows.append(f'<tr>{cell}<td>{h["login"]}</td>'
                    f'<td><a href="mailto:{h["email"]}">{h["email"]}</a></td>'
                    f'<td>{note}</td></tr>')
    rows.append("</table>")
    return "\n".join(rows)


def ascii_art(key):
    path = ROOT / "art" / f"{key}.txt"
    if not path.exists():
        return ""
    return f'<pre class="ascii">{html.escape(path.read_text().rstrip(), quote=False)}</pre>\n'


def main():
    skel = (ROOT / "skel.html").read_text()
    for h in HOSTS:
        if not h.get("gen"):
            continue
        outdir = REPO / h["key"] / "public_html"
        outdir.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "tilde.css", outdir / "tilde.css")
        for page, (title, h1, desc, has_art) in PAGES.items():
            body = (ROOT / "pages" / f"{page}.html").read_text()
            body = (body.replace("{{EMAIL}}", h["email"])
                        .replace("{{FLAVOR}}", FLAVOR.get(h["key"], ""))
                        .replace("{{TILDE_TABLE}}", tilde_table(h["key"]))
                        .replace("{{EXTRA}}", EXTRA.get((h["key"], page), "")))
            doc = (skel.replace("{{TITLE}}", title.format(name=h["name"]))
                       .replace("{{DESC}}", desc.format(name=h["name"]))
                       .replace("{{H1}}", h1.format(name=h["name"]))
                       .replace("{{CLASS}}", h["key"])
                       .replace("{{ART}}", ascii_art(h["key"]) if has_art else "")
                       .replace("{{NAV}}", nav(f"{page}.html", EXTRA_NAV.get(h["key"], ())))
                       .replace("{{BODY}}", body.strip())
                       .replace("{{HOST_URL}}", h["host_url"])
                       .replace("{{HOST_NAME}}", h["name"]))
            out = outdir / f"{page}.html"
            out.write_text(doc)
            print("wrote", out)


if __name__ == "__main__":
    main()
