import os
import re
import subprocess
from typing import Optional, Tuple, Dict, List
from urllib.parse import urlparse, urlunparse

class GitOperations:
    def __init__(self, base_path: str = ".", ssh_key_path: Optional[str] = None):
        """
        Initialize GitOperations with a base path and optional SSH key path
        
        Args:
            base_path (str): Base directory where repositories will be cloned
            ssh_key_path (str, optional): Path to SSH private key
        """
        self.base_path = os.path.abspath(base_path)
        self.ssh_key_path = ssh_key_path
        os.makedirs(self.base_path, exist_ok=True)
