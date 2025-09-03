#!/usr/bin/env python3
\"\"\"
Demo script for Cynetics CLI showcasing its capabilities.
\"\"\"

import subprocess
import sys
import os
import time

def run_command(command, description):
    \"\"\"Run a command and print its output.\"\"\"
    print(f\"\\n=== {description} ===\")
    print(f\"Command: {command}\")
    print(\"-\" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.stdout:
            print(\"Output:\")
            print(result.stdout)
        if result.stderr:
            print(\"Errors:\")
            print(result.stderr)
            
        print(f\"Return code: {result.returncode}\")
        return result.returncode == 0
    except Exception as e:
        print(f\"Error running command: {e}\")
        return False

def main():
    \"\"\"Run demo commands.\"\"\"
    print(\"Cynetics CLI Demo\")
    print(\"=\" * 50)
    
    # Show help
    run_command(\"python -m cynetics.cli.main --help\", \"Show CLI help\")
    
    time.sleep(1)
    
    # Show personality modes
    run_command(\"python -m cynetics.cli.main personality --list-modes\", \"List personality modes\")
    
    time.sleep(1)
    
    # Show available tools
    run_command(\"python -m cynetics.cli.main run --repl <<< tools\", \"List available tools in REPL\")
    
    time.sleep(1)
    
    # Show agent mesh capabilities
    run_command(\"python -m cynetics.cli.main agent-mesh --list-agents\", \"List available agents\")
    
    time.sleep(1)
    
    # Show autocomplete workflows
    run_command(\"python -m cynetics.cli.main autocomplete --workflows\", \"List available workflows\")
    
    time.sleep(1)
    
    # Show playbooks
    run_command(\"python -m cynetics.cli.main playbooks --list\", \"List available playbooks\")
    
    print(\"\\n\" + \"=\" * 50)
    print(\"Demo completed!\")
    print(\"Cynetics CLI showcases many advanced features including:\")
    print(\"- Universal model access (OpenAI, Ollama, Anthropic, etc.)\")
    print(\"- Extensible with MCP tools\")
    print(\"- Interactive REPL and single-command execution\")
    print(\"- Rich TUI interface\")
    print(\"- Plugin system for models and tools\")
    print(\"- Agent system for executing tool commands\")
    print(\"- Context fusion from multiple models\")
    print(\"- Model voting and consensus\")
    print(\"- Knowledge snapshots for state persistence\")
    print(\"- Self-extending CLI (generate new subcommands on demand)\")
    print(\"- Agent mesh for collaborative AI workflows\")
    print(\"- Adaptive personality and modes\")
    print(\"- Cross-protocol operability (APIs, SSH, Git, etc.)\")
    print(\"- Team mode for collaborative CLI sessions\")
    print(\"- Secure agentic task delegation with sandboxing\")
    print(\"- Multi-modal CLI (images, audio, text, video in/out)\")
    print(\"- Self-healing errors\")
    print(\"- Intelligent autocomplete\")
    print(\"- Contextual playbooks\")
    print(\"- Conversational debugging\")
    print(\"- AI-driven CLI tutorials\")

if __name__ == \"__main__\":
    main()
