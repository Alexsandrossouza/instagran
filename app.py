import streamlit as st

# 1. Configuração da página (Título interno do navegador)
st.set_page_config(page_title="Achadinhos da Cris", page_icon="📚", layout="centered")

# 2. Estilização CSS personalizada (Conserta as cores e limita o tamanho estilo celular)
st.markdown("""
    <style>
    /* Cor de fundo da página */
    .stApp {
        background-color: #FDFBF7; 
    }
    
    /* Força todos os textos a terem a cor correta e estarem centralizados */
    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #4A4A4A !important;
    }
    
    /* Container para o site não ficar espalhado na tela do PC */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("<h1 class='titulo-principal'>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes, novidades e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)

# Linha divisória charmosa
st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px 0;'>", unsafe_allow_html=True)

# --- SEÇÃO DE PRODUTOS ---
st.markdown("<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>", unsafe_allow_html=True)

link_amazon = "https://a.co"

# Botão nativo do Streamlit: mais seguro, responsivo e com clique direto
st.link_button(
    "👉 Ver Livro Perfeitamente Diferentes na Amazon", 
    link_amazon, 
    use_container_width=True
)

# --- RODAPÉ ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p class='rodape-texto' style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. Obrigada pelo apoio! 💕</p>", unsafe_allow_html=True)
