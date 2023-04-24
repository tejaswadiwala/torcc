import os
from PIL import Image

# Set up the design image
design_path = "automate_design/designs/design_1.png"
design_image = Image.open(design_path).convert("RGBA")

# Set up the directory paths
clothing_dir = "automate_design/clothing_images/"
export_dir = "automate_design/exports/"

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
                max_width = int(clothing_image.size[0] / 2)
                max_height = int(clothing_image.size[1] / 2)
                design_image.thumbnail((max_width, max_height), Image.LANCZOS)

                # Paste the clothing image onto the canvas
                final_image = clothing_image.copy()

                # Paste the design image onto the clothing image
                design_position = (int((clothing_image.size[0] - design_image.size[0]) / 2), int((clothing_image.size[1] - design_image.size[1]) / 2))
                final_image.paste(design_image, design_position, design_image)

                # Save the final image in PNG format
                export_path = os.path.join(export_dir, f"{filename}")
                final_image.save(export_path)
                print(f'Automate Design: Added design to {export_path}.')
        print('Automate Design: Successfully completed execution.')
    except Exception as e:
        print(f'Automate Design: Error occurred - {e}.')

automate_design()
