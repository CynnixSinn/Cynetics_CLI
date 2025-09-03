from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from enum import Enum

class MediaType(Enum):
    """Enumeration of media types."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

class MediaProcessor(ABC):
    """Abstract base class for media processors."""
    
    def __init__(self, media_type: MediaType):
        self.media_type = media_type
    
    @abstractmethod
    def process_input(self, data: Any) -> Dict[str, Any]:
        """Process input media data.
        
        Args:
            data: Input media data
            
        Returns:
            Processed data dictionary
        """
        pass
    
    @abstractmethod
    def process_output(self, data: Dict[str, Any]) -> Any:
        """Process output media data.
        
        Args:
            data: Output data dictionary
            
        Returns:
            Processed media data
        """
        pass

class TextProcessor(MediaProcessor):
    """Processor for text media."""
    
    def __init__(self):
        super().__init__(MediaType.TEXT)
    
    def process_input(self, data: str) -> Dict[str, Any]:
        """Process text input."""
        return {
            "type": "text",
            "content": data,
            "length": len(data),
            "word_count": len(data.split()),
            "char_count": len(data)
        }
    
    def process_output(self, data: Dict[str, Any]) -> str:
        """Process text output."""
        return data.get("content", "")

class ImageProcessor(MediaProcessor):
    """Processor for image media."""
    
    def __init__(self):
        super().__init__(MediaType.IMAGE)
    
    def process_input(self, data: Union[str, bytes]) -> Dict[str, Any]:
        """Process image input.
        
        Args:
            data: Image file path or bytes
            
        Returns:
            Processed image data
        """
        if isinstance(data, str):
            # Assume it's a file path
            return {
                "type": "image",
                "source": "file",
                "path": data,
                "format": data.split(".")[-1].lower() if "." in data else "unknown"
            }
        elif isinstance(data, bytes):
            # Raw image bytes
            return {
                "type": "image",
                "source": "bytes",
                "size": len(data)
            }
        else:
            raise ValueError("Image data must be a file path or bytes")
    
    def process_output(self, data: Dict[str, Any]) -> Union[str, bytes]:
        """Process image output."""
        if data.get("source") == "file":
            return data.get("path", "")
        elif data.get("source") == "bytes":
            # In a real implementation, you would return the actual bytes
            return b""  # Placeholder
        else:
            return ""

class AudioProcessor(MediaProcessor):
    """Processor for audio media."""
    
    def __init__(self):
        super().__init__(MediaType.AUDIO)
    
    def process_input(self, data: Union[str, bytes]) -> Dict[str, Any]:
        """Process audio input."""
        if isinstance(data, str):
            # Assume it's a file path
            return {
                "type": "audio",
                "source": "file",
                "path": data,
                "format": data.split(".")[-1].lower() if "." in data else "unknown"
            }
        elif isinstance(data, bytes):
            # Raw audio bytes
            return {
                "type": "audio",
                "source": "bytes",
                "size": len(data)
            }
        else:
            raise ValueError("Audio data must be a file path or bytes")
    
    def process_output(self, data: Dict[str, Any]) -> Union[str, bytes]:
        """Process audio output."""
        if data.get("source") == "file":
            return data.get("path", "")
        elif data.get("source") == "bytes":
            # In a real implementation, you would return the actual bytes
            return b""  # Placeholder
        else:
            return ""

class VideoProcessor(MediaProcessor):
    """Processor for video media."""
    
    def __init__(self):
        super().__init__(MediaType.VIDEO)
    
    def process_input(self, data: Union[str, bytes]) -> Dict[str, Any]:
        """Process video input."""
        if isinstance(data, str):
            # Assume it's a file path
            return {
                "type": "video",
                "source": "file",
                "path": data,
                "format": data.split(".")[-1].lower() if "." in data else "unknown"
            }
        elif isinstance(data, bytes):
            # Raw video bytes
            return {
                "type": "video",
                "source": "bytes",
                "size": len(data)
            }
        else:
            raise ValueError("Video data must be a file path or bytes")
    
    def process_output(self, data: Dict[str, Any]) -> Union[str, bytes]:
        """Process video output."""
        if data.get("source") == "file":
            return data.get("path", "")
        elif data.get("source") == "bytes":
            # In a real implementation, you would return the actual bytes
            return b""  # Placeholder
        else:
            return ""

class MultiModalCLI:
    """A CLI system that can handle multiple media types."""
    
    def __init__(self):
        self.processors = {
            MediaType.TEXT: TextProcessor(),
            MediaType.IMAGE: ImageProcessor(),
            MediaType.AUDIO: AudioProcessor(),
            MediaType.VIDEO: VideoProcessor()
        }
    
    def process_input(self, media_type: MediaType, data: Any) -> Dict[str, Any]:
        """Process input data of a specific media type.
        
        Args:
            media_type: Type of media
            data: Input data
            
        Returns:
            Processed data dictionary
        """
        if media_type not in self.processors:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        return self.processors[media_type].process_input(data)
    
    def process_output(self, media_type: MediaType, data: Dict[str, Any]) -> Any:
        """Process output data of a specific media type.
        
        Args:
            media_type: Type of media
            data: Output data dictionary
            
        Returns:
            Processed media data
        """
        if media_type not in self.processors:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        return self.processors[media_type].process_output(data)
    
    def list_supported_media_types(self) -> List[MediaType]:
        """List all supported media types.
        
        Returns:
            List of supported media types
        """
        return list(self.processors.keys())