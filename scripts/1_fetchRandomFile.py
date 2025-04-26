import requests
import random
import os
import base64
from urllib.parse import urlparse

def fetch_random_file(repo_url):
    """
    Fetch a random file from a public GitHub repository.
    
    Args:
        repo_url (str): URL of the GitHub repository (e.g., 'https://github.com/username/repo')
    
    Returns:
        tuple: (file_name, file_content) or (None, None) if failed
    """
    # Parse the GitHub URL to get the username and repository name
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        print(f"Invalid GitHub URL format: {repo_url}")
        return None, None
    
    username = path_parts[0]
    repo_name = path_parts[1]
    
    # Base URL for GitHub API
    api_url = f"https://github.com/krutikpatel/tech-revision-notes/tree/main/SpringFramework"
    
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
            return None, None
        
        # Select a random file
        random_file = random.choice(all_files)
        file_name = random_file['name']
        file_url = random_file['download_url']
        
        # Download the file content
        file_response = requests.get(file_url)
        file_response.raise_for_status()
        file_content = file_response.text
        
        print(f"Successfully downloaded: {file_name}")
        return file_name, file_content
    
    except Exception as e:
        print(f"Error fetching random file: {e}")
        return None, None

def save_file(file_name, file_content, output_dir='.'):
    """
    Save the file content to disk.
    
    Args:
        file_name (str): Name of the file
        file_content (str): Content of the file
        output_dir (str): Directory to save the file
    
    Returns:
        str: Path to the saved file
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    return file_path

# Example usage
if __name__ == "__main__":
    # Replace this with the GitHub repository URL you want to fetch from
    repo_url = "https://github.com/krutikpatel/tech-revision-notes/tree/main/SpringFramework"
    
    file_name, file_content = fetch_random_file(repo_url)
    
    if file_name and file_content:
        file_path = save_file(file_name, file_content, "downloaded_files")
        print(f"File saved to: {file_path}")
    else:
        print("Failed to fetch a random file.")