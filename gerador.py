import os
from PIL import Image, ImageDraw, ImageFont

def criar_imagem_produto(caminho_produto, titulo, preco, caminho_salvamento):
    # 1. Definir o tamanho padrão do Instagram Feed (1080x1080)
    largura_canvas, altura_canvas = 1080, 1080
    
    # 2. Criar uma imagem de fundo branca
    imagem_final = Image.new("RGB", (largura_canvas, altura_canvas), (255, 255, 255))
    draw = ImageDraw.Draw(imagem_final)
    
    # 3. Abrir e redimensionar a imagem do produto
    if not os.path.exists(caminho_produto):
        print(f"Erro: A imagem {caminho_produto} não foi encontrada.")
        return
        
    img_produto = Image.open(caminho_produto)
    img_produto.thumbnail((600, 600))
    largura_prod, altura_prod = img_produto.size
    
    pos_x = (largura_canvas - largura_prod) // 2
    pos_y = (altura_canvas - altura_prod) // 2 - 50
    
    if img_produto.mode in ('RGBA', 'LA'):
        imagem_final.paste(img_produto, (pos_x, pos_y), img_produto)
    else:
        imagem_final.paste(img_produto, (pos_x, pos_y))
        
    # 4. Configurar as fontes para os textos
    try:
        # Tenta carregar a Arial (se estiver no Windows)
        fonte_titulo = ImageFont.truetype("arial.ttf", 45)
        fonte_preco = ImageFont.truetype("arial.ttf", 65)
        fonte_cta = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        # Se estiver no servidor Linux do Streamlit
        fonte_titulo = ImageFont.load_default()
        fonte_preco = ImageFont.load_default()
        fonte_cta = ImageFont.load_default()

    # 5. Adicionar os textos na imagem
        # 5. Adicionar os textos na imagem (Título ajustado para a posição 120 para não cortar no topo)
    draw.text((largura_canvas // 2, 120), titulo, fill=(50, 50, 50), font=fonte_titulo, anchor="mm")
    draw.text((largura_canvas // 2, 880), f"Apenas: {preco}", fill=(225, 115, 0), font=fonte_preco, anchor="mm")
    draw.text((largura_canvas // 2, 980), "Clique no link para aproveitar!", fill=(100, 100, 100), font=fonte_cta, anchor="mm")
    
    # 6. Salvar a imagem final
    imagem_final.save(caminho_salvamento, "JPEG", quality=95)
    print(f"Sucesso! Imagem salva em: {caminho_salvamento}")

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    criar_imagem_produto(
        caminho_produto="bateria.webp", 
        titulo="Bateria Controle Xbox Series S/X", 
        preco="R$ 149,90", 
        caminho_salvamento="anuncio_instagram.jpg"
    )