# ~/.bash_logout: executed by bash(1) when login shell exits.

# clear home directory tmp folder
#[ -d ~/tmp ] && rm -r ~/tmp/*

# when leaving the console clear the screen to increase privacy
if [ "$SHLVL" = 1 ]; then
    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
fi
