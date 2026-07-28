import json
import os
import streamlit as st
from github import Github

# Configuração da página (Aba do navegador)
st.set_page_config(
    page_title="Achadinhos da Cris", page_icon="📚", layout="centered"
)

# ==============================================================================
# 🎨 BLOCO DE ESTILOS CSS (AQUI FICA A COR DE TODOS OS BOTÕES E FUNDOS)
# ==============================================================================
st.markdown(
    """
    <style>
    /* 1. COR DE FUNDO DO SITE (Rosa Claro) */
    .stApp { background-color: #d4aebe; }



    .titulo-principal, .subtitulo, .secao-texto, .rodape-texto, .preco-texto {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* 2. COR DO PREÇO DO PRODUTO (Verde) */
    .preco-texto { font-weight: bold; color: #2E7D32 !important; margin-bottom: 5px; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    
    /* 3. ESTILO DOS BOTÕES (Afeta TODOS os botões e links do site) */
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #a8406b !important; /* 👈 COR DE FUNDO DO BOTÃO (Rosa) */
        color: #FFFFFF !important;            /* 👈 COR DO TEXTO DO BOTÃO (Branco) */
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    /* 4. COR DO BOTÃO AO PASSAR O MOUSE POR CIMA */
    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background-color: #8c3256 !important; /* 👈 COR AO PASSAR O MOUSE (Rosa Escuro) */
        color: #FFFFFF !important;            /* 👈 COR DO TEXTO AO PASSAR O MOUSE */
        border-color: transparent !important;
        transform: scale(1.02);
    }

    /* 5. CAMPOS DE TEXTO (Onde você digita) */
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
    (
        "<h1 class='titulo-principal' style='color: #f7208f"
        " !important;'>📚 Achadinhos da Cris </h1>"
    ),  # 👈 style='color: #f7208f' define a cor do Título (Rosa Choque)
    unsafe_allow_html=True,
)

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

# ------------------------------------------------------------------------------
# CONTATO DO WHATSAPP
# ------------------------------------------------------------------------------
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

# 🔘 BOTÃO 3: Botão de redirecionamento para o WhatsApp
st.link_button(
    label="💬 Chamar a Cris no WhatsApp",  # Texto do botão do WhatsApp
    url=url_whatsapp,
    use_container_width=True,
)

# ==============================================================================
# ⚙️ PAINEL DO ADMINISTRADOR (ÁREA PRIVADA DA CRIS)
# ==============================================================================
st.markdown("<br><hr><br>", unsafe_allow_html=True)

# 🔘 BOTÃO/CHECKBOX 4: Caixa para abrir o painel do administrador
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
                    # 🔘 BOTÃO 5: Botão "Apagar" dentro do painel
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

            # 🔘 BOTÃO 6: Botão para enviar e salvar o novo produto
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