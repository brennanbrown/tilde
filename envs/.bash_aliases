#
# User specific aliases and functions
#

alias grep='grep --color'
alias psa='ps -axuwf'

#alias ls='exa -ag'
alias la='exa -lag'
#alias ll='exa -lahg'

# todo-txt
alias todo='todo-txt'
alias t='todo-txt'

# twtxt
alias twtxt_users="curl 'https://twtxt.envs.net/api/plain/users'"
twtxt_user() { curl 'https://twtxt.envs.net/api/plain/users?q='"$1" ; }
twtxt_user_url() { curl 'https://twtxt.envs.net/api/plain/users?url='"$1" ; }

alias twtxt_tweets="curl 'https://twtxt.envs.net/api/plain/tweets'"
twtxt_tweet() { curl 'https://twtxt.envs.net/api/plain/tweets?q='"$1" ; }

alias twtxt_tags="curl 'https://twtxt.envs.net/api/plain/tags'"
twtxt_tag() { curl 'https://twtxt.envs.net/api/plain/tags/'"$1" ; }

alias twtxt_mentions="curl 'https://twtxt.envs.net/api/plain/mentions'"
twtxt_mention_url() { curl 'https://twtxt.envs.net/api/plain/mentions?url='"$1" ; }

#
# nullpointer on 0x0.st
#
0file() { curl -F"file=@$1" https://0x0.st/ ; }
0url() { curl -F"url=$1" https://0x0.st/ ; }
0short() { curl -F"shorten=$1" https://0x0.st/ ; }
