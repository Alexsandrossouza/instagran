import json
import os
import streamlit as st
from github import Github

# 1. Configuração da página
st.set_page_config(
    page_title="Achadinhos da Cris", page_icon="📚", layout="centered"
)

# 2. Estilização CSS
st.markdown(
    """
    <style>
    /* Oculta barras padrão do Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp { background-color: #d4aebe; }
    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto, .preco-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #f7cf02 !important;
    }
    .preco-texto { font-weight: bold; color: #2E7D32 !important; margin-bottom: 5px; }
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }
    
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #a8406b !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background-color: #d16f96 !important;
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
        color: #121212 !important;
        font-weight: bold !important;
    }

    /* Regra para travar todas as fotos com a mesma altura padrão */
    div[data-testid="stImage"] img {
        height: 320px !important;
        object-fit: contain !important;
        width: 100% !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Importação do Gerador de Imagens (se existir)
try:
    from gerador import criar_imagem_produto

    gerador_disponivel = True
except Exception:
    gerador_disponivel = False


# 4. Funções para carregar e salvar produtos no GitHub
def carregar_produtos():
    if os.path.exists("produtos.json"):
        with open("produtos.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def salvar_produtos_github(produtos_lista):
    try:
        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(produtos_lista, f, ensure_ascii=False, indent=4)

        token = st.secrets.get("GITHUB_TOKEN")
        repo_name = st.secrets.get("GITHUB_REPO")

        if token and repo_name:
            g = Github(token)
            repo = g.get_repo(repo_name)
            contents = repo.get_contents("produtos.json")
            json_str = json.dumps(produtos_lista, ensure_ascii=False, indent=4)
            repo.update_file(
                contents.path,
                "Atualizando produtos.json",
                json_str,
                contents.sha,
            )
            return True
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False


# Carrega a lista inicial de produtos
produtos = carregar_produtos()

# ==========================================
# 👑 CABEÇALHO (ADMIN + WHATSAPP NO TOPO)
# ==========================================
col_admin, col_whats = st.columns([1, 1])

with col_admin:
    if st.button("🔐 Admin", key="btn_admin_topo"):
        st.session_state["modo_admin"] = not st.session_state.get(
            "modo_admin", False
        )

with col_whats:
    # ⚠️ Troque pelo número real da Cris (Com DDD e 55 na frente)
    numero_whatsapp = "5548988480217"
    mensagem = "Olá Cris! Vim pelo site e gostaria de tirar uma dúvida."

    link_wa = (
        f"https://wa.me/{numero_whatsapp}?text={mensagem.replace(' ', '%20')}"
    )
    st.link_button("💬 Falar no WhatsApp", link_wa, use_container_width=True)
# ==========================================
# 🔐 PAINEL DE ADMINISTRADOR (Aparece se clicar no botão)
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

# ==========================================
# 🔍 BARRA DE BUSCA E CONFIGURAÇÕES NO TOPO
# ==========================================

# ==========================================
# 🔍 BARRA DE BUSCA (ESTILO ADAPTADO)
# ==========================================
termo_busca = st.text_input(
    label="Pesquise seu produto...",
    placeholder="Pesquise seu produto...",
    key="campoBusca",
    label_visibility="collapsed",  # Esconde o rótulo padrão para ficar idêntico ao HTML
)

# Filtra a lista de produtos de acordo com o texto digitado
produtos_exibir = [
    p
    for p in produtos
    if termo_busca.lower() in p.get("titulo", "").lower()
]

# Mensagem quando nada for encontrado (adaptada com as cores do site)
if termo_busca and not produtos_exibir:
    st.markdown(
        """
        <div style="text-align: center; color: #a8406b; font-weight: bold; padding: 20px; background-color: #ffffff; border-radius: 8px; margin-top: 10px;">
            Este produto não foi encontrado em nosso site. 😢
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

# Estilização do layout
st.markdown(
    """
    <style>
        /* 1. RESTAURAR COR DE FUNDO (Lilás) */
        .stApp {
            background-color: #eb87ed !important; /* Cor Lilás de fundo */
        }

        /* 2. RESTAURAR ESTILO DO TÍTULO (Rosa Choque) */
        .titulo-principal {
            color: #f7208f !important;
            text-align: center;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-weight: bold;
        }

        /* Deixa os campos de busca e seleção com fundo branco e cantos arredondados no topo */
div[data-baseweb="input"], div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
}

        /* 3. TEXTOS GERAIS */
        .subtitulo, .secao-texto, .rodape-texto {
            text-align: center;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #4A4A4A;
        }
        
        .preco-texto {
            color: #2E7D32 !important; /* Verde do preço */
            font-weight: bold;
            text-align: center;
        }

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

        div[data-testid="stLinkButton"] > a:hover {
            background-color: #F0F0F0 !important; /* Fundo ligeiramente mais escuro no hover */
            border-color: #A9A9A9 !important;     /* Borda mais escura no hover */
            transform: translateY(-2px);           /* Pequeno efeito de flutuar */
        }

        /* 5. MANTER A CORREÇÃO DE TAMANHO DAS IMAGENS */
        div[data-testid="stColumn"] img, img {
            max-height: 230px !important;
            height: 230px !important;
            object-fit: contain !important;
            width: 100% !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        /* 6. AJUSTAR O ESPAÇAMENTO DO CONTEÚDO */
        .block-container {
            max-width: 600px !important;
            padding-top: 2rem !important;
        }
        /* Customização do Campo de Busca */
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border-radius: 25px !important; /* Deixa a barra de busca arredondada */
    border: 2px solid #a8406b !important; /* Cor da borda combinando com o botão */
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
# Tenta carregar o gerador de imagens
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


# ==============================================================================
# 🛍️ VISÃO DO VISITANTE (PARTE PÚBLICA DO SITE)
# ==============================================================================

# 📌 TÍTULO PRINCIPAL DO SITE

st.markdown(
    "<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações"
    " de leituras edificantes e utilidades com muito carinho! ✨</p>",
    unsafe_allow_html=True,
)

# 📌 LINHA DIVISÓRIA (AZUL)
st.markdown(
    "<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px"
    " 0;'>",  # 👈 background: #6C8EBF define a cor azul da linha
    unsafe_allow_html=True,
)

produtos = carregar_produtos()

# ------------------------------------------------------------------------------
# SE NÃO HOUVER PRODUTOS CADASTRADOS (MOSTRA O PRODUTO PADRÃO/SUGESTÃO)
# ------------------------------------------------------------------------------
if not produtos:
    st.markdown(
        "<h3 class='secao-texto'>📖 Sugestão de Leitura Cristã</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='preco-texto'>Apenas: R$ 38,75</p>", unsafe_allow_html=True
    )

    # 🔘 BOTÃO 1: Botão do produto padrão (Sugestão de Leitura)
    st.link_button(
        label="👉 Ver Livro Perfeitamente Diferentes na Amazon",  # Texto no botão
        url="https://amazon.com.br",
        use_container_width=True,
    )

# ------------------------------------------------------------------------------
# SE HOUVER PRODUTOS CADASTRADOS (MOSTRA A LISTA DE PRODUTOS)
# ------------------------------------------------------------------------------
else:
    for prod in reversed(produtos):
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
                f"<h4 style='text-align: left; color: #4A4A4A;"
                f" margin-bottom: 5px;'>📖 {prod['titulo']}</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: left; font-weight: bold; color:"
                f" #2E7D32; margin-bottom: 10px;'>Apenas: R$ {prod['preco']}</p>",
                unsafe_allow_html=True,
            )

            # 🔘 BOTÃO 2: Botão de compra de cada produto da lista
            link_perfeito = prod.get("link", "#")
            st.link_button(
                label="👉 Ver na Amazon",  # Texto do botão de compra
                url=link_perfeito,
                use_container_width=True,
            )

        # 📌 LINHA DIVISÓRIA ENTRE PRODUTOS (ROSA)
        st.markdown(
            "<hr style='border: 0; height: 1px; background: #6C8EBF; margin:"
            " 15px 0;'>",  # 👈 background: #e60e0e define a cor rosa da linha
            unsafe_allow_html=True,
        )

# Rodapé explicativo
st.markdown(
    "<p class='rodape-texto' style='font-size: 12px; color: #e60e0e;'>Ao comprar"
    " através dos links acima, eu ganho uma pequena comissão da Amazon."
    " 💕</p>",
    unsafe_allow_html=True,
)