import streamlit as st

# Configuração da página (Título que aparece na aba do navegador)
st.set_page_config(page_title="Achadinhos da Cris", page_icon="📚", layout="centered")

# Estilização Personalizada (Cores suaves e elegantes para o nicho literário e cristão)
st.markdown("""
    <style>
    /* Cor de fundo da página (Bege muito claro/pastel - lembra folha de livro) */
    .stApp {
        background-color: #FDFBF7; 
    }
    
    /* Estilo dos Botões de Links (Azul Sereno / Clássico) */
    .stButton > button {
        background-color: #6C8EBF; /* Azul sereno */
        color: #FFFFFF; /* Texto branco para contraste perfeito */
        border-radius: 8px; /* Bordas levemente arredondadas e clássicas */
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 500;
        width: 100%;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    /* Efeito ao passar o mouse no botão */
    .stButton > button:hover {
        background-color: #52719C; /* Azul um pouco mais profundo */
        color: #FFFFFF;
        transform: scale(1.01);
    }
    
    /* Títulos e textos centrais */
    h1, h3, p {
        text-align: center;
        color: #4A4A4A;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONTEÚDO DO SITE ---

# Ícone e Título Principal
st.markdown("<h1>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes, novidades e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin-bottom: 30px;'>", unsafe_allow_html=True)

# BOTÃO 1: O Livro "Perfeitamente Diferentes"
st.markdown("<h3>📖 Sugestão de Leitura Cristã</h3>", unsafe_allow_html=True)
if st.button("👉 Ver Livro Perfeitamente Diferentes na Amazon"):
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://a.co/d/0cPSR7aq\'">', unsafe_allow_html=True)

# Rodapé obrigatório da Amazon
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. Obrigada pelo apoio! 💕</p>", unsafe_allow_html=True)
