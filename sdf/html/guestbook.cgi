#!/usr/pkg/bin/perl
# guestbook.cgi: flat-file guestbook, no modules beyond core perl.
#
# SDF notes (see wiki.sdf.org/doku.php?id=cgi_passing_parameters and
# sdf.org/?faq?WEB?02):
#   - file must end in .cgi and be chmod +x
#   - can live anywhere under ~/html, no cgi-bin required
#   - run `mkhomepg -p` after uploading to set secure web permissions
#   - $DATA_FILE lives outside ~/html so it can't be fetched as plain
#     text over the web; .htaccess denies it too as a second layer.
#     $ENV{HOME} is NOT set under suexec on SDF, so the home path is
#     hardcoded below -- update it if the account ever moves.

use strict;
use warnings;
use Fcntl qw(:flock);

my $DATA_FILE   = "/sdf/arpa/af/b/bren/guestbook.dat";
my $MAX_NAME    = 60;
my $MAX_MESSAGE = 1000;
my $MAX_ENTRIES_SHOWN = 50;

# ---- read request -----------------------------------------------------

my $method = $ENV{REQUEST_METHOD} || 'GET';
my %params;

if ($method eq 'POST') {
    my $len = $ENV{CONTENT_LENGTH} || 0;
    my $body = '';
    read(STDIN, $body, $len) if $len > 0;
    %params = parse_form($body);
} else {
    %params = parse_form($ENV{QUERY_STRING} || '');
}

# ---- handle submission --------------------------------------------------

my $notice = '';

