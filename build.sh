#!/bin/sh
# Build the wiki: markdown in wiki/ (plus the repo README) -> HTML in docs/
# docs/ is served by GitHub Pages at tilde.land. Links between pages are
# written as .md (so they work on GitHub) and rewritten to .html here;
# ../README.md becomes readme.html.
set -eu
cd "$(dirname "$0")"

mkdir -p docs
cp wiki/style.css docs/
touch docs/.nojekyll          # serve plain static files, skip Jekyll
echo tilde.land > docs/CNAME  # custom domain for GitHub Pages

for f in wiki/*.md README.md; do
  name=$(basename "$f" .md | tr 'A-Z' 'a-z')
  pandoc -s -f markdown -t html \
    --css=style.css \
    --metadata pagetitle="$name - tilde wiki" \
    "$f" | sed -e 's|\.\./README\.md|readme.html|g' \
               -e 's/\.md#/.html#/g' -e 's/\.md"/.html"/g' > "docs/$name.html"
done

echo "built $(ls docs/*.html | wc -l | tr -d ' ') pages -> docs/"
