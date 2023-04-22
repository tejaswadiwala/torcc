from PIL import Image

# Set up the design and clothing images
design_path = "automate_design/designs/design_1.png"
clothing_path = "automate_design/clothing_images/navy_classic_tee.png"

design_image = Image.open(design_path).convert("RGBA")
clothing_image = Image.open(clothing_path)

# Resize the design image to fit on the clothing image
design_size = (int(clothing_image.size[0] / 2), int(clothing_image.size[1] / 2))
design_image = design_image.resize(design_size)

# Paste the clothing image onto the canvas
final_image = clothing_image.copy()

# Paste the design image onto the clothing image
design_position = (int((clothing_image.size[0] - design_size[0]) / 2), int((clothing_image.size[1] - design_size[1]) / 2))
final_image.paste(design_image, design_position, design_image)

# Save the final image in PNG format
final_image.save("automate_design/exports/mockup.png")
