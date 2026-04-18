from pydantic import BaseModel
from typing import List, Dict

class RepoRequest(BaseModel):
    repo_url: str

class RepoResponse(BaseModel):
    status: str
    owner: str
    repo: str
    files_analyzed: List[str]
    ai_analysis: Dict