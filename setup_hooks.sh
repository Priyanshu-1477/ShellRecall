#!/bin/bash

# This is the code we want to add into your .zshrc file
ZSH_HOOK=$(cat <<'EOF'
# === ShellRecall Hooks for Zsh ===
preexec() {
    export LAST_COMMAND="$1"
}
precmd() {
    python3 ~/ShellRecall/shellrecall.py "$LAST_COMMAND" "$PWD" $?
}
EOF
)

# Path to your zsh config file
SHELL_CONFIG="$HOME/.zshrc"

# If our hook is not already present in your zshrc, then add it
if ! grep -q "ShellRecall Hooks for Zsh" "$SHELL_CONFIG"; then
    echo "Adding ShellRecall hooks to $SHELL_CONFIG"
    echo "$ZSH_HOOK" >> "$SHELL_CONFIG"
    echo "✅ ShellRecall Zsh hook added! Restart your terminal to activate."
else
    echo "⚠️  ShellRecall Zsh hook already exists in $SHELL_CONFIG"
fi
