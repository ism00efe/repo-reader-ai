from fastapi import FastAPI, HTTPException
from schemas import RepoRequest, RepoResponse
from github_utils import parse_github_url, get_target_files
from ai_agent import analyze_code_with_gemini

app = FastAPI(title="RepoReader AI - DevSecOps Agent")

@app.post("/api/analyze", response_model=RepoResponse)
async def analyze_repo(request: RepoRequest):
    owner, repo = parse_github_url(request.repo_url)
    if not owner or not repo:
        raise HTTPException(status_code=400, detail="Geçersiz GitHub URL'si.")

    fetched_files = get_target_files(owner, repo)
    if not fetched_files:
        raise HTTPException(status_code=404, detail="Kilit dosyalar bulunamadı veya repo gizli.")

    # Execute Gemini Analysis
    ai_result = analyze_code_with_gemini(fetched_files)
    
    if "error" in ai_result:
         raise HTTPException(status_code=500, detail=ai_result["error"])

    return RepoResponse(
        status="success",
        owner=owner,
        repo=repo,
        files_analyzed=list(fetched_files.keys()),
        ai_analysis=ai_result
    )