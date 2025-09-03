import click
import json
from typing import List, Dict, Any
from pathlib import Path

class AgentMeshManager:
    """Manager for the agent mesh system."""
    
    def __init__(self, storage_dir: str = "agent_mesh"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.agents_file = self.storage_dir / "agents.json"
        self._load_agents()
    
    def _load_agents(self):
        """Load agents from file."""
        if self.agents_file.exists():
            with open(self.agents_file, 'r') as f:
                self.agents = json.load(f)
        else:
            self.agents = {}
            self._save_agents()
    
    def _save_agents(self):
        """Save agents to file."""
        with open(self.agents_file, 'w') as f:
            json.dump(self.agents, f, indent=2)
    
    def create_agent(self, name: str, capabilities: List[str]) -> Dict[str, Any]:
        """Create a new agent."""
        from datetime import datetime
        
        agent = {
            "name": name,
            "capabilities": capabilities,
            "status": "inactive",
            "created_at": datetime.now().isoformat(),
            "last_active": None
        }
        
        self.agents[name] = agent
        self._save_agents()
        
        return agent
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all agents."""
        return self.agents
    
    def get_agent(self, name: str) -> Dict[str, Any]:
        """Get an agent by name."""
        return self.agents.get(name, None)
    
    def update_agent_status(self, name: str, status: str) -> bool:
        """Update an agent's status."""
        if name in self.agents:
            from datetime import datetime
            self.agents[name]["status"] = status
            self.agents[name]["last_active"] = datetime.now().isoformat()
            self._save_agents()
            return True
        return False
    
    def remove_agent(self, name: str) -> bool:
        """Remove an agent."""
        if name in self.agents:
            del self.agents[name]
            self._save_agents()
            return True
        return False

@click.command()
@click.option('--create', is_flag=True, help='Create a new agent')
@click.option('--list-agents', is_flag=True, help='List all agents')
@click.option('--start-all', is_flag=True, help='Start all agents')
@click.option('--name', help='Name of the agent')
@click.option('--capabilities', multiple=True, help='Capabilities of the agent')
def agent_mesh(create, list_agents, start_all, name, capabilities):
    """Manage collaborative AI agents."""
    manager = AgentMeshManager()
    
    if create:
        if not name:
            click.echo("Error: --name is required to create an agent")
            return
        
        agent = manager.create_agent(name, list(capabilities))
        click.echo(f"Created agent: {agent['name']}")
        click.echo(f"Capabilities: {', '.join(agent['capabilities'])}")
        click.echo(f"Status: {agent['status']}")
    
    elif list_agents:
        agents = manager.list_agents()
        if not agents:
            click.echo("No agents found.")
            return
        
        click.echo("Available agents:")
        for agent_name, agent_data in agents.items():
            status_marker = "●" if agent_data["status"] == "active" else "○"
            click.echo(f"  {status_marker} {agent_name}")
            click.echo(f"    Capabilities: {', '.join(agent_data['capabilities'])}")
            click.echo(f"    Status: {agent_data['status']}")
            click.echo(f"    Created: {agent_data['created_at']}")
            if agent_data['last_active']:
                click.echo(f"    Last active: {agent_data['last_active']}")
            click.echo()
    
    elif start_all:
        agents = manager.list_agents()
        started_count = 0
        for agent_name in agents:
            if manager.update_agent_status(agent_name, "active"):
                started_count += 1
        
        click.echo(f"Started {started_count} agents.")
    
    else:
        click.echo("Agent Mesh System")
        click.echo("Use --create to create a new agent, --list-agents to see all agents, or --start-all to start all agents.")

if __name__ == "__main__":
    agent_mesh()