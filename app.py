import streamlit as st

# Configuração da página (Título que aparece na aba do navegador)
st.set_page_config(page_title="Meus Achadinhos da Amazon", page_icon="🌸", layout="centered")

# Estilização Personalizada (Cores suaves, meigas e femininas)
st.markdown("""
    <style>
    /* Cor de fundo da página (Rosa bem claro/pastel) */
    .stApp {
        background-color: #FFF0F5; 
    }
    
    /* Estilo dos Botões de Links */
    .stButton > button {
        background-color: #FFB6C1; /* Rosa claro */
        color: #4A4A4A; /* Texto cinza escuro para ficar legível */
        border-radius: 20px; /* Bordas arredondadas e delicadas */
        border: 2px solid #FFA07A; /* Borda pêssego suave */
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 500;
        width: 100%;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    /* Efeito ao passar o mouse no botão */
    .stButton > button:hover {
        background-color: #FFC0CB; /* Rosa um pouco mais vivo */
        border-color: #FF69B4;
        color: #FFFFFF;
        transform: scale(1.02);
    }
    
    /* Títulos e textos centrais */
    h1, h3, p {
        text-align: center;
        color: #5D5D5D;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONTEÚDO DO SEU SITE ---

# Ícone e Título Principal (Estilo cabeçalho de perfil)
st.markdown("<h1>🌸 Meus Achadinhos 🌸</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; font-style: italic;'>Os melhores produtos da Amazon que eu uso e recomendo com muito amor! ✨</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: #FFB6C1; margin-bottom: 30px;'>", unsafe_allow_html=True)

# BOTÃO 1: Câmera de Segurança (O produto que você estava vendo)
st.markdown("<h3>📸 Segurança & Praticidade</h3>", unsafe_allow_html=True)
if st.button("👉 Ver Câmera de Segurança WiFi Externa na Amazon"):
    # Substitua pelo seu link de afiliado da Amazon gerado no SiteStripe
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://amzn.to\'">', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# BOTÃO 2: Exemplo de outro produto do seu nicho
st.markdown("<h3>🎮 Meu Cantinho Gamer / Tech</h3>", unsafe_allow_html=True)
if st.button("👉 Ver Bateria para Controle de Xbox na Amazon"):
    # Substitua pelo seu link de afiliado da Amazon gerado no SiteStripe
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://www.amazon.com.br/Seguran%C3%A7a-Bidirecional-Rastreamento-Autom%C3%A1tico-Compat%C3%ADvel/dp/B0H5L5MTSQ/ref=pd_rhf_gw_s_pd_crcd_d_sccl_1_2/145-8498386-9315941?psc=1\'">', unsafe_allow_html=True)

# Rodapé delicado
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. Obrigada pelo apoio! 💕</p>", unsafe_allow_html=True)
