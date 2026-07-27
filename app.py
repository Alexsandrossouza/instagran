import streamlit as st

# Configuração da página
st.set_page_config(page_title="Achadinhos da Cris", page_icon="📚", layout="centered")

# Estilização do fundo da página
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF7; 
    }
    h1, h3, p {
        text-align: center;
        color: #4A4A4A;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("<h1>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes, novidades e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- BOTÃO DE LINK DIRETO (HTML) ---
st.markdown("<h3>📖 Sugestão de Leitura Cristã</h3>", unsafe_allow_html=True)

# Link direto em HTML estilizado
link_amazon = "https://a.co/d/0cPSR7aq"

st.markdown(f'''
    <div style="text-align: center; margin-top: 20px;">
        <a href="{link_amazon}" target="_blank" style="
            display: inline-block;
            width: 100%;
            background-color: #6C8EBF;
            color: white;
            padding: 16px 20px;
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            border-radius: 8px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            transition: 0.3s;
        ">
            👉 Ver Livro Perfeitamente Diferentes na Amazon
        </a>
    </div>
''', unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. Obrigada pelo apoio! 💕</p>", unsafe_allow_html=True)
