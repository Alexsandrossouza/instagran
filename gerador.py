import os
from PIL import Image, ImageDraw, ImageFont

def criar_imagem_produto(caminho_produto, titulo, preco, caminho_salvamento):
    # 1. Definir o tamanho padrão do Instagram Feed (1080x1080)
    largura_canvas, altura_canvas = 1080, 1080
    
    # 2. Criar uma imagem de fundo (fundo branco limpo)
    # Você pode mudar (255, 255, 255) para a cor RGB que preferir
    imagem_final = Image.new("RGB", (largura_canvas, altura_canvas), (255, 255, 255))
    draw = ImageDraw.Draw(imagem_final)
    
    # 3. Abrir e redimensionar a imagem do produto
    if not os.path.exists(caminho_produto):
        print(f"Erro: A imagem {caminho_produto} não foi encontrada.")
        return
        
    img_produto = Image.open(caminho_produto)
    
    # Redimensiona o produto para caber bem no centro (ex: máximo 600x600 pixels)
    img_produto.thumbnail((600, 600))
    largura_prod, altura_prod = img_produto.size
    
    # Calcular posição para centralizar o produto horizontalmente e um pouco acima do meio
    pos_x = (largura_canvas - largura_prod) // 2
    pos_y = (altura_canvas - altura_prod) // 2 - 50
    
    # Colar a imagem do produto sobre o fundo branco
    # Usamos img_produto como máscara se ela tiver fundo transparente (PNG)
    if img_produto.mode in ('RGBA', 'LA'):
        imagem_final.paste(img_produto, (pos_x, pos_y), img_produto)
    else:
        imagem_final.paste(img_produto, (pos_x, pos_y))
        
    # 4. Configurar as fontes para os textos
    # Tenta carregar uma fonte padrão do sistema, se não conseguir usa a básica do Pillow
    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 50)
        fonte_preco = ImageFont.truetype("arial.ttf", 70)
        fonte_cta = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        print("Aviso: Fonte Arial não encontrada. Usando fonte padrão.")
        fonte_titulo = ImageFont.load_default()
        fonte_preco = ImageFont.load_default()
        fonte_cta = ImageFont.load_default()

    # 5. Adicionar os textos na imagem
    # Título do produto (no topo)
    draw.text((largura_canvas // 2, 80), titulo, fill=(50, 50, 50), font=fonte_titulo, anchor="mm")
    
    # Preço do produto (abaixo do produto)
    draw.text((largura_canvas // 2, 880), f"Apenas: {preco}", fill=(225, 115, 0), font=fonte_preco, anchor="mm")
    
    # Chamada para ação (CTA no rodapé)
    draw.text((largura_canvas // 2, 980), "Clique no link da bio para aproveitar!", fill=(100, 100, 100), font=fonte_cta, anchor="mm")
    
    # 6. Salvar a imagem final pronta para postar
    imagem_final.save(caminho_salvamento, "JPEG", quality=95)
    print(f"Sucesso! Imagem salva em: {caminho_salvamento}")

# --- EXEMPLO DE USO DO SCRIPT ---
if __name__ == "__main__":
    # Configure aqui os dados do seu produto
    # IMPORTANTE: Coloque uma foto chamada 'teste.jpg' na mesma pasta para o script funcionar
    criar_imagem_produto(
        caminho_produto="Bateria Controle Para Xbox Séries S X 1200mah Cabo 3m.webp", 
        titulo="Bateria Controle Para Xbox Séries S X 1200mah", 
        preco="R$ 149,90", 
        caminho_salvamento="anuncio_instagram.jpg"
    )
