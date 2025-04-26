import requests
import random
from urllib.parse import urlparse

def get_random_file_link(repo_url):
    """
    Get a link to a random file from a public GitHub repository.
    
    Args:
        repo_url (str): URL of the GitHub repository (e.g., 'https://github.com/username/repo')
    
    Returns:
        str: URL to a random file in the repository or None if failed
    """
    # Parse the GitHub URL to get the username and repository name
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        print(f"Invalid GitHub URL format: {repo_url}")
        return None
    
    username = path_parts[0]
    repo_name = path_parts[1]
    
    # Base URL for GitHub API
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
    
    try:
        # Get the contents of the repository (files and directories)
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Parse the response to get the list of files and directories
        contents = response.json()
        
        # Keep track of all files found
        all_files = []
        
        # Process initial contents
        directories = []
        for item in contents:
            if item['type'] == 'file':
                all_files.append(item)
            elif item['type'] == 'dir':
                directories.append(item['path'])
        
        # Process directories up to a certain depth to avoid too many API calls
        max_depth = 2
        current_depth = 0
        
        while directories and current_depth < max_depth:
            new_directories = []
            for directory in directories:
                dir_url = f"{api_url}/{directory}"
                try:
                    dir_response = requests.get(dir_url)
                    dir_response.raise_for_status()
                    dir_contents = dir_response.json()
                    
                    for item in dir_contents:
                        if item['type'] == 'file':
                            all_files.append(item)
                        elif item['type'] == 'dir':
                            new_directories.append(item['path'])
                except Exception as e:
                    print(f"Error accessing directory {directory}: {e}")
            
            directories = new_directories
            current_depth += 1
        
        if not all_files:
            print("No files found in the repository.")
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
    # Replace this with the GitHub repository URL you want to fetch from
    repo_url = "https://github.com/krutikpatel/tech-revision-notes/tree/main"
    
    file_link = get_random_file_link(repo_url)
    
    if file_link:
        print(f"Random file link: {file_link}")
    else:
        print("Failed to fetch a random file link.")