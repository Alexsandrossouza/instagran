import streamlit as st
import json
import os

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
except Exception as e:
    gerador_disponivel = False

# Caminho absoluto para persistência dos dados no servidor
ARQUIVO_BANCO = os.path.join(os.getcwd(), "produtos.json")

if not os.path.exists(ARQUIVO_BANCO) or os.path.getsize(ARQUIVO_BANCO) == 0:
    try:
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
            json.dump([], f)
    except Exception:
        pass

def carregar_produtos():
    if os.path.exists(ARQUIVO_BANCO):
        try:
            with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    return dados
        except Exception:
            return []
    return []

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
                # CORREÇÃO CRUCIAL: Inserido a estrutura /dp/ obrigatória para o link funcionar na Amazon
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
                    except Exception as e:
                        st.error(f"Erro ao gerar imagem: {e}")
                
                lista_atual = carregar_produtos()
                
                novo_item = {
                    "titulo": novo_titulo,
                    "preco": novo_preco,
                    "link": link_automatizado,
                    "imagem_instagram": nome_anuncio_final
                }
                
                lista_atual.append(novo_item)
                
                try:
                    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
                        json.dump(lista_atual, f, indent=4, ensure_ascii=False)
                    st.balloons()
                    st.success("Produto adicionado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar arquivo: {e}")

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
