from .git_operations import GitOperations
import os
from dotenv import load_dotenv



def main():
    """
    Main function for the application
    """
    load_dotenv()
    git_ops = GitOperations(base_path="./repos", ssh_key_path="~/.ssh/id_rsa")
    github_url = "git@github.com:leeaaron629/sandbox-test-toast.git"
    repo_path = git_ops.clone_repository(github_url, branch="main")
    print(f"Current branch: {git_ops.get_current_branch(repo_path)}")
    git_ops.pull_repository(repo_path)


if __name__ == "__main__":

    load_dotenv()

    app_name = os.getenv("APP_NAME")
    print(f"Starting {app_name}")
    
    
