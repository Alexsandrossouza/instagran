import streamlit as st
import json
import os
from github import Github

st.set_page_config(page_title="Painel da Cris", page_icon="⚙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    .titulo-principal, .secao-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #4A4A4A !important;
    }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

try:
    from gerador import criar_imagem_produto
    gerador_disponivel = True
except Exception:
    gerador_disponivel = False

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

def salvar_produtos_github(lista_produtos):
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(GITHUB_REPO)
            novo_conteudo = json.dumps(lista_produtos, indent=4, ensure_ascii=False)
            conteudo = repo.get_contents(NOME_ARQUIVO, ref="main")
            repo.update_file(conteudo.path, "Atualiza lista de achadinhos", novo_conteudo, conteudo.sha, branch="main")
            return True
        except Exception:
            return False
    return False

st.markdown("<h1 class='titulo-principal'>⚙️ Área Administrativa</h1>", unsafe_allow_html=True)

senha = st.text_input("Digite sua senha de acesso:", type="password")
if senha == "cris123": 
    st.success("Acesso liberado!")
    
    produtos = carregar_produtos()
    
    # Gerenciador de Exclusão
    if produtos:
        st.subheader("🗑️ Gerenciar/Apagar Produtos")
        for i, prod in enumerate(produtos):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{prod['titulo']}** - R$ {prod['preco']}")
            with col2:
                if st.button("Apagar", key=f"del_{i}"):
                    produtos.pop(i)
                    if salvar_produtos_github(produtos):
                        st.toast("Item removido!")
                        st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)

    # Formulário de Cadastro
    st.subheader("➕ Adicionar Novo Achadinho")
    with st.form("cadastro_produto", clear_on_submit=True):
        novo_titulo = st.text_input("Título do Produto:")
        novo_preco = st.text_input("Preço (Ex: 38,75):")
        novo_asin = st.text_input("Código na Amazon (ASIN ou ISBN):").strip().replace(" ", "")
        foto_upload = st.file_uploader("Escolha a foto:", type=["webp", "jpg", "jpeg", "png"])
        botao_salvar = st.form_submit_button("Salvar Produto")
        
        if botao_salvar and novo_titulo and novo_preco and novo_asin:
            link_automatizado = f"https://amazon.com.br{novo_asin}?tag=abielstore-20"
            nome_anuncio_final = f"anuncio_{novo_asin}.jpg"
            
            if foto_upload and gerador_disponivel:
                with open("temp_original.jpg", "wb") as f:
                    f.write(foto_upload.getbuffer())
                try:
                    criar_imagem_produto(
                        caminho_produto="temp_original.jpg",
                        titulo=novo_titulo,
                        preco=f"R$ {novo_preco}",
                        caminho_salvamento=nome_anuncio_final
                    )
                    st.session_state["ultimo_anuncio"] = nome_anuncio_final
                except Exception:
                    pass
            
            lista_atual = carregar_produtos()
            novo_item = {
                "titulo": novo_titulo,
                "preco": novo_preco,
                "link": link_automatizado,
                "imagem_instagram": nome_anuncio_final
            }
            lista_atual.append(novo_item)
            
            if salvar_produtos_github(lista_atual):
                st.balloons()
                st.success("Produto cadastrado com sucesso!")
                st.rerun()

    if "ultimo_anuncio" in st.session_state and os.path.exists(st.session_state["ultimo_anuncio"]):
        st.subheader("📸 Seu Anúncio está Pronto!")
        st.image(st.session_state["ultimo_anuncio"], use_container_width=True)
        with open(st.session_state["ultimo_anuncio"], "rb") as file:
            st.download_button(label="📥 Baixar Imagem", data=file, file_name=st.session_state["ultimo_anuncio"], mime="image/jpeg", use_container_width=True)
