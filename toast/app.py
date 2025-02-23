import subprocess
from .git_operations import GitOperations
import os
from dotenv import load_dotenv
import shutil


def main():
    """
    Main function for the application
    """
    load_dotenv()
    git_ops = GitOperations(base_path="./repos", ssh_kßey_path="~/.ssh/id_rsa")
    github_url = "git@github.com:leeaaron629/sandbox-test-toast.git"
    repo_path = git_ops.clone_repository(github_url, branch="main")
    print(f"Current branch: {git_ops.get_current_branch(repo_path)}")
    git_ops.pull_repository(repo_path)


if __name__ == "__main__":

    load_dotenv()

    app_name = os.getenv("APP_NAME")
    print(f"Starting {app_name}")

    base_path = os.getenv("BASE_PATH", "./repos")
    os.makedirs(base_path, exist_ok=True)
    
    
    github_url = "git@github.com:leeaaron629/sandbox-test-toast.git"
    repo_name = "sandbox-test-toast"
    print(f"Cloning repository: {github_url}")
    command = f"git clone {github_url} {repo_name}".split(" ")
    process = subprocess.Popen(command, cwd=base_path)

    stdout, stderr = process.communicate()

    print(f"stdout: {stdout}")
    print(f"stderr: {stderr}")

    if process.returncode != 0:
        print(f"Error cloning repository: {stderr}")

    print(f"Cloned repository to {base_path}")

    print(f"Cleaning up repo: {base_path}/{repo_name}")
    if os.path.exists(f"{base_path}/{repo_name}"):
        shutil.rmtree(f"{base_path}/{repo_name}")
    print(f"Cleaned up repository: {base_path}/{repo_name}")
    
