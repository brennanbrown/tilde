# ~/.profile - Quality of life settings for tilde.pink (NetBSD/sh)

# Environment variables
export EDITOR=micro
export VISUAL=micro
export PAGER=less
export LESS='-R'

# Better history
export HISTSIZE=1000
export HISTFILESIZE=2000

# Add local bin to PATH if it exists
if [ -d "$HOME/bin" ]; then
    PATH="$HOME/bin:$PATH"
fi

# Add local sbin to PATH if it exists
if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
fi

# Useful aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias h='history'
alias grep='grep --color=auto'

# Safety aliases
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Quick directory navigation
alias ~='cd ~'
alias desk='cd ~/Desktop'

# Quick edit common files
alias profile='$EDITOR ~/.profile'
alias plan='$EDITOR ~/.plan'
alias project='$EDITOR ~/.project'

# Quick Gemini/Gopher navigation
alias gemini='cd ~/public_gemini'
alias gopher='cd ~/public_gopher'

# System info aliases
alias df='df -h'
alias du='du -h'

# Network aliases
alias ping='ping -c 4'

# Quick check who's online
alias who='w'

# Less-like viewing for common commands
alias less='less -R'

# Set umask for better default permissions
umask 022

# Print welcome message
echo "Welcome to tilde.pink, $(whoami)!"
echo "Type 'w' to see who's online, 'finger <user>' to learn about others."
