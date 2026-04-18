import base64
import requests
import re

TARGET_FILES = [
    "README.md", "requirements.txt", "Dockerfile", 
    "docker-compose.yml", "package.json", "main.py", "app.py"
]

def parse_github_url(url: str):
    """GitHub URL'sini parçalayıp owner ve repo isimlerini çıkarır."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2).replace(".git", "")
    return None, None

def fetch_file_content(owner: str, repo: str, file_path: str):
    """GitHub API'den tek bir dosyanın içeriğini çeker ve metne çevirir."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content_b64 = response.json().get("content", "")
        if content_b64:
            return base64.b64decode(content_b64).decode("utf-8")
    return None

def get_target_files(owner: str, repo: str):
    """Sadece hedef dosyaları arar ve bulduklarını sözlük (dict) olarak döner."""
    fetched_data = {}
    for file_name in TARGET_FILES:
        content = fetch_file_content(owner, repo, file_name)
        if content:
            fetched_data[file_name] = content
    return fetched_data