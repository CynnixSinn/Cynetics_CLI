import click
import random
from typing import List, Dict, Any

class CLITutorialSystem:
    """An AI-driven CLI tutorial system."""
    
    def __init__(self):
        self.tutorials = self._load_tutorials()
        self.user_progress = {}
    
    def _load_tutorials(self) -> Dict[str, Dict[str, Any]]:
        """Load built-in tutorials."""
        return {
            "basic_navigation": {
                "title": "Basic Navigation",
                "description": "Learn basic file and directory navigation commands",
                "commands": [
                    {
                        "name": "ls",
                        "description": "List directory contents",
                        "examples": [
                            "ls",
                            "ls -l",
                            "ls -la"
                        ],
                        "explanation": "The 'ls' command lists files and directories in the current directory. Options like -l show detailed information, and -a shows hidden files."
                    },
                    {
                        "name": "cd",
                        "description": "Change directory",
                        "examples": [
                            "cd /home",
                            "cd ..",
                            "cd ~"
                        ],
                        "explanation": "The 'cd' command changes your current directory. Use '..' to go up one level, '~' for your home directory, or a full path to navigate to a specific location."
                    },
                    {
                        "name": "pwd",
                        "description": "Print working directory",
                        "examples": [
                            "pwd"
                        ],
                        "explanation": "The 'pwd' command shows your current directory path."
                    }
                ]
            },
            "file_operations": {
                "title": "File Operations",
                "description": "Learn commands for creating, copying, moving, and deleting files",
                "commands": [
                    {
                        "name": "touch",
                        "description": "Create an empty file or update timestamp",
                        "examples": [
                            "touch newfile.txt",
                            "touch file1.txt file2.txt"
                        ],
                        "explanation": "The 'touch' command creates empty files or updates the timestamp of existing files."
                    },
                    {
                        "name": "cp",
                        "description": "Copy files or directories",
                        "examples": [
                            "cp file1.txt file2.txt",
                            "cp -r dir1 dir2"
                        ],
                        "explanation": "The 'cp' command copies files. Use -r to copy directories recursively."
                    },
                    {
                        "name": "mv",
                        "description": "Move or rename files or directories",
                        "examples": [
                            "mv oldname.txt newname.txt",
                            "mv file.txt /path/to/destination/"
                        ],
                        "explanation": "The 'mv' command moves files or renames them. It can also move directories."
                    },
                    {
                        "name": "rm",
                        "description": "Remove files or directories",
                        "examples": [
                            "rm file.txt",
                            "rm -r directory/",
                            "rm -f file.txt"
                        ],
                        "explanation": "The 'rm' command deletes files. Use -r to remove directories and -f to force removal without confirmation."
                    }
                ]
            },
            "text_processing": {
                "title": "Text Processing",
                "description": "Learn commands for viewing and processing text files",
                "commands": [
                    {
                        "name": "cat",
                        "description": "Concatenate and display file contents",
                        "examples": [
                            "cat file.txt",
                            "cat file1.txt file2.txt"
                        ],
                        "explanation": "The 'cat' command displays the contents of files or concatenates multiple files."
                    },
                    {
                        "name": "grep",
                        "description": "Search for patterns in files",
                        "examples": [
                            "grep 'pattern' file.txt",
                            "grep -r 'pattern' directory/",
                            "grep -i 'Pattern' file.txt"
                        ],
                        "explanation": "The 'grep' command searches for text patterns in files. Use -r for recursive search and -i for case-insensitive search."
                    },
                    {
                        "name": "wc",
                        "description": "Count lines, words, and characters",
                        "examples": [
                            "wc file.txt",
                            "wc -l file.txt",
                            "wc -w file.txt"
                        ],
                        "explanation": "The 'wc' command counts lines, words, and characters in files. Use -l for lines, -w for words, or -c for characters."
                    }
                ]
            }
        }
    
    def list_tutorials(self) -> List[Dict[str, str]]:
        """List all available tutorials.
        
        Returns:
            List of tutorial information
        """
        return [
            {
                "id": tutorial_id,
                "title": tutorial["title"],
                "description": tutorial["description"],
                "command_count": len(tutorial["commands"])
            }
            for tutorial_id, tutorial in self.tutorials.items()
        ]
    
    def get_tutorial(self, tutorial_id: str) -> Dict[str, Any]:
        """Get a tutorial by ID.
        
        Args:
            tutorial_id: ID of the tutorial
            
        Returns:
            Tutorial data
        """
        return self.tutorials.get(tutorial_id, {})
    
    def start_interactive_tutorial(self, tutorial_id: str):
        """Start an interactive tutorial session.
        
        Args:
            tutorial_id: ID of the tutorial to start
        """
        tutorial = self.get_tutorial(tutorial_id)
        if not tutorial:
            click.echo(f"Tutorial '{tutorial_id}' not found.")
            return
        
        click.echo(f"\n=== {tutorial['title']} ===")
        click.echo(f"{tutorial['description']}\n")
        
        for i, command in enumerate(tutorial["commands"], 1):
            click.echo(f"\n--- Command {i}: {command['name']} ---")
            click.echo(f"Description: {command['description']}")
            click.echo(f"Explanation: {command['explanation']}")
            click.echo("Examples:")
            for example in command["examples"]:
                click.echo(f"  $ {example}")
            
            # Interactive practice
            click.echo("\nTry it yourself! (Press Enter to continue)")
            input()
        
        click.echo(f"\n🎉 Congratulations! You've completed the '{tutorial['title']}' tutorial.")
    
    def recommend_next_tutorial(self, user_id: str = "default") -> str:
        """Recommend the next tutorial based on user progress.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Recommended tutorial ID
        """
        completed = self.user_progress.get(user_id, [])
        all_tutorials = list(self.tutorials.keys())
        
        # Find the first tutorial that hasn't been completed
        for tutorial_id in all_tutorials:
            if tutorial_id not in completed:
                return tutorial_id
        
        # If all tutorials are completed, recommend a random one
        return random.choice(all_tutorials) if all_tutorials else ""
    
    def mark_tutorial_completed(self, tutorial_id: str, user_id: str = "default"):
        """Mark a tutorial as completed for a user.
        
        Args:
            tutorial_id: ID of the tutorial
            user_id: ID of the user
        """
        if user_id not in self.user_progress:
            self.user_progress[user_id] = []
        
        if tutorial_id not in self.user_progress[user_id]:
            self.user_progress[user_id].append(tutorial_id)