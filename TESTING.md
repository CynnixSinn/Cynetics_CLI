# Cynetics CLI Test Script

This script tests the basic functionality of the Cynetics CLI.

## Setup

1. Create a `config.yaml` file based on `config.yaml.example`
2. Install the package: `pip install -e .`

## Basic Tests

### 1. Help Command
```bash
cynetics --help
```

### 2. REPL Mode
```bash
cynetics run --repl
```
In REPL mode, try:
- `help` - List available commands
- `tools` - List available tools
- `model list` - List available model providers
- `exit` - Exit REPL

### 3. Personality Modes
```bash
# List available modes
cynetics personality --list-modes

# Set a mode
cynetics personality --mode creative
```

### 4. Team Mode (collaborative sessions)
```bash
# Create a new team session
cynetics team --create --user-id user1 --user-name "Alice" --session-id test_session

# Send a message
cynetics team --session-id test_session --user-id user1 --user-name "Alice" --send-message "Hello, team!"

# View chat history
cynetics team --session-id test_session --user-id user1 --user-name "Alice" --get-history
```

### 5. Self-Extending CLI
```bash
# Generate a new command (requires OpenAI API key)
cynetics generate --description "List files in a directory" --api-key YOUR_OPENAI_API_KEY
```

## Expected Results

All commands should execute without errors and produce the expected output as described in the README.md.

## Troubleshooting

If you encounter any issues:
1. Check that all dependencies are installed: `pip install -e .`
2. Verify your config.yaml is properly formatted
3. Ensure required services (like Ollama) are running if using local models