import os
from PIL import Image

from Product import Product

# Set the product directory
PRODUCT = Product.Hoodies.India.Back()

# Set up the design image
design_path = "automate_design/designs/design_1.png"
design_image = Image.open(design_path).convert("RGBA")

# Set up the directory paths
clothing_dir = f"automate_design/clothing_images/{PRODUCT.dir_name}"
export_dir = f"automate_design/exports/{PRODUCT.dir_name}"

def automate_design():
    try: 
        print('Automate Design: Starting now.')
        # Loop over all the images in the clothing directory
        for filename in os.listdir(clothing_dir):
            if filename.endswith(".png"):
                print(f'Automate Design: Starting to add design to {filename}.')
                # Set up the clothing image
                clothing_path = os.path.join(clothing_dir, filename)
                clothing_image = Image.open(clothing_path).convert("RGBA")

                # Resize the design image to fit on the clothing image
                max_width, max_height = get_max_width_height(clothing_image)
                design_image.thumbnail((max_width, max_height), Image.LANCZOS)

                # Paste the clothing image onto the canvas
                final_image = clothing_image.copy()

                # Paste the design image onto the clothing image
                design_position = get_design_postion(clothing_image)
                final_image.paste(design_image, design_position, design_image)

                # Save the final image in JPEG format
                export_path = os.path.join(export_dir, f'{filename.split("_", 1)[0]}.jpg')
                final_image.convert('RGB').save(export_path, optimize=True, quality=90)
                print(f'Automate Design: Added design to {export_path}.')
        print('Automate Design: Successfully completed execution.')
    except Exception as e:
        print(f'Automate Design: Error occurred - {e}.')
        raise

def get_max_width_height(clothing_image):
    if PRODUCT.dir_name == 'oversized_tees':
        max_width = int(clothing_image.size[0] / 3)
        max_height = int(clothing_image.size[1] / 3)
    elif PRODUCT.dir_name == 'classic_tees':
        max_width = int(clothing_image.size[0] / 2)
        max_height = int(clothing_image.size[1] / 2)
    elif PRODUCT.dir_name == 'tote_bags':
        max_width = clothing_image.size[0] / 1.8
        max_height = int(clothing_image.size[1] / 2)
    elif PRODUCT.dir_name == 'hoodies/back':
        max_width = clothing_image.size[0] / 3
        max_height = int(clothing_image.size[1] / 2)
    elif PRODUCT.dir_name == 'hoodies/india/back':
        max_width = clothing_image.size[0] / 2.6
        max_height = clothing_image.size[1] / 2.4
    elif PRODUCT.dir_name == 'sweatshirts/back':
        max_width = clothing_image.size[0] / 3
        max_height = clothing_image.size[1] / 3
    elif PRODUCT.dir_name == 'sweatshirts/front':
        max_width = clothing_image.size[0] / 2.5
        max_height = clothing_image.size[1] / 2.5
    else:
        max_width = int(clothing_image.size[0] / 2)
        max_height = int(clothing_image.size[1] / 2)
    return max_width, max_height

def get_design_postion(clothing_image):
    if PRODUCT.dir_name == 'tote_bags':
        return (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 1.40))
    elif PRODUCT.dir_name == 'hoodies/front':
        return (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 1.8))
    elif PRODUCT.dir_name == 'hoodies/back':
        return (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 1.65))
    elif PRODUCT.dir_name == 'hoodies/india/back':
        return (int((clothing_image.size[0] - design_image.size[0]) / 1.95), int((clothing_image.size[1] - design_image.size[1]) / 1.9))
    elif PRODUCT.dir_name == 'sweatshirts/front':
        return (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 2.3))
    elif PRODUCT.dir_name == 'sweatshirts/back':
        return (int((clothing_image.size[0] - design_image.size[0]) / 2.23), int((clothing_image.size[1] - design_image.size[1]) / 2))
    else:
        return (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 2))

automate_design()
