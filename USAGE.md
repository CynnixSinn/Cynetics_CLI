# Cynetics CLI

The next-generation AI-driven command-line tool.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Cynetics_CLI
```

Install the package in development mode:

```bash
pip install -e .
```

## Configuration

Create a `config.yaml` file in the root directory:

```yaml
model_providers:
  openai:
    api_key: "sk-..."  # Your OpenAI API key
    model: "gpt-4"
  ollama:
    host: "http://localhost:11434"
    model: "llama3"
  anthropic:
    api_key: "your-anthropic-api-key"
    model: "claude-3-opus-20240229"
  openrouter:
    api_key: "your-openrouter-api-key"
    model: "openai/gpt-4-turbo"
  qwen:
    api_key: "your-qwen-api-key"
    model: "qwen-max"
  deepseek:
    api_key: "your-deepseek-api-key"
    model: "deepseek-chat"
  cohere:
    api_key: "your-cohere-api-key"
    model: "command-r-plus"
  google:
    api_key: "your-google-api-key"
    model: "gemini-pro"

tools:
  enabled:
    - "file_manager"
    - "web_search"
    - "code_generation"
```

## Usage

### Help

Show available commands:

```bash
python -m cynetics.cli --help
```

### Generate New Commands

Create new CLI commands with AI:

```bash
python -m cynetics.cli generate --description "List files in a directory" --api-key YOUR_OPENAI_API_KEY
```

### Personality Management

List available personality modes:

```bash
python -m cynetics.cli personality --list-modes
```

Set personality mode:

```bash
python -m cynetics.cli personality --mode creative
```

### Managing Model Providers

List available model providers:

```bash
python -m cynetics.cli model-manager --list
```

View current provider configuration:

```bash
python -m cynetics.cli model-manager
```

### Protocol Operations

Execute actions across different protocols:

```bash
# API example
python -m cynetics.cli protocol --protocol api --action get_posts --param endpoint=posts --param method=GET

# Git example
python -m cynetics.cli protocol --protocol git --action status --param repo_path=/path/to/repo
```

### Team Collaboration

Create a team session:

```bash
python -m cynetics.cli team --create --session-id my_session --user-id user1 --user-name "Alice"
```

Join a team session:

```bash
python -m cynetics.cli team --session-id my_session --user-id user2 --user-name "Bob" --send-message "Hello Alice!"
```

## Development

### Project Structure

- `cynetics/`: Main package
  - `cli/`: CLI implementation
  - `commands/`: CLI commands
  - `config_module.py`: Configuration loading
  - `models/`: Model providers
  - `tools/`: Built-in tools
  - `plugins/`: Plugin loader
- `plugins/`: Directory for plugin modules

### Adding New Tools

1. Create a new tool class in `cynetics/tools/`
2. Inherit from `BaseTool`
3. Implement the required methods:
   - `name`: Tool name
   - `description`: Tool description
   - `run()`: Tool execution logic

### Adding New Model Providers

1. Create a new provider class in `cynetics/models/`
2. Inherit from `ModelProvider`
3. Implement the required methods:
   - `configure()`: Provider configuration
   - `generate()`: Text generation

## Testing

Run the test suite:

```bash
python test_cli.py
```

Run the demo:

```bash
python demo.py
```