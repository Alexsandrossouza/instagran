import streamlit as st
import json
import os
from github import Github

# Configuração da página e design móvel
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
    else:
        if os.path.exists(NOME_ARQUIVO) and os.path.getsize(NOME_ARQUIVO) > 0:
            try:
                with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

def salvar_produtos_github(lista_produtos):
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(GITHUB_REPO)
            novo_conteudo = json.dumps(lista_produtos, indent=4, ensure_ascii=False)
            try:
                conteudo = repo.get_contents(NOME_ARQUIVO, ref="main")
                repo.update_file(conteudo.path, "Atualiza lista de achadinhos", novo_conteudo, conteudo.sha, branch="main")
            except Exception:
                repo.create_file(NOME_ARQUIVO, "Cria lista inicial de achadinhos", novo_conteudo, branch="main")
            return True
        except Exception:
            return False
    else:
        try:
            with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
                json.dump(lista_produtos, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

# --- VISÃO DO VISITANTE ---
st.markdown("<h1 class='titulo-principal'>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px 0;'>", unsafe_allow_html=True)

produtos = carregar_produtos()

if not produtos:
    st.markdown("<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>", unsafe_allow_html=True)
    st.markdown("<p class='preco-texto'>Apenas: R$ 38,75</p>", unsafe_allow_html=True)
    st.link_button(
        label="👉 Ver Livro Perfeitamente Diferentes na Amazon", 
        url="https://amazon.com.br", 
        use_container_width=True
    )
else:
    for prod in reversed(produtos):
        st.markdown(f"<h3 class='secao-texto'>📖 {prod['titulo']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='preco-texto'>Apenas: R$ {prod['preco']}</p>", unsafe_allow_html=True)
        st.link_button(label="👉 Ver na Amazon", url=prod['link'], use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<p class='rodape-texto' style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. 💕</p>", unsafe_allow_html=True)

# --- PAINEL DO ADMINISTRADOR ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)
abrir_painel = st.checkbox("⚙️ Acessar Painel de Cadastro (Área da Cris)")

if abrir_painel:
    senha = st.text_input("Digite sua senha de acesso:", type="password")
    if senha == "cris123": 
        st.success("Acesso liberado!")
        
        with st.form("cadastro_produto", clear_on_submit=True):
            novo_titulo = st.text_input("Título do Produto:")
            novo_preco = st.text_input("Preço (Ex: 38,75):")
            novo_asin = st.text_input("Código do Produto na Amazon (ASIN ou ISBN):").strip().replace(" ", "")
            foto_upload = st.file_uploader("Escolha a foto do produto:", type=["webp", "jpg", "jpeg", "png"])
            botao_salvar = st.form_submit_button("Salvar Produto")
            
            if botao_salvar and novo_titulo and novo_preco and novo_asin:
                # FÓRMULA CORRIGIDA NO LUGAR CERTO: Dentro do bloco de salvamento
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
                    st.success("Produto adicionado com sucesso!")
                    st.rerun()

        if "ultimo_anuncio" in st.session_state and os.path.exists(st.session_state["ultimo_anuncio"]):
            st.subheader("📸 Seu Anúncio do Instagram está Pronto!")
            st.image(st.session_state["ultimo_anuncio"], use_container_width=True)
            
            with open(st.session_state["ultimo_anuncio"], "rb") as file:
                st.download_button(
                    label="📥 Baixar Imagem para o Celular/PC",
                    data=file,
                    file_name=st.session_state["ultimo_anuncio"],
                    mime="image/jpeg",
                    use_container_width=True
                )
