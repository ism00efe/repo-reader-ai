import streamlit as st
import requests
import streamlit.components.v1 as components

# Backend API URL
API_URL = "http://127.0.0.1:8000/api/analyze"

st.set_page_config(page_title="RepoReader AI", page_icon="🚀", layout="wide")

st.title("🚀 RepoReader AI")
st.subheader("Anında GitHub Repozitori Analizi ve Mimari Çıkarımı")

repo_url = st.text_input("GitHub Repo URL'sini girin:", placeholder="https://github.com/owner/repo")

def render_mermaid(code: str):
    """Mermaid.js grafiğini HTML bileşeni olarak render eder."""
    html_code = f"""
    <div class="mermaid">
        {code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(html_code, height=400)

if st.button("Analiz Et"):
    if repo_url:
        with st.spinner("AI dosyaları okuyor ve mimariyi çözümlüyor... Bu birkaç saniye sürebilir."):
            try:
                response = requests.post(API_URL, json={"repo_url": repo_url})
                
                if response.status_code == 200:
                    data = response.json()
                    ai_data = data.get("ai_analysis", {})
                    
                    st.success(f"Başarılı! Analiz edilen proje: {data['owner']}/{data['repo']}")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("### 📝 Proje Özeti")
                        st.info(ai_data.get("summary", "Özet bulunamadı."))
                        
                        st.markdown("### 🛡️ Güvenlik Uyarıları")
                        alerts = ai_data.get("security_alerts", [])
                        if alerts:
                            for alert in alerts:
                                st.warning(f"- {alert}")
                        else:
                            st.success("Belirgin bir güvenlik riski bulunamadı.")
                            
                        st.markdown("### 📁 Analiz Edilen Dosyalar")
                        st.write(", ".join(data.get("files_analyzed", [])))
                        
                    with col2:
                        st.markdown("### 🏗️ Sistem Mimarisi")
                        mermaid_code = ai_data.get("mermaid_diagram", "")
                        if mermaid_code:
                            render_mermaid(mermaid_code)
                        else:
                            st.error("Mimari şema oluşturulamadı.")
                else:
                    st.error(f"Hata: {response.json().get('detail', 'Bilinmeyen bir hata oluştu.')}")
            except requests.exceptions.ConnectionError:
                st.error("Backend'e bağlanılamadı. FastAPI sunucusunun (uvicorn main:app --reload) çalıştığından emin olun.")
    else:
        st.warning("Lütfen geçerli bir GitHub URL'si girin.")