if ($method eq 'POST') {
    my $name    = trim($params{name}    // '');
    my $message = trim($params{message} // '');
    my $url     = trim($params{url}     // '');
    my $trap    = trim($params{website} // '');  # honeypot field, must stay empty

    if ($trap ne '') {
        # bot filled the honeypot; silently drop, pretend success
        $notice = 'Thanks for signing!';
    } elsif ($name eq '' || $message eq '') {
        $notice = 'Both name and message are required. Nothing was saved.';
    } elsif (length($name) > $MAX_NAME) {
        $notice = "Name is too long (max $MAX_NAME characters). Nothing was saved.";
    } elsif (length($message) > $MAX_MESSAGE) {
        $notice = "Message is too long (max $MAX_MESSAGE characters). Nothing was saved.";
    } else {
        add_entry($name, $message, $url);
        $notice = 'Thanks for signing!';
    }
}

# ---- render -------------------------------------------------------------

print "Content-type: text/html; charset=utf-8\n\n";

print <<"HEAD";
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Guestbook | bren.sdf.org</title>
  <meta name="description" content="Sign the guestbook at bren.sdf.org.">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="stylesheet" href="style.css">
</head>
<body>

<header>
  <h1>Guestbook | bren.sdf.org</h1>
  <nav>
    <a href="index.html">Home</a> &middot;
    <a href="sdf.html">What is SDF?</a> &middot;
    <a href="services.html">Services &amp; Tools</a> &middot;
    <a href="links.html">Links</a> &middot;
    <a href="keys.html">Keys</a> &middot;
    <a href="support.html">Support</a> &middot;
    <a href="guestbook.cgi" aria-current="page">Guestbook</a>
  </nav>
</header>
<hr>

<main>

  <p>
    Sign the guestbook! A small, old-web tradition: leave your name, a
    message, and (if you like) a link back to your own site, gopherhole,
    or capsule.
  </p>
HEAD

if ($notice) {
    print '  <p class="guestbook-notice">' . escape_html($notice) . "</p>\n";
}

print <<"FORM";
  <form method="post" action="guestbook.cgi" class="guestbook-form">
    <p>
      <label for="name">Name</label><br>
      <input type="text" id="name" name="name" maxlength="$MAX_NAME" required>
    </p>
    <p>
      <label for="url">Website (optional)</label><br>
      <input type="text" id="url" name="url" maxlength="200" placeholder="https://&hellip;">
    </p>
    <p>
      <label for="message">Message</label><br>
      <textarea id="message" name="message" rows="4" maxlength="$MAX_MESSAGE" required></textarea>
    </p>
    <!-- honeypot: hidden from real visitors via CSS, bots tend to fill every field -->
    <p class="guestbook-trap">
      <label for="website">Leave blank</label>
      <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
    </p>
    <p>
      <button type="submit">Sign the guestbook</button>
    </p>
  </form>

  <hr>

  <h2>Entries</h2>
FORM

my @entries = read_entries();

if (!@entries) {
    print "  <p><em>No entries yet. Be the first!</em></p>\n";
} else {
    my $shown = 0;
    for my $e (reverse @entries) {
        last if $shown >= $MAX_ENTRIES_SHOWN;
        $shown++;
        my ($ts, $name, $message, $url) = @$e;
        print "  <div class=\"guestbook-entry\">\n";
        print "    <p class=\"guestbook-meta\"><strong>" . escape_html($name) . "</strong>";
        if ($url ne '') {
            print " &middot; <a href=\"" . escape_html($url) . "\">" . escape_html($url) . "</a>";
        }
        print " <span class=\"guestbook-ts\">" . escape_html($ts) . "</span></p>\n";
        my $msg_html = escape_html($message);
        $msg_html =~ s/\n/<br>\n/g;
        print "    <p class=\"guestbook-message\">$msg_html</p>\n";
        print "  </div>\n";
    }
}

print <<"FOOT";

</main>
<hr>

<footer>
  <p>
    <small>
      (c) <a href="https://brennan.day">Brennan Kenneth Brown</a> &middot;
      <a href="https://www.gnu.org/licenses/agpl-3.0.en.html">AGPL-3.0</a> +
      <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.en">CC-BY-SA</a> &middot;
      hosted on <a href="https://sdf.org">sdf.org</a> &middot;
      <a href="https://github.com/brennanbrown/tilde">source</a>
    </small>
  </p>
</footer>

</body>
</html>
FOOT

exit 0;

# ---- helpers --------------------------------------------------------------

sub parse_form {
    my ($raw) = @_;
    my %out;
    for my $pair (split /&/, $raw) {
        next if $pair eq '';
        my ($k, $v) = split /=/, $pair, 2;
        $out{url_decode($k)} = url_decode($v // '');
    }
    return %out;
}

sub url_decode {
    my ($s) = @_;
    return '' unless defined $s;
    $s =~ tr/+/ /;
    $s =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/ge;
    return $s;
}

sub trim {
    my ($s) = @_;
    $s =~ s/^\s+|\s+$//g;
    return $s;
}

sub escape_html {
    my ($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/"/&quot;/g;
    return $s;
}

# one entry per line: timestamp \x01 name \x01 message \x01 url
# newlines in the message become the literal two-char sequence \n,
# and the escaping is undone when the line is read back.
sub add_entry {
    my ($name, $message, $url) = @_;
    my $ts = scalar localtime;
    my $enc_message = $message;
    $enc_message =~ s/\\/\\\\/g;
    $enc_message =~ s/\n/\\n/g;

    open(my $fh, '>>', $DATA_FILE) or return;
    flock($fh, LOCK_EX);
    print $fh join("\x01", $ts, $name, $enc_message, $url) . "\n";
    flock($fh, LOCK_UN);
    close($fh);
}

sub read_entries {
    my @out;
    return @out unless -e $DATA_FILE;
    open(my $fh, '<', $DATA_FILE) or return @out;
    flock($fh, LOCK_SH);
    while (my $line = <$fh>) {
        chomp $line;
        next if $line eq '';
        my ($ts, $name, $enc_message, $url) = split /\x01/, $line, 4;
        next unless defined $name;
        my $message = $enc_message // '';
        $message =~ s/\\n/\n/g;
        $message =~ s/\\\\/\\/g;
        push @out, [$ts, $name, $message, $url // ''];
    }
    flock($fh, LOCK_UN);
    close($fh);
    return @out;
}
