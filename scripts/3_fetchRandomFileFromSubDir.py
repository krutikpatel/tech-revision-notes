import requests
import random
from urllib.parse import urlparse

def get_random_file_link_from_subdir(repo_url, subdir_path):
    """
    Get a link to a random file from a specific subdirectory in a public GitHub repository.
    
    Args:
        repo_url (str): URL of the GitHub repository (e.g., 'https://github.com/username/repo')
        subdir_path (str): Path to the subdirectory within the repository
    
    Returns:
        str: URL to a random file in the subdirectory or None if failed
    """
    # Parse the GitHub URL to get the username and repository name
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        print(f"Invalid GitHub URL format: {repo_url}")
        return None
    
    username = path_parts[0]
    repo_name = path_parts[1]
    
    # Base URL for GitHub API with the specified subdirectory
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{subdir_path}"
    
    try:
        # Get the contents of the subdirectory
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Parse the response to get the list of files and directories
        contents = response.json()
        
        # Keep track of all files found
        all_files = []
        
        # Process contents
        for item in contents:
            if item['type'] == 'file':
                all_files.append(item)
        
        if not all_files:
            print(f"No files found in the subdirectory: {subdir_path}")
            return None
        
        # Select a random file
        random_file = random.choice(all_files)
        file_name = random_file['name']
        
        # Return the HTML URL to view the file on GitHub
        html_url = random_file['html_url']
        print(f"Random file selected: {file_name}")
        print(f"File URL: {html_url}")
        
        return html_url
    
    except Exception as e:
        print(f"Error fetching random file link: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Base repository URL
    repo_url = "https://github.com/krutikpatel/tech-revision-notes/tree/main"
    
    # Subdirectory path within the repository
    subdir_path = "SpringFramework"  # Example: the test directory in Python's standard library
    
    file_link = get_random_file_link_from_subdir(repo_url, subdir_path)
    
    if file_link:
        print(f"Random file link: {file_link}")
    else:
        print(f"Failed to fetch a random file link from subdirectory: {subdir_path}")