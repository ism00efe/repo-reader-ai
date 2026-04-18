import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY bulunamadı! .env dosyanızı kontrol edin.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_code_with_gemini(github_files: dict):
    context_text = "Target Repository Files:\n\n"
    
    for filename, content in github_files.items():
        # Token optimization: Truncate files larger than ~10KB (approx 2500 lines)
        if len(content) > 10000:
            content = content[:10000] + "\n...[TRUNCATED FOR CONTEXT LIMIT]..."
        context_text += f"--- FILE: {filename} ---\n{content}\n\n"

    prompt = f"""
    Sen kıdemli bir yazılım mimarı ve DevSecOps uzmanısın.
    Aşağıdaki GitHub dosyalarını incele ve sadece geçerli bir JSON döndür.
    
    JSON Schema:
    {{
      "summary": "Projenin ne işe yaradığını, framework'leri ve DB'yi anlatan 2-3 cümle.",
      "security_alerts": ["Güvenlik açığı 1", "Eksik bağımlılık veya risk 2"],
      "mermaid_diagram": "graph TD;\\n  A[Frontend] --> B[Backend];"
    }}

    Data to Analyze:
    {context_text}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
        
    except Exception as e:
        return {"error": f"LLM Generation Error: {str(e)}"}