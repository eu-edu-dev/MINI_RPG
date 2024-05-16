from PIL import Image
import os


def slice_horizontal(image_path, width_crop, height_crop):
    # Abre a imagem
    img = Image.open(image_path)

    # Obtém largura e altura da imagem
    width, height = img.size

    # Calcula o número de fatias horizontalmente


    # Lista para armazenar as fatias
    slices = []

    # Fatiamento horizontal

    # Calcula as coordenadas da fatia
    left = (width - (width_crop))/2
    upper = (height - height_crop)/2
    right = (width )
    lower = (height + height_crop)/2

    # Corta a fatia
    slice_img = img.crop((left, upper, right, lower))

    # Adiciona a fatia à lista
    slices.append(slice_img)

    return slice_img


# Caminho da imagem
image_path = "img/Skeleton/Attack"


# Fatiamento horizontal
i = 0

# Salva cada fatia
for file_name in sorted(os.listdir(image_path)):
    if i >= 6:
        slice_img = slice_horizontal(f"{image_path}/{file_name}", 60, 60)
        slice_img.save(f"{image_path}/{file_name}")
    i += 1

# slice_img = slice_horizontal(f"{image_path}/slice_2.png", 100, 60)
# slice_img.save(f"slice_{3}.png")
# slice_img = slice_horizontal(f"{image_path}/slice_3.png", 100, 60)
# slice_img.save(f"slice_{4}.png")