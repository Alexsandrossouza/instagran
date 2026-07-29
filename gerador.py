import os
from PIL import Image, ImageDraw, ImageFont


def criar_imagem_produto(caminho_produto, titulo, preco, caminho_salvamento):
    # 1. Definir o tamanho padrão do Instagram Feed (1080x1080)
    largura_canvas, altura_canvas = 1080, 1080

    # 2. Criar a imagem de fundo branca (1080x1080)
    imagem_final = Image.new(
        "RGB", (largura_canvas, altura_canvas), (255, 255, 255)
    )
    draw = ImageDraw.Draw(imagem_final)

    # 3. Verificação de segurança: Checa se a imagem original existe
    if not os.path.exists(caminho_produto):
        print(f"Erro: A imagem {caminho_produto} não foi encontrada.")
        return

    # 4. Abrir e redimensionar a imagem do produto (Tamanho expandido para destacar no Feed)
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

    # 5. Configurar as fontes
    try:
        # Carrega a fonte Arial se estiver no Windows
        fonte_titulo = ImageFont.truetype("arial.ttf", 45)
        fonte_preco = ImageFont.truetype("arial.ttf", 65)
        fonte_cta = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        # Fallback para o servidor Linux do Streamlit
        fonte_titulo = ImageFont.load_default()
        fonte_preco = ImageFont.load_default()
        fonte_cta = ImageFont.load_default()

    # 6. Adicionar os textos na imagem
    # Título (Posição 120, centralizado no topo)
    draw.text(
        (largura_canvas // 2, 120),
        titulo,
        fill=(50, 50, 50),
        font=fonte_titulo,
        anchor="mm",
    )

    # Preço em Destaque (Posição 880 na cor laranja)
    draw.text(
        (largura_canvas // 2, 880),
        f"Apenas: {preco}",
        fill=(225, 115, 0),
        font=fonte_preco,
        anchor="mm",
    )

    # Chamada para Ação / CTA (Posição 980 no rodapé)
    draw.text(
        (largura_canvas // 2, 980),
        "Clique no link para aproveitar!",
        fill=(100, 100, 100),
        font=fonte_cta,
        anchor="mm",
    )

        # 7. Salvar a imagem final pronta para o Instagram dentro da pasta Imagen
    # 🟢 CORREÇÃO DA FÓRMULA: Força o salvamento na pasta correta
    caminho_final_pasta = f"Imagen/{caminho_salvamento}"
    
    imagem_final.save(caminho_final_pasta, "JPEG", quality=95)
    print(f"Sucesso! Imagem salva em: {caminho_final_pasta}")



# --- EXEMPLO DE TESTE LOCAL ---
if __name__ == "__main__":
    criar_imagem_produto(
        caminho_produto="bateria.webp",
        titulo="Bateria Controle Xbox Series S/X",
        preco="R$ 149,90",
        caminho_salvamento="anuncio_instagram.jpg",
    )