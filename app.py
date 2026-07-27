import streamlit as st

# Configuração da página
st.set_page_config(page_title="Achadinhos da Cris", page_icon="📚", layout="centered")

# Estilização Personalizada
st.markdown("""
    <style>
    /* Cor de fundo da página (Bege suave) */
    .stApp {
        background-color: #FDFBF7; 
    }
    
    /* Estilo dos Botões de Link do Streamlit */
    div.stLinkButton > a {
        background-color: #6C8EBF !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px 24px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100% !important;
        text-align: center !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efeito ao passar o mouse no botão */
    div.stLinkButton > a:hover {
        background-color: #52719C !important;
        transform: translateY(-2px);
    }
    
    /* Estilo do Card do Produto */
    .product-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #EAEAEA;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    
    /* Textos centrais */
    h1, h3, p {
        text-align: center;
        color: #4A4A4A;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("<h1>📚 Achadinhos da Cris</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; font-style: italic; color: #666;'>Indicações de leituras edificantes, novidades e achadinhos especiais com muito carinho! ✨</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- RECOMENDAÇÃO EM DESTAQUE ---
st.markdown("### 📖 Sugestão de Leitura Cristã")

# Se você quiser adicionar a foto da capa do livro depois, coloque o arquivo da imagem na mesma pasta e descomente a linha abaixo:
# st.image("capa_livro.jpg", use_column_width=True)

st.markdown("""
    <div class="product-card">
        <h3 style="margin-top:0;">Perfeitamente Diferentes</h3>
        <p style="color: #666; font-size: 14px; margin-bottom: 20px;">
            Uma excelente indicação de leitura edificante para abençoar sua vida e seus relacionamentos. Garanta o seu exemplar diretamente na Amazon!
        </p>
    </div>
""", unsafe_allow_html=True)

# BOTÃO DE LINK DIRETO (Funciona de primeira no clique!)
st.link_button("👉 Ver Livro Perfeitamente Diferentes na Amazon", "https://a.co/d/0cPSR7aq", use_container_width=True)

# --- RODAPÉ ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 12px; color: #9A9A9A;'>Como participante do Programa de Associados da Amazon, posso receber comissões por compras qualificadas. Obrigada pelo apoio! 💕</p>", unsafe_allow_html=True)