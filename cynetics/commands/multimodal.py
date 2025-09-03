import click
import os
import json
from typing import Dict, Any

class MultimodalProcessor:
    """Processor for multimodal inputs."""
    
    SUPPORTED_TYPES = ["text", "image", "audio", "video"]
    
    def process_text(self, input_data: str) -> Dict[str, Any]:
        """Process text input."""
        return {
            "type": "text",
            "content": input_data,
            "length": len(input_data),
            "word_count": len(input_data.split()),
            "processed_at": __import__('datetime').datetime.now().isoformat()
        }
    
    def process_image(self, input_file: str) -> Dict[str, Any]:
        """Process image input."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Image file '{input_file}' not found")
        
        # Get file information
        stat = os.stat(input_file)
        
        return {
            "type": "image",
            "file_path": input_file,
            "file_size": stat.st_size,
            "extension": os.path.splitext(input_file)[1],
            "processed_at": __import__('datetime').datetime.now().isoformat()
        }
    
    def process_audio(self, input_file: str) -> Dict[str, Any]:
        """Process audio input."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Audio file '{input_file}' not found")
        
        # Get file information
        stat = os.stat(input_file)
        
        return {
            "type": "audio",
            "file_path": input_file,
            "file_size": stat.st_size,
            "extension": os.path.splitext(input_file)[1],
            "processed_at": __import__('datetime').datetime.now().isoformat()
        }
    
    def process_video(self, input_file: str) -> Dict[str, Any]:
        """Process video input."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Video file '{input_file}' not found")
        
        # Get file information
        stat = os.stat(input_file)
        
        return {
            "type": "video",
            "file_path": input_file,
            "file_size": stat.st_size,
            "extension": os.path.splitext(input_file)[1],
            "processed_at": __import__('datetime').datetime.now().isoformat()
        }

@click.command()
@click.option('--input', 'input_data', required=True, help='Input data (text or file path)')
@click.option('--type', 'input_type', required=True, type=click.Choice(['text', 'image', 'audio', 'video']), help='Type of input')
@click.option('--list-types', is_flag=True, help='List supported media types')
@click.option('--output', help='Output file for processed data (JSON format)')
def multimodal(input_data, input_type, list_types, output):
    """Handle images, audio, text, and video."""
    processor = MultimodalProcessor()
    
    if list_types:
        click.echo("Supported media types:")
        for media_type in processor.SUPPORTED_TYPES:
            click.echo(f"  {media_type}")
        return
    
    try:
        if input_type == "text":
            result = processor.process_text(input_data)
        elif input_type == "image":
            result = processor.process_image(input_data)
        elif input_type == "audio":
            result = processor.process_audio(input_data)
        elif input_type == "video":
            result = processor.process_video(input_data)
        else:
            click.echo(f"Unsupported input type: {input_type}")
            return
        
        # Display result
        click.echo(json.dumps(result, indent=2))
        
        # Save to output file if specified
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Result saved to: {output}")
            
    except Exception as e:
        click.echo(f"Error processing {input_type}: {e}")

if __name__ == "__main__":
    multimodal()