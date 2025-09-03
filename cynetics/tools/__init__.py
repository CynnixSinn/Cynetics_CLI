from cynetics.tools.base import BaseTool
from cynetics.tools.file_manager import FileManagerTool
from cynetics.tools.web_search import WebSearchTool
from cynetics.tools.advanced_web_search import AdvancedWebSearchTool
from cynetics.tools.code_generation import CodeGenerationTool
from cynetics.plugins.loader import load_plugins

# Registry of available tools (built-in + plugins)
TOOL_REGISTRY = {
    "file_manager": FileManagerTool,
    "web_search": WebSearchTool,
    "advanced_web_search": AdvancedWebSearchTool,
    "code_generation": CodeGenerationTool
}

# Try to import tools with external dependencies
try:
    from cynetics.tools.data_analysis import DataAnalysisTool
    TOOL_REGISTRY["data_analysis"] = DataAnalysisTool
except ImportError:
    # pandas not available, skip data_analysis tool
    pass

try:
    from cynetics.tools.system_monitor import SystemMonitorTool
    TOOL_REGISTRY["system_monitor"] = SystemMonitorTool
except ImportError:
    # psutil not available, skip system_monitor tool
    pass

# Load plugins dynamically
TOOL_REGISTRY.update(load_plugins())

def load_tool(name: str) -> BaseTool:
    """Load a tool by name from the registry."""
    if name in TOOL_REGISTRY:
        return TOOL_REGISTRY[name]()
    else:
        raise ValueError(f"Tool '{name}' not found in registry.")