import threading
import time
import uuid
from typing import Dict, Any, List, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class AgentStatus(Enum):
    """Enumeration of agent statuses."""
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class AgentMessage:
    """A message between agents."""
    id: str
    sender: str
    recipient: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

class CollaborativeAgent:
    """An AI agent that can collaborate with other agents."""
    
    def __init__(self, agent_id: str, name: str, capabilities: List[str]):
        self.id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.message_queue = []
        self.message_handlers = {}
        self.on_message_callback = None
    
    def set_message_handler(self, message_type: str, handler: Callable):
        """Set a handler for a specific message type."""
        self.message_handlers[message_type] = handler
    
    def set_on_message_callback(self, callback: Callable):
        """Set a callback for when messages are received."""
        self.on_message_callback = callback
    
    def send_message(self, recipient: str, content: str, message_type: str = "default") -> AgentMessage:
        """Send a message to another agent."""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.id,
            recipient=recipient,
            content=content,
            timestamp=datetime.now(),
            metadata={"type": message_type}
        )
        return message
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent."""
        self.message_queue.append(message)
        self.last_active = datetime.now()
        
        # Call the on_message callback if set
        if self.on_message_callback:
            self.on_message_callback(message)
        
        # Handle the message based on type
        message_type = message.metadata.get("type", "default") if message.metadata else "default"
        if message_type in self.message_handlers:
            self.message_handlers[message_type](message)
    
    def process_messages(self):
        """Process messages in the queue."""
        while self.message_queue:
            message = self.message_queue.pop(0)
            # In a real implementation, you would process the message here
            print(f"[{self.name}] Received message from {message.sender}: {message.content}")
    
    def start(self):
        """Start the agent."""
        self.status = AgentStatus.RUNNING
        print(f"Agent {self.name} started")
    
    def stop(self):
        """Stop the agent."""
        self.status = AgentStatus.STOPPED
        print(f"Agent {self.name} stopped")
    
    def execute_task(self, task: str) -> str:
        """Execute a task (placeholder implementation)."""
        self.status = AgentStatus.RUNNING
        self.last_active = datetime.now()
        
        # Simulate task execution
        result = f"[{self.name}] Executed task: {task}"
        print(result)
        
        self.status = AgentStatus.IDLE
        return result

class AgentMesh:
    """A mesh of collaborative agents."""
    
    def __init__(self):
        self.agents: Dict[str, CollaborativeAgent] = {}
        self.message_broker = MessageBroker()
        self.message_broker.set_agent_mesh(self)
    
    def create_agent(self, name: str, capabilities: List[str] = None) -> CollaborativeAgent:
        """Create a new agent and add it to the mesh."""
        agent_id = str(uuid.uuid4())
        agent = CollaborativeAgent(agent_id, name, capabilities or [])
        self.agents[agent_id] = agent
        self.message_broker.register_agent(agent)
        return agent
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the mesh."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.message_broker.unregister_agent(agent_id)
            return True
        return False
    
    def get_agent(self, agent_id: str) -> CollaborativeAgent:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents in the mesh."""
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "capabilities": agent.capabilities,
                "status": agent.status.value,
                "created_at": agent.created_at.isoformat(),
                "last_active": agent.last_active.isoformat()
            }
            for agent in self.agents.values()
        ]
    
    def send_message(self, sender_id: str, recipient_id: str, content: str, message_type: str = "default"):
        """Send a message between agents."""
        if sender_id in self.agents and recipient_id in self.agents:
            message = self.agents[sender_id].send_message(recipient_id, content, message_type)
            self.message_broker.route_message(message)
        else:
            raise ValueError("Sender or recipient agent not found")
    
    def broadcast_message(self, sender_id: str, content: str, message_type: str = "default"):
        """Broadcast a message to all agents."""
        if sender_id in self.agents:
            for agent_id in self.agents:
                if agent_id != sender_id:
                    message = self.agents[sender_id].send_message(agent_id, content, message_type)
                    self.message_broker.route_message(message)
        else:
            raise ValueError("Sender agent not found")
    
    def start_all_agents(self):
        """Start all agents in the mesh."""
        for agent in self.agents.values():
            agent.start()
    
    def stop_all_agents(self):
        """Stop all agents in the mesh."""
        for agent in self.agents.values():
            agent.stop()

class MessageBroker:
    """A message broker for routing messages between agents."""
    
    def __init__(self):
        self.agents: Dict[str, CollaborativeAgent] = {}
        self.agent_mesh = None
    
    def set_agent_mesh(self, mesh: AgentMesh):
        """Set the agent mesh."""
        self.agent_mesh = mesh
    
    def register_agent(self, agent: CollaborativeAgent):
        """Register an agent with the broker."""
        self.agents[agent.id] = agent
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the broker."""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def route_message(self, message: AgentMessage):
        """Route a message to its recipient."""
        if message.recipient in self.agents:
            self.agents[message.recipient].receive_message(message)
        else:
            print(f"Warning: Message recipient {message.recipient} not found")

# Example usage
if __name__ == "__main__":
    # Create an agent mesh
    mesh = AgentMesh()
    
    # Create agents
    agent1 = mesh.create_agent("Researcher", ["research", "data_analysis"])
    agent2 = mesh.create_agent("Writer", ["writing", "editing"])
    agent3 = mesh.create_agent("Reviewer", ["review", "feedback"])
    
    # Start all agents
    mesh.start_all_agents()
    
    # Send messages between agents
    mesh.send_message(agent1.id, agent2.id, "I've completed the research. Here are the findings...", "research_complete")
    mesh.send_message(agent2.id, agent3.id, "I've written the article based on the research. Please review.", "draft_complete")
    mesh.send_message(agent3.id, agent2.id, "Here's my feedback on the article. Please revise.", "review_complete")
    
    # Process messages
    for agent in mesh.agents.values():
        agent.process_messages()
    
    # Stop all agents
    mesh.stop_all_agents()