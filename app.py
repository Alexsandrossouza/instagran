import json
import os
import streamlit as st
from github import Github

# ==========================================
# 🎨 PALETA DE CORES (Cores de alto contraste e legibilidade)
# ==========================================
COR_FUNDO_SITE = "#eb87ed"  # Lilás/Rosa do fundo
COR_TITULO_PRINCIPAL = "#F009C9"  # Branco em destaque com sombra para o título
COR_SUBTITULO = "#FFFFFF"  # Branco legível para as frases
COR_TEXTO_PRODUTO = "#121013"  # Roxo escuro bem visível para o nome dos produtos
COR_BOTOES = "#a8406b"  # Vinho/Rosa escuro dos botões e busca
COR_BOTOES_HOVER = "#8c3256"  # Tom escuro do botão no hover
COR_PRECO = "#FA0606"  # Verde limão chamativo e de alta leitura
COR_LINHA_DIVISORIA = "#6C8EBF"  # Azul das linhas
COR_RODAPE = "#FFFFFF"  # Branco para o rodapé

# 1. Configuração da página
st.set_page_config(
    page_title="Achadinhos da Cris", page_icon="📚", layout="centered"
)

st.markdown(
    """
    <style>
    /* Fundo da aplicação */
    .stApp { background-color: #d4aebe; }
    
    /* Textos principais */
    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto, .preco-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #4A4A4A !important;
    }
    .preco-texto { font-weight: bold; color: #2E7D32 !important; margin-bottom: 5px; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    
    /* FIX: Estilo bonito para os Botões (link_button e button) */
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #a8406b !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    /* FIX: Efeito ao passar o mouse em cima (Hover) */
    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background-color: #8c3256 !important;
        color: #FFFFFF !important;
        border-color: transparent !important;
        transform: scale(1.02);
    }

    /* FIX: Estilo para os inputs de texto e senha */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #a8406b !important;
        border-radius: 6px !important;
    }

    /* FIX: Textos de Labels e Checkbox visíveis */
    .stCheckbox label, .stTextInput label {
        color: #4A4A4A !important;
        font-weight: bold !important;
    }
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

# ==========================================
# 👑 1º LUGAR: TÍTULO E SUBTÍTULO
# ==========================================
st.markdown(
    "<h1 class='titulo-principal'>Achadinhos da Cris</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p class='subtitulo'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>",
    unsafe_allow_html=True,
)

# ==========================================
# 🔘 2º LUGAR: BOTÕES (ADMIN + WHATSAPP)
# ==========================================
col_admin, col_whats = st.columns([1, 1])

with col_admin:
    if st.button("🔐 Admin", key="btn_admin_topo"):
        st.session_state["modo_admin"] = not st.session_state.get(
            "modo_admin", False
        )

with col_whats:
    numero_whatsapp = "5548988480217"
    mensagem = "Olá Cris! Vim pelo site e gostaria de tirar uma dúvida."
    link_wa = (
        f"https://wa.me/{numero_whatsapp}?text={mensagem.replace(' ', '%20')}"
    )
    st.link_button("💬 Falar no WhatsApp", link_wa, use_container_width=True)

# ==========================================
# 🔍 3º LUGAR: BARRA DE BUSCA
# ==========================================
termo_busca = st.text_input(
    label="Pesquise seu produto...",
    placeholder="Pesquise seu produto...",
    key="campoBusca",
    label_visibility="collapsed",
)

st.markdown(
    f"<hr style='border: 0; height: 1px; background: {COR_LINHA_DIVISORIA}; margin: 15px 0;'>",
    unsafe_allow_html=True,
)

# Filtra produtos
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

# ==============================================================================
# 🛍️ VISÃO DO VISITANTE (CABEÇALHO FIXO)
# ==============================================================================

# Encapsulamos tudo dentro de um container especial para travar tudo junto no topo
with st.container():
    # 📌 1º LUGAR: TÍTULO E SUBTÍTULO
    st.markdown(
        "<h1 class='titulo-principal'>Achadinhos da Cris</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subtitulo'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>",
        unsafe_allow_html=True,
    )

    # 🔘 2º LUGAR: BOTÕES (ADMIN + WHATSAPP)
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

    # 🔍 3º LUGAR: BARRA DE BUSCA
    termo_busca = st.text_input(
        label="Pesquise seu produto...",
        placeholder="Pesquise seu produto...",
        key="campoBusca",
        label_visibility="collapsed",
    )

    # Linha divisória após a busca
    st.markdown(
        f"<hr style='border: 0; height: 1px; background: {COR_LINHA_DIVISORIA}; margin: 15px 0;'>",
        unsafe_allow_html=True,
    )
# ------------------------------------------------------------------------------
# LISTA DE PRODUTOS
# ------------------------------------------------------------------------------
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