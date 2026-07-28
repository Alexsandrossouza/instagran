import json
import os
import streamlit as st
from github import Github

# ==========================================
# 🎨 PALETA DE CORES
# ==========================================
COR_FUNDO_SITE = "#eb87ed"  # Lilás/Rosa do fundo
COR_TITULO_PRINCIPAL = "#FFFFFF"  # Branco em destaque para o título
COR_SUBTITULO = "#FFFFFF"  # Branco legível para as frases
COR_TEXTO_PRODUTO = "#2C1B2E"  # Roxo escuro para o nome dos produtos
COR_BOTOES = "#a8406b"  # Vinho/Rosa escuro dos botões e busca
COR_BOTOES_HOVER = "#8c3256"  # Tom escuro do botão no hover
COR_PRECO = "#00FF66"  # Verde limão chamativo
COR_LINHA_DIVISORIA = "#6C8EBF"  # Azul das linhas
COR_RODAPE = "#FFFFFF"  # Branco para o rodapé

# 1. Configuração da página
st.set_page_config(
    page_title="Achadinhos da Cris", page_icon="📚", layout="centered"
)

# 2. Estilização CSS utilizando as referências de cores
st.markdown(
    f"""
    <style>
    /* Oculta barras padrão do Streamlit */
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* 1. COR DE FUNDO */
    .stApp {{
        background-color: {COR_FUNDO_SITE} !important;
    }}

    /* TRAVA O CABEÇALHO INTEIRO NO TOPO */
    div[data-testid="stVerticalBlock"] > div:first-child {{
        position: sticky !important;
        top: 0 !important;
        z-index: 9999 !important;
        background-color: {COR_FUNDO_SITE} !important;
        padding-top: 10px !important;
        padding-bottom: 5px !important;
    }}

    /* 2. TÍTULO PRINCIPAL */
    .titulo-principal {{
        color: {COR_TITULO_PRINCIPAL} !important;
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800;
        font-size: 32px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-top: 5px;
        margin-bottom: 5px;
    }}

    /* 3. SUBTÍTULO E TEXTOS */
    .subtitulo {{
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: {COR_SUBTITULO} !important;
        font-size: 15px !important;
        font-style: italic;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        margin-bottom: 10px;
    }}

    .secao-texto {{
        text-align: center;
        color: {COR_TEXTO_PRODUTO} !important;
        font-weight: bold;
    }}
    
    .preco-texto {{
        color: {COR_PRECO} !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
    }}

    .rodape-texto {{
        text-align: center;
        color: {COR_RODAPE} !important;
        font-weight: 500;
    }}

    /* 4. BOTÕES */
    .stButton > button, div[data-testid="stLinkButton"] > a {{
        background-color: {COR_BOTOES} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {{
        background-color: {COR_BOTOES_HOVER} !important;
        color: #FFFFFF !important;
        border-color: transparent !important;
        transform: scale(1.02);
    }}

    /* CAMPO DE BUSCA */
    div[data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        border-radius: 25px !important;
        border: 2px solid {COR_BOTOES} !important;
    }}

    .stTextInput input {{
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border-radius: 6px !important;
    }}

    /* IMAGENS */
    div[data-testid="stColumn"] img, img {{
        max-height: 230px !important;
        height: 230px !important;
        object-fit: contain !important;
        width: 100% !important;
        margin: 0 auto !important;
        display: block !important;
    }}
    
    /* Ajusta a largura no PC mantendo perfeito no celular */
    .block-container {{
        max-width: 1000px !important; /* Aumentado para expandir no computador */
        padding-top: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Importação do Gerador de Imagens
try:
    from gerador import criar_imagem_produto

    gerador_disponivel = True
except Exception:
    gerador_disponivel = False

# Credenciais do GitHub
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)
GITHUB_REPO = st.secrets.get("GITHUB_REPO", None)
NOME_ARQUIVO = "produtos.json"

st.cache_data.clear()


# Função para carregar produtos
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


# Função para salvar produtos
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


# Carrega a lista de produtos
produtos = carregar_produtos()

# ==============================================================================
# 👑 CABEÇALHO TRAVADO NO TOPO (TÍTULO ➔ BOTÕES ➔ BUSCA)
# ==============================================================================
with st.container():
    # 📌 1º: TÍTULO E SUBTÍTULO
    st.markdown(
        "<h1 class='titulo-principal'>Achadinhos da Cris</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subtitulo'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>",
        unsafe_allow_html=True,
    )

    # 🔘 2º: BOTÕES (ADMIN + WHATSAPP)
    col_admin, col_whats = st.columns([1, 1])

    with col_admin:
        if st.button("🔐 Admin", key="btn_admin_topo"):
            st.session_state["modo_admin"] = not st.session_state.get(
                "modo_admin", False
            )

    with col_whats:
        numero_whatsapp = "5548988480217"
        mensagem = "Olá Cris! Vim pelo site e gostaria de tirar uma dúvida."
        link_wa = f"https://wa.me/{numero_whatsapp}?text={mensagem.replace(' ', '%20')}"
        st.link_button(
            "💬 Falar no WhatsApp", link_wa, use_container_width=True
        )

    # 🔍 3º: BARRA DE BUSCA
    termo_busca = st.text_input(
        label="Pesquise seu produto...",
        placeholder="Pesquise seu produto...",
        key="campoBusca",
        label_visibility="collapsed",
    )

    # Linha divisória
    st.markdown(
        f"<hr style='border: 0; height: 1px; background: {COR_LINHA_DIVISORIA}; margin: 15px 0;'>",
        unsafe_allow_html=True,
    )

# ==========================================
# 🔐 PAINEL DE ADMINISTRADOR (Aparece se clicar em Admin)
# ==========================================
if st.session_state.get("modo_admin", False):
    st.info(" Área Restrita do Administrador")
    senha = st.text_input(
        "Digite sua senha de acesso:", type="password", key="senha_admin"
    )

    if senha == "cris123":
        st.success("Acesso liberado!")

        if produtos:
            st.subheader("🗑️ Gerenciar/Apagar Produtos")
            for i, prod in enumerate(produtos):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{prod['titulo']}** - R$ {prod['preco']}")
                with col2:
                    if st.button("Apagar", key=f"del_{i}"):
                        produtos.pop(i)
                        salvar_produtos_github(produtos)
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
    elif senha != "":
        st.error("Senha incorreta!")

# ==============================================================================
# 🛍️ LISTAGEM DOS PRODUTOS
# ==============================================================================

# Filtra produtos da busca
produtos_exibir = [
    p
    for p in produtos
    if termo_busca.lower() in p.get("titulo", "").lower()
]

# Mensagem de item não encontrado
if termo_busca and not produtos_exibir:
    st.markdown(
        f"""
        <div style="text-align: center; color: {COR_BOTOES}; font-weight: bold; padding: 20px; background-color: #ffffff; border-radius: 8px; margin-top: 10px;">
            Este produto não foi encontrado em nosso site. 😢
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

# Exibição dos produtos
if not produtos:
    st.markdown(
        "<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p class='preco-texto'>Apenas: R$ 38,75</p>", unsafe_allow_html=True
    )

    st.link_button(
        label="👉 Ver Livro Perfeitamente Diferentes na Amazon",
        url="https://amazon.com.br",
        use_container_width=True,
    )

else:
    for prod in reversed(produtos_exibir):
        col_img, col_info = st.columns([1, 2])

        nome_img = prod.get("imagem_instagram", "")
        asin = prod.get("asin", "")

        if not asin and "anuncio_" in nome_img:
            asin = (
                nome_img.replace("anuncio_", "")
                .replace(".jpg", "")
                .replace(".png", "")
                .replace(".webp", "")
            )

        with col_img:
            imagem_exibida = False

            if nome_img and os.path.exists(nome_img):
                st.image(nome_img, use_container_width=True)
                imagem_exibida = True

            elif asin:
                for arq in os.listdir("."):
                    if asin in arq and arq.endswith(
                        (".jpg", ".png", ".jpeg", ".webp")
                    ):
                        st.image(arq, use_container_width=True)
                        imagem_exibida = True
                        break

            if not imagem_exibida and asin:
                st.image(
                    f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_.jpg",
                    use_container_width=True,
                )

        with col_info:
            st.markdown(
                f"<h4 style='text-align: left; color: {COR_TEXTO_PRODUTO};"
                f" font-weight: bold; margin-bottom: 5px;'>📖 {prod['titulo']}</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='preco-texto' style='text-align: left; margin-bottom: 10px;'>Apenas: R$ {prod['preco']}</p>",
                unsafe_allow_html=True,
            )

            link_perfeito = prod.get("link", "#")
            st.link_button(
                label="👉 Ver na Amazon",
                url=link_perfeito,
                use_container_width=True,
            )

        st.markdown(
            f"<hr style='border: 0; height: 1px; background: {COR_LINHA_DIVISORIA}; margin: 15px 0;'>",
            unsafe_allow_html=True,
        )

# RODAPÉ
st.markdown(
    f"<p class='rodape-texto' style='font-size: 12px;'>Ao comprar"
    " através dos links acima, eu ganho uma pequena comissão da Amazon."
    " 💕</p>",
    unsafe_allow_html=True,
)