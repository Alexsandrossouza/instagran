import json
import os
import streamlit as st
from github import Github

# Configuração da página
st.set_page_config(
    page_title="Achadinhos da Cris", page_icon="📚", layout="centered"
)

# Estilização do layout
st.markdown(
    """
    <style>
    .stApp { background-color: #d4aebe; }
    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto, .preco-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #f7cf02 !important;
    }
    .preco-texto { font-weight: bold; color: #2E7D32 !important; margin-bottom: 5px; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #a8406b !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background-color: #8c3256 !important;
        color: #FFFFFF !important;
        border-color: transparent !important;
        transform: scale(1.02);
    }

    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #a8406b !important;
        border-radius: 6px !important;
    }

    .stCheckbox label, .stTextInput label {
        color: #4A4A4A !important;
        font-weight: bold !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

try:
    from gerador import criar_imagem_produto

    gerador_disponivel = True
except Exception:
    gerador_disponivel = False

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)
GITHUB_REPO = st.secrets.get("GITHUB_REPO", None)
NOME_ARQUIVO = "produtos.json"

st.cache_data.clear()


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
            novo_conteudo = json.dumps(
                lista_produtos, indent=4, ensure_ascii=False
            )
            conteudo = repo.get_contents(NOME_ARQUIVO, ref="main")
            repo.update_file(
                conteudo.path,
                "Atualiza lista de achadinhos",
                novo_conteudo,
                conteudo.sha,
                branch="main",
            )
            st.cache_data.clear()
            return True
        except Exception:
            return False
    return False


# --- VISÃO DO VISITANTE ---
st.markdown(
    "<h1 class='titulo-principal'>📚 Achadinhos da Cris 📚</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações"
    " de leituras edificantes e utilidades com muito carinho! ✨</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px"
    " 0;'>",
    unsafe_allow_html=True,
)

produtos = carregar_produtos()

if not produtos:
    st.markdown(
        "<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='preco-texto'>Apenas: R$ 38,75</p>", unsafe_allow_html=True
    )
    st.link_button(
        label="👉 Ver Livro Perfeitamente Diferentes na Amazon",
        url="https://amazon.com.br",
        use_container_width=True,
    )
else:
    for prod in reversed(produtos):
        # Layout Lado a Lado (Coluna da Imagem e Coluna de Dados)
        col_img, col_info = st.columns([1, 2])

        nome_img = prod.get("imagem_instagram", "")
        asin = prod.get("asin", "")

        if not asin and "anuncio_" in nome_img:
            asin = (
                nome_img.replace("anuncio_", "")
                .replace(".jpg", "")
                .replace(".png", "")
            )

        with col_img:
            imagem_exibida = False

            # 1. Procura se a imagem existe na pasta local
            if nome_img and os.path.exists(nome_img):
                st.image(nome_img, use_container_width=True)
                imagem_exibida = True

            # 2. Procura qualquer arquivo na pasta que tenha o ASIN no nome
            elif asin:
                for arq in os.listdir("."):
                    if asin in arq and arq.endswith(
                        (".jpg", ".png", ".jpeg", ".webp")
                    ):
                        st.image(arq, use_container_width=True)
                        imagem_exibida = True
                        break

            # 3. Se não achou na pasta local, busca da Amazon
            if not imagem_exibida and asin:
                st.image(
                    f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_.jpg",
                    use_container_width=True,
                )

        with col_info:
            st.markdown(
                f"<h4 style='text-align: left; color: #4A4A4A;"
                f" margin-bottom: 5px;'>📖 {prod['titulo']}</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: left; font-weight: bold; color:"
                f" #2E7D32; margin-bottom: 10px;'>Apenas: R$ {prod['preco']}</p>",
                unsafe_allow_html=True,
            )

            link_perfeito = prod.get("link", "#")
            st.link_button(
                label="👉 Ver na Amazon",
                url=link_perfeito,
                use_container_width=True,
            )

        st.markdown(
            "<hr style='border: 0; height: 1px; background: #a8406b; margin:"
            " 15px 0;'>",
            unsafe_allow_html=True,
        )

st.markdown(
    "<p class='rodape-texto' style='font-size: 12px; color: #9A9A9A;'>Ao comprar"
    " através dos links acima, eu ganho uma pequena comissão da Amazon."
    " 💕</p>",
    unsafe_allow_html=True,
)

# Contato do WhatsApp
st.markdown(
    "<hr style='border: 0; height: 1px; background: #a8406b; margin: 20px"
    " 0;'>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtitulo' style='font-size: 14px;'>Ficou com alguma dúvida ou"
    " quer bater um papo?</p>",
    unsafe_allow_html=True,
)

NUMERO_WHATSAPP = "5548988480217"
url_whatsapp = (
    f"https://wa.me/{NUMERO_WHATSAPP}?text=Olá,%20Cris!%20Vi%20um%20produto%20no%20seu%20site%20e%20gostaria%20de%20tirar%20uma%20dúvida."
)
st.link_button(
    label="💬 Chamar a Cris no WhatsApp",
    url=url_whatsapp,
    use_container_width=True,
)

# --- PAINEL DO ADMINISTRADOR ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)
abrir_painel = st.checkbox("⚙️ Acessar Painel de Cadastro (Área da Cris)")

if abrir_painel:
    senha = st.text_input("Digite sua senha de acesso:", type="password")
    if senha == "cris123":
        st.success("Acesso liberado!")

        if produtos:
            st.subheader("🗑️ Gerenciar/Apagar Produtos")
            for i, prod in enumerate(produtos):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{prod['titulo']}** - R$ {prod['preco']}")
                with col2:
                    if st.button("Apagar", key=f"del_{i}"):
                        produtos.pop(i)
                        if salvar_produtos_github(produtos):
                            st.toast("Item removido!")
                            st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("➕ Adicionar Novo Achadinho")
        with st.form("cadastro_produto", clear_on_submit=True):
            novo_titulo = st.text_input("Título do Produto:")
            novo_preco = st.text_input("Preço (Ex: 38,75):")
            novo_asin = (
                st.text_input("Código na Amazon (ASIN ou ISBN):")
                .strip()
                .replace(" ", "")
            )
            foto_upload = st.file_uploader(
                "Escolha a foto:", type=["webp", "jpg", "jpeg", "png"]
            )
            botao_salvar = st.form_submit_button("Salvar Produto")

            if botao_salvar and novo_titulo and novo_preco and novo_asin:
                link_automatizado = f"https://www.amazon.com.br/dp/{novo_asin}?tag=abielstore-20"
                nome_anuncio_final = f"anuncio_{novo_asin}.jpg"

                if foto_upload and gerador_disponivel:
                    with open("temp_original.jpg", "wb") as f:
                        f.write(foto_upload.getbuffer())
                    try:
                        criar_imagem_produto(
                            caminho_produto="temp_original.jpg",
                            titulo=novo_titulo,
                            preco=f"R$ {novo_preco}",
                            caminho_salvamento=nome_anuncio_final,
                        )
                    except Exception:
                        pass

                lista_atual = carregar_produtos()
                novo_item = {
                    "titulo": novo_titulo,
                    "preco": novo_preco,
                    "link": link_automatizado,
                    "imagem_instagram": nome_anuncio_final,
                    "asin": novo_asin,
                }
                lista_atual.append(novo_item)

                if salvar_produtos_github(lista_atual):
                    st.balloons()
                    st.success("Produto cadastrado com sucesso!")
                    st.rerun()