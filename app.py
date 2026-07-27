import streamlit as st
import json
import os
from github import Github

st.set_page_config(page_title="Achadinhos da Cris", page_icon="📚", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto, .preco-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #4A4A4A !important;
    }
    .preco-texto { font-weight: bold; color: #2E7D32 !important; margin-bottom: 5px; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)
GITHUB_REPO = st.secrets.get("GITHUB_REPO", None)
NOME_ARQUIVO = "produtos.json"

def carregar_produtos():
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(GITHUB_REPO)
            conteudo = repo.get_contents(NOME_ARQUIVO, ref="main")
            return json.loads(conteudo.decoded_content.decode("utf-8"))
        except Exception:
            return []
    return []

st.markdown("<h1 class='titulo-principal'>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px 0;'>", unsafe_allow_html=True)

produtos = carregar_produtos()

if not produtos:
    st.markdown("<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>", unsafe_allow_html=True)
    st.markdown("<p class='preco-texto'>Apenas: R$ 38,75</p>", unsafe_allow_html=True)
    st.link_button(label="👉 Ver Livro Perfeitamente Diferentes na Amazon", url="https://amazon.com.br", use_container_width=True)
else:
    for prod in reversed(produtos):
        st.markdown(f"<h3 class='secao-texto'>📖 {prod['titulo']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='preco-texto'>Apenas: R$ {prod['preco']}</p>", unsafe_allow_html=True)
        
        nome_imagem = prod.get("imagem_instagram", "")
        if "anuncio_" in nome_imagem:
            asin_limpo = nome_imagem.replace("anuncio_", "").replace(".jpg", "")
            link_perfeito = f"https://amazon.com.br{asin_limpo}?tag=abielstore-20"
        else:
            link_perfeito = prod['link']

        st.link_button(label="👉 Ver na Amazon", url=link_perfeito, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<p class='rodape-texto' style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. 💕</p>", unsafe_allow_html=True)

# Contato do WhatsApp
st.markdown("<hr style='border: 0; height: 1px; background: #E0E0E0; margin: 20px 0;'>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo' style='font-size: 14px;'>Ficou com alguma dúvida ou quer bater um papo?</p>", unsafe_allow_html=True)

NUMERO_WHATSAPP = "5548988480217" # Mude para o número real se quiser
url_whatsapp = f"https://wa.me{NUMERO_WHATSAPP}?text=Olá,%20Cris!%20Vi%20um%20produto%20no%20seu%20site%20e%20gostaria%20de%20tirar%20uma%20dúvida."

st.link_button(label="💬 Chamar a Cris no WhatsApp", url=url_whatsapp, use_container_width=True)
