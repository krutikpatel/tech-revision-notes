import requests
import csv
from urllib.parse import urlparse

def get_files_from_subdir(repo_url, subdir_path, output_csv):
    """
    Get files from a specific subdirectory and all its subdirectories in a public GitHub repository
    and save their names and URLs to a CSV file.
    
    Args:
        repo_url (str): URL of the GitHub repository (e.g., 'https://github.com/username/repo')
        subdir_path (str): Path to the subdirectory within the repository
        output_csv (str): Path to the output CSV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Parse the GitHub URL to get the username and repository name
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        print(f"Invalid GitHub URL format: {repo_url}")
        return False
    
    username = path_parts[0]
    repo_name = path_parts[1]
    
    # Files to be written to CSV
    all_files = []
    
    # Function to recursively get files from directory and subdirectories
    def get_contents_recursive(dir_path):
        # Base URL for GitHub API with the specified directory
        api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{dir_path}"
        
        try:
            # Get the contents of the directory
            response = requests.get(api_url)
            response.raise_for_status()
            
            # Parse the response to get the list of files and directories
            contents = response.json()
            
            # Process contents
            for item in contents:
                if item['type'] == 'file':
                    # Create articleName in directory+filename format
                    articleName = f"{dir_path}/{item['name']}"
                    articleUrl = item['html_url']
                    all_files.append({
                        'articleName': articleName,
                        'articleUrl': articleUrl
                    })
                elif item['type'] == 'dir':
                    # Recursively process subdirectory
                    subdirectory_path = f"{dir_path}/{item['name']}" if dir_path else item['name']
                    get_contents_recursive(subdirectory_path)
            
            return True
        
        except Exception as e:
            print(f"Error fetching files from {dir_path}: {e}")
            return False
    
    # Start recursive process from the initial subdirectory
    success = get_contents_recursive(subdir_path)
    
    if not all_files:
        print(f"No files found in the subdirectory tree starting from: {subdir_path}")
        return False
    
    # Write data to CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['articleName', 'articleUrl']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for file in all_files:
            writer.writerow(file)
    
    print(f"Successfully wrote {len(all_files)} files to {output_csv}")
    return True

# Example usage
if __name__ == "__main__":
    # Base repository URL
    repo_url = "https://github.com/krutikpatel/tech-revision-notes/tree/main"
    
    # Subdirectory path within the repository
    subdir_path = "SpringFramework"  # Example: the test directory in Python's standard library
    
    # Output CSV file path
    output_csv = "github_files.csv"
    
    success = get_files_from_subdir(repo_url, subdir_path, output_csv)
    
    if success:
        print(f"CSV file created successfully: {output_csv}")
    else:
        print(f"Failed to create CSV file from subdirectory tree: {subdir_path}")