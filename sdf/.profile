#ident	"@(#)/etc/stdprofile.sl 1.1 3.0 11/18/85 18386 "
#	This is the default standard profile provided to a user.
#	They are expected to edit it to meet their own needs.

# Hello there and welcome to your .profile!  The .profile is a
# way for you to initialize and customize your UNIX environment.
# The '#' character is the comment character.  Anything after the
# '#' is not interpreted by the shell.  Simply remove that character
# at the beginning of a line you want to make an active variable.
#
# I'd like to help you with a few notes about each part. 
#
# If your teacher asked you to edit this file, you'll need to 
# use the following PATH environment variable.
#PATH=/sys/classroom/bin:/bin:/usr/bin:/usr/local/bin

# This sets the environment variable "MAIL" for the location of your
# email file.  Typically email is spooled in /usr/mail with the user's
# login (enviroment variable LOGNAME) for the file's name.
MAIL=/mail/${LOGNAME:?}

# Which editor?  Well, here is the standard and then the VIsual editor
# based off of ex (EXtended ed).  But since you might not know these,
# we will give you "pico".
#EDITOR=/bin/ed
#VISUAL=/usr/bin/vi
EDITOR=/usr/pkg/bin/pico

# Neat hacks for the David Korn's shell.
# standard prompt is the dollar sign.  The shell comment character
# if you can't tell is the pound (#) sign.  Uncomment out the follow
# and delete the line after it (or comment it out) if you would like
# the standard UNIX Korn shell prompt.
#
# Normal UNIX prompt
PS1="$ " 
#
# This one gives you the return code for the last command executed
# and the present working directory
#PS1=['$?:${PWD#${PWD%/*/*/*}/}> '

# here is an example of a KSH function.  This one puts the current
# directory and hostname in your prompt
#host=`uname -n`

#chdir ()
#{
#	\cd ${*:-$HOME} && PS1="$host:$(pwd)> "
#}

#alias cd=chdir
#cd

# This tells the system what terminal you are using or emulating.  We do
# support a number of terminals and can infact support more.  For more 
# ideas, you can look in /usr/lib/terminfo.  Default TTY is typically a
# DEC vt100.
TERM=vt100

# stty (Set TTY) sets up your TTY.  Note, if you have problems with
# your backspace key, try changing the "erase '^h'" to "erase '^?'".
# If that still does not help, type stty erase at the shell prompt
#and then hit your backspace key.

stty erase '^?' echoe

# The following can be used for setting up the number of lines and 
# columns you are using.  Most typical PC-COMM programs use 24 lines
# by 79 or 80 columns.  These settings (commented out) are typically
# used for TTYs .. experiment in sizing your own.
#LINES=25
#COLUMNS=80
#
# stty rows 25 cols 80

# Now lets go ahead and make those enviroment variables active!  export 'em!
export MAIL PS1 TERM EDITOR VISUAL PATH

/usr/pkg/bin/guestbook -l 20
echo
echo "Welcome to the SDF Public Access UNIX system. (est. 1987)\n"
echo "For quick help, type 'help'"
echo "For detailed questions and answers, type 'faq'"
echo "For user discussion boards and software requests, type 'bboard'"
echo "For interactive discussions, type 'com'"
echo "To setup your homepage, type 'mkhomepg'"
echo "to create your URL http://$LOGNAME.freeshell.org, type 'mkhomepg -a'\n"
echo "Explore and Enjoy!\n"
