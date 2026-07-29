import os
import shutil
from PIL import Image, ImageDraw, ImageFont


def criar_imagem_produto(caminho_produto, titulo, preco, caminho_salvamento):
    """
    Processa a imagem enviada no cadastro:
    1. Salva a foto LIMPA e sem textos com o nome do ASIN para o carrossel do site.
    2. Cria uma versão quadrada com textos exclusiva para postar no Instagram.
    """
    # Verificação de segurança: Checa se a imagem original existe
    if not os.path.exists(caminho_produto):
        print(f"Erro: A imagem {caminho_produto} não foi encontrada.")
        return

    # =========================================================================
    # 🟢 ETAPA 1: SALVAR A FOTO LIMPA PARA O CARROSSEL DO SITE
    # =========================================================================
    # O app.py precisa da foto pura do produto salva diretamente na pasta.
    # Se o caminho de salvamento original for "anuncio_B0XXX.jpg", mudamos para "B0XXX.jpg"
    nome_arquivo_limpo = caminho_salvamento.replace("anuncio_", "")
    
    try:
        # Copia o arquivo original diretamente para o destino do site (mantém a foto pura)
        shutil.copy(caminho_produto, nome_arquivo_limpo)
        print(f"Sucesso! Imagem limpa para o site salva em: {nome_arquivo_limpo}")
    except Exception as e:
        print(f"Aviso: Não foi possível salvar a imagem limpa para o site. Erro: {e}")

    # =========================================================================
    # 📸 ETAPA 2: GERAR A IMAGEM QUADRADA DE DIVULGAÇÃO (INSTAGRAM FEED)
    # =========================================================================
    largura_canvas, altura_canvas = 1080, 1080

    # Criar a imagem de fundo branca (1080x1080)
    imagem_final = Image.new(
        "RGB", (largura_canvas, altura_canvas), (255, 255, 255)
    )
    draw = ImageDraw.Draw(imagem_final)

    # Abrir e redimensionar a imagem do produto para o feed
    img_produto = Image.open(caminho_produto)
    img_produto.thumbnail((850, 700))
    largura_prod, altura_prod = img_produto.size

    # Centraliza horizontalmente e ajusta a posição vertical entre o título e o preço
    pos_x = (largura_canvas - largura_prod) // 2
    pos_y = (largura_canvas - altura_prod) // 2 - 20

    # Cola o produto no fundo branco (preservando transparência se houver)
    if img_produto.mode in ("RGBA", "LA"):
        imagem_final.paste(img_produto, (pos_x, pos_y), img_produto)
    else:
        imagem_final.paste(img_produto, (pos_x, pos_y))

    # Configurar as fontes
    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 45)
        fonte_preco = ImageFont.truetype("arial.ttf", 65)
        fonte_cta = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        fonte_titulo = ImageFont.load_default()
        fonte_preco = ImageFont.load_default()
        fonte_cta = ImageFont.load_default()

    # Adicionar os textos na imagem do Instagram
    # Título
    draw.text(
        (largura_canvas // 2, 120),
        titulo,
        fill=(50, 50, 50),
        font=fonte_titulo,
        anchor="mm",
    )

    # Preço em Destaque (Laranja)
    draw.text(
        (largura_canvas // 2, 880),
        f"Apenas: {preco}",
        fill=(225, 115, 0),
        font=fonte_preco,
        anchor="mm",
    )

    # Chamada para Ação / CTA
    draw.text(
        (largura_canvas // 2, 980),
        "Clique no link para aproveitar!",
        fill=(100, 100, 100),
        font=fonte_cta,
        anchor="mm",
    )

    # Cria um nome específico focado na sua divulgação do Instagram (ex: instagram_anuncio_B0XXX.jpg)
    caminho_instagram = f"instagram_{caminho_salvamento}"
    imagem_final.save(caminho_instagram, "JPEG", quality=95)
    print(f"Sucesso! Imagem de divulgação salva em: {caminho_instagram}")


# --- EXEMPLO DE TESTE LOCAL ---
if __name__ == "__main__":
    # Teste simulando o cadastro de um produto
    criar_imagem_produto(
        caminho_produto="bateria.webp",
        titulo="Bateria Controle Xbox Series S/X",
        preco="R$ 149,90",
        caminho_salvamento="anuncio_B0123456.jpg",
    )
