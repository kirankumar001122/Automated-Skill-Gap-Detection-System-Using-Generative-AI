import os
import tempfile
import shutil
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or tempfile.mkdtemp(prefix="coding_agent_")
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"FileManager initialized with base directory: {self.base_dir}")
    
    def create_file(self, filename: str, content: str, subdirectory: Optional[str] = None) -> str:
        """Create a file with the given content"""
        if subdirectory:
            dir_path = os.path.join(self.base_dir, subdirectory)
            os.makedirs(dir_path, exist_ok=True)
            file_path = os.path.join(dir_path, filename)
        else:
            file_path = os.path.join(self.base_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Created file: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to create file {file_path}: {e}")
            raise
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise
    
    def list_files(self, subdirectory: Optional[str] = None) -> List[str]:
        """List files in the base directory or subdirectory"""
        dir_path = os.path.join(self.base_dir, subdirectory) if subdirectory else self.base_dir
        
        try:
            files = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    files.append(item)
            return files
        except Exception as e:
            logger.error(f"Failed to list files in {dir_path}: {e}")
            return []
    
    def cleanup(self):
        """Clean up the base directory"""
        try:
            shutil.rmtree(self.base_dir)
            logger.info(f"Cleaned up directory: {self.base_dir}")
        except Exception as e:
            logger.error(f"Failed to cleanup directory {self.base_dir}: {e}")
    
    def get_file_path(self, filename: str, subdirectory: Optional[str] = None) -> str:
        """Get the full path for a file"""
        if subdirectory:
            return os.path.join(self.base_dir, subdirectory, filename)
        return os.path.join(self.base_dir, filename)
