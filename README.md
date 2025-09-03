# Cynetics CLI

The next-generation AI-driven command-line tool.

## Features

- Universal model access (OpenAI, Ollama, Anthropic, OpenRouter, Qwen, DeepSeek, Cohere, Google)
- Extensible with MCP tools
- Interactive REPL and single-command execution
- Rich TUI interface
- Plugin system for models and tools
- Agent system for executing tool commands
- Context fusion from multiple models
- Model voting and consensus
- Knowledge snapshots for state persistence
- Self-extending CLI (generate new subcommands on demand)
- Agent mesh for collaborative AI workflows
- Adaptive personality and modes
- Cross-protocol operability (APIs, SSH, Git, etc.)
- Team mode for collaborative CLI sessions
- Secure agentic task delegation with sandboxing
- Multi-modal CLI (images, audio, text, video in/out)
- Self-healing errors (detects and fixes broken commands or missing dependencies)
- Intelligent autocomplete that suggests entire workflows
- Contextual "playbooks" for recurring multi-step tasks
- Conversational debugging of commands
- AI-driven CLI tutorials that teach new shell commands interactively

## Installation

```bash
pip install -e .
```

## Usage

```bash
cynetics --help
```

### REPL Mode

Start the interactive REPL mode:

```bash
cynetics run --repl
```

In REPL mode, you can use available tools. Type `help` to see a list of available commands.

### Self-Extending CLI

Generate new CLI commands on demand:

```bash
cynetics generate --description "List files in a directory" --api-key YOUR_OPENAI_API_KEY
```

### Adaptive Personality & Modes

Manage agent personality and modes:

```bash
# List available modes
cynetics personality --list-modes

# Set agent mode
cynetics personality --mode creative
```

### Cross-Protocol Operability

Execute actions across different protocols:

```bash
# API example
cynetics protocol --protocol api --action get_posts --config api_config.json --param endpoint=posts --param method=GET

# Git example
cynetics protocol --protocol git --action status --param repo_path=/path/to/repo

# SSH example (requires SSH configuration)
cynetics protocol --protocol ssh --action command --param host=example.com --param user=username --param command="ls -la"
```

### Team Mode

Collaborate with other users in a team session:

```bash
# Create a new team session
cynetics team --create --user-id user1 --user-name "Alice" --session-id my_team_session

# Join an existing session and send a message
cynetics team --session-id my_team_session --user-id user2 --user-name "Bob" --send-message "Hello Alice!"

# View chat history
cynetics team --session-id my_team_session --user-id user1 --user-name "Alice" --get-history

# Share context between team members
cynetics team --session-id my_team_session --user-id user1 --user-name "Alice" --set-context project_status "In progress"

# View shared context
cynetics team --session-id my_team_session --user-id user2 --user-name "Bob" --get-context
```

### Agent Mesh

Manage collaborative AI agents:

```bash
# Create a new agent
cynetics agent-mesh --create --name "Researcher" --capabilities research --capabilities data_analysis

# List all agents
cynetics agent-mesh --list-agents

# Start all agents
cynetics agent-mesh --start-all
```

### Knowledge Snapshots

Save and load state/context across sessions:

```bash
# Save a snapshot
cynetics knowledge-snapshot --save my_project data.json

# List all snapshots
cynetics knowledge-snapshot --list

# Load a snapshot
cynetics knowledge-snapshot --load my_project
```

### Secure Task Delegation

Execute tasks in secure environments:

```bash
# Create a task
cynetics task-delegation --create --name "Setup Project" --description "Set up a new project" --command "mkdir project && cd project && git init" --environment sandbox

# Execute a task
cynetics task-delegation --execute task_id

# List tasks
cynetics task-delegation --list-tasks
```

### Multi-modal CLI

Handle images, audio, text, and video:

```bash
# Process text
cynetics multimodal --input "Hello, world!" --type text

# Process an image
cynetics multimodal --input image.jpg --type image

# List supported media types
cynetics multimodal --list-types
```

### Self-Healing System

Detect and fix command issues:

```bash
# Diagnose a command
cynetics self-healing --diagnose "python script.py"

# Attempt to fix a command
cynetics self-healing --fix "python script.py"

# Show diagnosis history
cynetics self-healing --history
```

