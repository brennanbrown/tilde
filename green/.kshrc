# skip this setup for non-interactive shells
[[ -o interactive && -t 0 ]] || return

# set some useful shell options
set -o emacs -o globstar
[[ -o ?backslashctrl ]] && set +o backslashctrl

# specify search path for autoloadable functions
FPATH=/usr/share/ksh/functions:~/.func${FPATH:+:$FPATH}

# save more commands in history
HISTSIZE=5000

# aliases for various command shortcuts
alias ll='ls -lFb'
alias la='ls -LaFb'

# show directory colors where possible
if command -v dircolors >/dev/null 2>&1; then
	if [[ -r ~/.dircolors ]]; then
		eval "$(command dircolors -b ~/.dircolors)"
	else
		eval "$(command dircolors -b)"
	fi
	alias ls='ls --color=auto' grep='grep --color=auto'
fi

# keep a shortened version of the current directory for the prompt
function _cd {
  "cd" "$@" || return

  if [[ $PWD == $HOME* && $HOME != / ]]; then
    _pwd=\~${PWD#$HOME}
    return
  fi

  _pwd="$PWD"
}
alias cd=_cd
_cd .

# use traditional trailing prompt characters based on user type
case ${ id -u; } in
  0) _prompt_char='#' ;;
  *) _prompt_char='$' ;;
esac

# put the current directory in the prompt
PS1='$_pwd $_prompt_char '
