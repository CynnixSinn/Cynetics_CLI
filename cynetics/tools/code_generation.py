import requests
from typing import Dict, Any
from cynetics.tools.base import BaseTool
from cynetics.models.openai import OpenAIProvider

class CodeGenerationTool(BaseTool):
    """A tool for generating code based on descriptions."""
    
    def __init__(self):
        super().__init__(
            name="code_generation",
            description="Generate code snippets or files based on natural language descriptions."
        )
        # This would typically be configured with an API key
        self.model_provider = None
    
    def configure_model(self, api_key: str, model: str = "gpt-4"):
        """Configure the model provider for code generation."""
        self.model_provider = OpenAIProvider()
        self.model_provider.configure({
            "api_key": api_key,
            "model": model
        })
    
    def run(self, description: str, language: str = "python", file_path: str = None) -> Dict[str, Any]:
        """Generate code based on a description.
        
        Args:
            description: Description of what the code should do.
            language: Programming language for the generated code.
            file_path: Optional file path to save the generated code.
            
        Returns:
            A dictionary with the generated code and metadata.
        """
        if not self.model_provider:
            return {
                "status": "error",
                "message": "Model provider not configured. Call configure_model() first."
            }
        
        try:
            # Create a prompt for code generation
            prompt = f"""
Generate {language} code that {description}.
Requirements:
1. Follow best practices for {language}
2. Include comments explaining complex logic
3. Handle potential errors appropriately
4. Use descriptive variable and function names
5. Include a simple example of how to use the code

Return ONLY the code without any markdown formatting or extra text.
"""
            
            generated_code = self.model_provider.generate(prompt, max_tokens=1000)
            
            result = {
                "status": "success",
                "description": description,
                "language": language,
                "generated_code": generated_code.strip()
            }
            
            # Save to file if requested
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        f.write(generated_code.strip())
                    result["file_path"] = file_path
                    result["message"] = f"Code generated and saved to {file_path}"
                except Exception as e:
                    result["save_error"] = str(e)
                    result["message"] = "Code generated but failed to save to file"
            else:
                result["message"] = "Code generated successfully"
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }