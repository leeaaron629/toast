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

    def _run_command(self, command: List[str], cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> Tuple[str, str]:
        """
        Execute a git command and return its output
        
        Args:
            command (List[str]): Command to execute
            cwd (str, optional): Working directory
            env (Dict[str, str], optional): Environment variables
            
        Returns:
            Tuple[str, str]: stdout and stderr
        """
        try:
            # Prepare environment variables
            process_env = os.environ.copy()
            if env:
                process_env.update(env)

            # If SSH key is specified, use GIT_SSH_COMMAND
            if self.ssh_key_path:
                process_env['GIT_SSH_COMMAND'] = f'ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no'

            process = subprocess.Popen(
                command,
                cwd=cwd,
                env=process_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Command failed with error: {stderr}")
                
            return stdout, stderr
            
        except subprocess.SubprocessError as e:
            raise Exception(f"Failed to execute command: {e}")

    def parse_git_url(self, url: str, token: Optional[str] = None) -> Tuple[str, str]:
        """
        Parse and normalize Git URL, optionally incorporating API token
        
        Args:
            url (str): Git repository URL
            token (str, optional): API token for authentication
            
        Returns:
            Tuple[str, str]: Repository name and normalized URL
        """
        # Handle SSH URLs
        if "@" in url and ":" in url and not url.startswith(('http://', 'https://')):
            ssh_pattern = r"git@([^:]+):([^/]+)/(.+)\.git"
            match = re.match(ssh_pattern, url)
            if match:
                host, owner, repo = match.groups()
                repo_name = repo.strip(".git")
                return repo_name, url

        # Handle HTTPS URLs
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) < 2:
            raise ValueError(f"Invalid Git URL format: {url}")
            
        repo_name = path_parts[-1].replace(".git", "")
        
        # If token is provided, incorporate it into HTTPS URL
        if token and parsed.scheme in ('http', 'https'):
            netloc = parsed.netloc
            if '@' not in netloc:
                netloc = f'oauth2:{token}@{netloc}'
            url = urlunparse((parsed.scheme, netloc, parsed.path, 
                            parsed.params, parsed.query, parsed.fragment))
            
        return repo_name, url

    def clone_repository(self, url: str, branch: Optional[str] = None, 
                        token: Optional[str] = None) -> str:
        """
        Clone a Git repository using either SSH or HTTPS with token
        
        Args:
            url (str): Repository URL
            branch (str, optional): Specific branch to clone
            token (str, optional): API token for authentication
            
        Returns:
            str: Path to the cloned repository
        """
        repo_name, normalized_url = self.parse_git_url(url, token)
        repo_path = os.path.join(self.base_path, repo_name)

        if os.path.exists(repo_path):
            raise ValueError(f"Repository directory already exists: {repo_path}")

        # Prepare clone command
        command = ['git', 'clone']
        if branch:
            command.extend(['-b', branch])
        command.extend(['--single-branch', normalized_url, repo_path])

        stdout, _ = self._run_command(command)
        print(f"Successfully cloned repository to {repo_path}")
        return repo_path

    def pull_repository(self, repo_path: str, branch: Optional[str] = None) -> None:
        """
        Pull latest changes from a repository
        
        Args:
            repo_path (str): Path to the local repository
            branch (str, optional): Branch to pull from
        """
        if branch:
            self._run_command(['git', 'checkout', branch], cwd=repo_path)
        
        stdout, _ = self._run_command(['git', 'pull'], cwd=repo_path)
        print(f"Successfully pulled latest changes for {repo_path}")

    def get_current_branch(self, repo_path: str) -> str:
        """
        Get the current branch name
        
        Args:
            repo_path (str): Path to the local repository
            
        Returns:
            str: Current branch name
        """
        stdout, _ = self._run_command(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=repo_path
        )
        return stdout.strip()

    def set_remote_url(self, repo_path: str, url: str, token: Optional[str] = None) -> None:
        """
        Update the remote URL, optionally incorporating an API token
        
        Args:
            repo_path (str): Path to the local repository
            url (str): New remote URL
            token (str, optional): API token for authentication
        """
        _, normalized_url = self.parse_git_url(url, token)
        self._run_command(['git', 'remote', 'set-url', 'origin', normalized_url], cwd=repo_path)
        print(f"Successfully updated remote URL for {repo_path}")

# Example usage
if __name__ == "__main__":
    # Initialize with SSH key
    git_ops = GitOperations(
        "./repositories",
        ssh_key_path="~/.ssh/id_rsa"
    )

    # Example URLs
    https_url = "https://github.com/username/repo.git"
    ssh_url = "git@github.com:username/repo.git"
    
    # Example with HTTPS + token
    try:
        token = "your_api_token"
        repo_path = git_ops.clone_repository(https_url, token=token, branch="main")
        print(f"Current branch: {git_ops.get_current_branch(repo_path)}")
        git_ops.pull_repository(repo_path)
    except Exception as e:
        print(f"HTTPS Error: {e}")

    # Example with SSH
    try:
        repo_path = git_ops.clone_repository(ssh_url, branch="main")
        print(f"Current branch: {git_ops.get_current_branch(repo_path)}")
        git_ops.pull_repository(repo_path)
    except Exception as e:
        print(f"SSH Error: {e}")