### CLI Tutorials

Learn new shell commands interactively:

```bash
# List available tutorials
cynetics cli-tutorial --list

# Start an interactive tutorial
cynetics cli-tutorial --start basic_navigation

# Get a recommended tutorial
cynetics cli-tutorial --recommend
```

### Intelligent Autocomplete

Get suggestions for entire workflows:

```bash
# Get suggestions
cynetics autocomplete --suggest "git"

# List all workflows
cynetics autocomplete --workflows

# Search workflows
cynetics autocomplete --search-workflows "docker"
```

### Playbooks

Execute recurring multi-step tasks:

```bash
# List playbooks
cynetics playbooks --list

# Create a playbook
cynetics playbooks --create --name "Git Setup" --description "Set up a new Git repository" --steps-file git_steps.yaml

# Execute a playbook
cynetics playbooks --execute playbook_id

# Show playbook details
cynetics playbooks --show playbook_id
```

### Conversational Debugging

Debug commands with conversational explanations:

```bash
# Debug a command
cynetics debugger --debug "ls /nonexistent"

# Explain an error
cynetics debugger --explain "command not found"

# Show debug history
cynetics debugger --history
```

### Configuration

Create a `config.yaml` file in the root directory to configure model providers and tools. See `config.yaml.example` for an example configuration.

### Plugins

Plugins can be added to the `plugins` directory. Each plugin should be a Python file that defines a tool class inheriting from `BaseTool`.

## Development

### Project Structure

- `cynetics/`: Main package
  - `cli/`: CLI implementation
    - `main.py`: Main CLI entry point
    - `self_extending.py`: Self-extending CLI system
    - `advanced_repl.py`: Advanced REPL with history and autocomplete
  - `commands/`: CLI commands
  - `config.py`: Configuration loading
  - `models/`: Model providers
  - `tools/`: Built-in tools
  - `plugins/`: Plugin loader
  - `agents/`: Agent implementations
    - `mesh.py`: Agent mesh system
  - `personality/`: Adaptive personality system
  - `protocols/`: Cross-protocol operability system
  - `team/`: Team mode system
  - `context/`: Context fusion system
  - `voting/`: Model voting system
  - `knowledge/`: Knowledge snapshot system
  - `security/`: Security features
    - `task_delegation.py`: Secure task delegation system
  - `utils/`: Utility functions
    - `tutorial.py`: AI-driven CLI tutorial system
    - `autocomplete.py`: Intelligent autocomplete system
    - `playbooks.py`: Contextual playbooks system
    - `debugger.py`: Conversational debugging system
    - `multimodal.py`: Multi-modal CLI system
    - `self_healing.py`: Self-healing error system
    - `tui.py`: Rich TUI utilities
- `plugins/`: Directory for plugin modules
- `snapshots/`: Directory for knowledge snapshots (created automatically)
- `commands/`: Directory for generated commands (created automatically)
- `team_sessions/`: Directory for team mode session data (created automatically)
- `playbooks/`: Directory for contextual playbooks
- `workflows/`: Directory for autocomplete workflows
- `tutorials/`: Directory for CLI tutorials
- `tasks/`: Directory for secure task delegation
- `agent_mesh/`: Directory for agent mesh data
- `debug_sessions/`: Directory for debugging sessions
- `healing_sessions/`: Directory for self-healing sessions

### Advanced Features

#### Agent Mesh

The agent mesh system allows spawning multiple AI agents that collaborate or compete. Agents can work together on complex tasks, sharing context and results.

#### Context Fusion

The context fusion system allows merging context from multiple models (cloud + local) into a single reasoning flow. This enables hybrid workflows where different models contribute to a unified context.

#### Model Voting/Consensus

The model voting system provides several methods for combining responses from multiple models:
- Majority vote: Selects the most common response
- Weighted voting: Considers provider weights for scoring
- Best-of-N: Generates multiple responses and selects the best one based on a scoring function

#### Knowledge Snapshots

Knowledge snapshots allow saving and reloading agent state/context across sessions. This feature enables agents to remember projects and tasks long-term, providing continuity between CLI sessions.

#### Self-Extending CLI

