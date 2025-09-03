from enum import Enum
from typing import Dict, Any

class AgentMode(Enum):
    """Enumeration of agent modes."""
    PRECISION = "precision"      # Tool-like precision mode
    CREATIVE = "creative"        # Creative exploration mode
    AUTONOMOUS = "autonomous"    # Autonomous long-running agent mode

class AdaptivePersonality:
    """A system to manage agent personalities and modes."""
    
    def __init__(self):
        self.current_mode = AgentMode.PRECISION
        self.mode_configs = {
            AgentMode.PRECISION: {
                "temperature": 0.1,
                "max_tokens": 500,
                "top_p": 0.1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "description": "Tool-like precision mode for accurate, deterministic responses"
            },
            AgentMode.CREATIVE: {
                "temperature": 0.9,
                "max_tokens": 1000,
                "top_p": 0.9,
                "frequency_penalty": 0.5,
                "presence_penalty": 0.5,
                "description": "Creative exploration mode for brainstorming and idea generation"
            },
            AgentMode.AUTONOMOUS: {
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 0.8,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3,
                "description": "Autonomous agent mode for long-running, independent tasks"
            }
        }
    
    def set_mode(self, mode: AgentMode):
        """Set the current agent mode."""
        self.current_mode = mode
    
    def get_mode(self) -> AgentMode:
        """Get the current agent mode."""
        return self.current_mode
    
    def get_mode_config(self, mode: AgentMode = None) -> Dict[str, Any]:
        """Get the configuration for a specific mode or the current mode."""
        if mode is None:
            mode = self.current_mode
        return self.mode_configs.get(mode, {})
    
    def get_mode_description(self, mode: AgentMode = None) -> str:
        """Get the description for a specific mode or the current mode."""
        config = self.get_mode_config(mode)
        return config.get("description", "Unknown mode")
    
    def list_modes(self) -> Dict[str, str]:
        """List all available modes with their descriptions."""
        return {mode.value: self.get_mode_description(mode) for mode in AgentMode}
    
    def adapt_prompt(self, prompt: str, mode: AgentMode = None) -> str:
        """Adapt a prompt based on the specified mode or current mode."""
        if mode is None:
            mode = self.current_mode
            
        if mode == AgentMode.PRECISION:
            return f"[PRECISION] {prompt} (Provide a concise, accurate response with minimal creativity)"
        elif mode == AgentMode.CREATIVE:
            return f"[CREATIVE] {prompt} (Explore multiple possibilities and think outside the box)"
        elif mode == AgentMode.AUTONOMOUS:
            return f"[AUTONOMOUS] {prompt} (Take initiative, plan multiple steps, and work independently)"
        else:
            return prompt  # Fallback to original prompt
    
    def adapt_response(self, response: str, mode: AgentMode = None) -> Dict[str, Any]:
        """Adapt a response based on the specified mode or current mode."""
        if mode is None:
            mode = self.current_mode
            
        adaptation = {
            "response": response,
            "mode": mode.value,
            "adaptation_applied": True
        }
        
        if mode == AgentMode.PRECISION:
            adaptation["confidence"] = "high"
            adaptation["response_type"] = "deterministic"
        elif mode == AgentMode.CREATIVE:
            adaptation["confidence"] = "variable"
            adaptation["response_type"] = "exploratory"
        elif mode == AgentMode.AUTONOMOUS:
            adaptation["confidence"] = "moderate"
            adaptation["response_type"] = "independent"
        else:
            adaptation["confidence"] = "unknown"
            adaptation["response_type"] = "unspecified"
            adaptation["adaptation_applied"] = False
            
        return adaptation