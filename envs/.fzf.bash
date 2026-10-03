# Setup fzf
# ---------
if [[ ! "$PATH" == */opt/services/fzf/bin* ]]; then
  export PATH="${PATH:+${PATH}:}/opt/services/fzf/bin"
fi

# Auto-completion
# ---------------
[[ $- == *i* ]] && source "/opt/services/fzf/shell/completion.bash" 2> /dev/null

# Key bindings
# ------------
source "/opt/services/fzf/shell/key-bindings.bash"