The self-extending CLI feature allows Cynetics to generate new subcommands or tools for itself on demand using its own AI abilities. This makes the CLI truly extensible and adaptive to new needs.

#### Adaptive Personality & Modes

The adaptive personality system allows switching between different agent modes:
- **Precision Mode**: Tool-like precision for accurate, deterministic responses
- **Creative Mode**: Creative exploration for brainstorming and idea generation
- **Autonomous Mode**: Autonomous agent mode for long-running, independent tasks

Each mode adjusts the underlying model parameters to optimize for the specific type of task.

#### Cross-Protocol Operability

The cross-protocol operability system allows the CLI to interact with various protocols and systems:
- **APIs**: REST API interactions with configurable endpoints and headers
- **SSH**: Secure shell command execution on remote systems
- **Git**: Version control operations (status, log, commit, push, pull)

This feature enables bridging AI with APIs, SSH, containers, git workflows, cloud deployments, and other systems directly from the CLI.

#### Team Mode

The team mode system allows multiple users to connect to the same CLI session collaboratively:
- **Chat**: Real-time messaging between team members
- **Shared Context**: Shared key-value store for collaboration
- **Persistent Sessions**: Session data stored on disk for continuity

This feature enables collaborative CLI sessions where multiple users can work together on projects, share context, and communicate in real-time.

### Secure Agentic Task Delegation

The secure task delegation system allows tasks to run in sandboxes or containers for safety:
- **Local Execution**: Run tasks in the local environment
- **Sandboxed Execution**: Run tasks in isolated temporary directories
- **Container Execution**: Run tasks in Docker containers
- **Timeout Protection**: Automatically terminate long-running tasks
- **Path Restrictions**: Limit file system access for security

This feature enables safe execution of potentially dangerous commands while maintaining security.

### Multi-modal CLI

The multi-modal CLI system supports images, audio, text, and video in/out:
- **Text Processing**: Standard text input/output
- **Image Handling**: Process image files with metadata
- **Audio Support**: Handle audio files
- **Video Processing**: Work with video files
- **Format Detection**: Automatic format recognition

This feature extends the CLI beyond text to handle various media types.

### Self-Healing Errors

The self-healing system detects and fixes broken commands or missing dependencies automatically:
- **Command Diagnosis**: Analyze why commands fail
- **Dependency Detection**: Identify missing modules or packages
- **Automatic Installation**: Attempt to install missing dependencies
- **Fix Suggestions**: Provide actionable solutions
- **Diagnosis History**: Track previous issues and solutions

This feature reduces friction by automatically resolving common issues.

### Intelligent Autocomplete

The intelligent autocomplete system suggests entire workflows, not just flags:
- **Command Suggestions**: Recommend commands based on partial input
- **Workflow Recommendations**: Suggest complete multi-step processes
- **Flag Completion**: Complete command flags intelligently
- **Contextual Matching**: Match based on tags and descriptions
- **Search Functionality**: Find workflows by keyword

This feature accelerates CLI usage by suggesting complete solutions.

### Contextual Playbooks

The playbooks system manages recurring multi-step tasks:
- **Playbook Creation**: Define multi-step processes as YAML files
- **Step Execution**: Run each step with error handling
- **Dry Run Mode**: Preview execution without running commands
- **Tag-based Organization**: Categorize playbooks for easy finding
- **Search Capability**: Find playbooks by name, description, or tags

This feature standardizes complex processes into reusable templates.

### Conversational Debugging

The conversational debugging system provides natural language explanations of errors:
- **Command Analysis**: Execute and analyze command results
- **Error Explanation**: Provide plain English descriptions of issues
- **Fix Suggestions**: Recommend specific solutions
- **Debug History**: Track previous debugging sessions
- **Multiple Detail Levels**: Adjust analysis depth as needed

This feature makes debugging more accessible to users of all skill levels.

### AI-Driven CLI Tutorials

The tutorial system teaches new shell commands interactively:
- **Built-in Tutorials**: Predefined learning modules for common tasks
- **Interactive Learning**: Hands-on practice with real commands
- **Progress Tracking**: Remember completed tutorials
- **Personalized Recommendations**: Suggest next tutorials based on progress
- **Command Details**: Deep dive into specific commands

This feature helps users learn the CLI through guided interactive experiences.