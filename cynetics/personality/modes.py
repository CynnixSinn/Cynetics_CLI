from cynetics.personality.adaptive import AdaptivePersonality, AgentMode

# Global personality instance
_personality = AdaptivePersonality()

def list_modes():
    """List all available personality modes."""
    return _personality.list_modes()

def set_mode(mode_name):
    """Set the personality mode by name."""
    # Convert string to enum
    try:
        mode = AgentMode(mode_name.lower())
        _personality.set_mode(mode)
    except ValueError:
        raise ValueError(f"Unknown mode: {mode_name}. Available modes: {list(AgentMode.__members__.keys())}")

def get_current_mode():
    """Get the current personality mode."""
    return _personality.get_mode().value

def get_mode_config(mode_name=None):
    """Get configuration for a mode."""
    if mode_name:
        try:
            mode = AgentMode(mode_name.lower())
            return _personality.get_mode_config(mode)
        except ValueError:
            raise ValueError(f"Unknown mode: {mode_name}")
    else:
        return _personality.get_mode_config()