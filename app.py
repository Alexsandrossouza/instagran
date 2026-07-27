import streamlit as st
import json
import os
# Importa a função que você criou no seu outro arquivo
from gerador import criar_imagem_produto

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

# Arquivo local para salvar os dados
ARQUIVO_BANCO = "produtos.json"

# Inicializa o arquivo local caso ele não exista
if not os.path.exists(ARQUIVO_BANCO):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump([], f)

# Função para carregar os produtos cadastrados
def carregar_produtos():
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
        return json.load(f)

# --- VISÃO DO VISITANTE DO INSTAGRAM ---
st.markdown("<h1 class='titulo-principal'>📚 Achadinhos da Cris 📚</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo' style='font-size: 16px; font-style: italic;'>Indicações de leituras edificantes e utilidades com muito carinho! ✨</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #6C8EBF; margin: 20px 0;'>", unsafe_allow_html=True)

produtos = carregar_produtos()

if not produtos:
    st.info("Nenhum produto listado no momento. Volte em breve! 💕")
else:
    # Mostra os produtos do mais recente para o mais antigo
    for prod in reversed(produtos):
        st.markdown(f"<h3 class='secao-texto'>📖 {prod['titulo']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='preco-texto'>Apenas: {prod['preco']}</p>", unsafe_allow_html=True)
        
        st.link_button(
            label="👉 Ver na Amazon", 
            url=prod['link'], 
            use_container_width=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<p class='rodape-texto' style='font-size: 12px; color: #9A9A9A;'>Ao comprar através dos links acima, eu ganho uma pequena comissão da Amazon. 💕</p>", unsafe_allow_html=True)

# --- PAINEL DO ADMINISTRADOR (ÁREA OCULTA) ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)
abrir_painel = st.checkbox("⚙️ Acessar Painel de Cadastro (Área da Cris)")

if abrir_painel:
    senha = st.text_input("Digite sua senha de acesso:", type="password")
    # Defina a senha que preferir aqui
    if senha == "cris123": 
        st.success("Acesso liberado!")
        st.subheader("Cadastrar Novo Achadinho")
        
        with st.form("cadastro_produto", clear_on_submit=True):
            novo_titulo = st.text_input("Título do Produto:")
            novo_preco = st.text_input("Preço (Ex: R$ 149,90):")
            novo_link = st.text_input("Link de Afiliado Amazon:")
            
            # Carregar a foto original do produto recebida do fornecedor
            foto_upload = st.file_uploader("Escolha a foto do produto (WebP, JPG, PNG):", type=["webp", "jpg", "jpeg", "png"])
            
            botao_salvar = st.form_submit_button("Salvar Produto e Criar Anúncio")
            
            if botao_salvar and novo_titulo and novo_preco and novo_link and foto_upload:
                # 1. Salva temporariamente o arquivo de imagem enviado pelo navegador
                nome_imagem_original = foto_upload.name
                with open(nome_imagem_original, "wb") as f:
                    f.write(foto_upload.getbuffer())
                
                # Definir o nome de saída da imagem final tratada do Instagram
                nome_anuncio_final = f"anuncio_{nome_imagem_original.split('.')[0]}.jpg"
                
                # 2. Executa a função do seu arquivo gerador.py de forma totalmente automatizada!
                criar_imagem_produto(
                    caminho_produto=nome_imagem_original,
                    titulo=novo_titulo,
                    preco=novo_preco,
                    caminho_salvamento=nome_anuncio_final
                )
                
                # 3. Adiciona as informações no nosso arquivo JSON (banco de dados Python)
                novo_item = {
                    "titulo": novo_titulo,
                    "preco": novo_preco,
                    "link": novo_link,
                    "imagem_instagram": nome_anuncio_final
                }
                
                produtos.append(novo_item)
                with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
                    json.dump(produtos, f, indent=4, ensure_ascii=False)
                
                st.balloons()
                st.success(f"Sucesso! Produto cadastrado e imagem '{nome_anuncio_final}' gerada na sua pasta!")
