from PIL import Image

def slice_horizontal(image_path, num_slices):
    # Abre a imagem
    img = Image.open(image_path)
    
    # Obtém largura e altura da imagem
    width, height = img.size
    
    # Calcula o número de fatias horizontalmente
    slice_width = width // num_slices
    
    # Lista para armazenar as fatias
    slices = []
    
    # Fatiamento horizontal
    for i in range(num_slices):
        # Calcula as coordenadas da fatia
        left = i * slice_width
        upper = 0
        right = left + slice_width
        lower = height
        
        # Corta a fatia
        slice_img = img.crop((left, upper, right, lower))
        
        # Adiciona a fatia à lista
        slices.append(slice_img)
    
    return slices

# Caminho da imagem
image_path = "img/Martial Hero 2/Sprites/Death.png"

# Largura de cada fatia
slice_width = 7  # Altere o valor para o tamanho desejado

# Fatiamento horizontal
slices = slice_horizontal(image_path, slice_width)

# Salva cada fatia
for i, slice_img in enumerate(slices):
    slice_img.save(f"img/Martial Hero 2/Death/slice_{i}.png")