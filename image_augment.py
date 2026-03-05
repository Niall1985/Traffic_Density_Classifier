import os
from PIL import Image, ImageOps

input_root = "Final_Dataset"
output_root = "Augmented_Dataset"

for root, dirs, files in os.walk(input_root):
    relative_path = os.path.relpath(root, input_root)
    output_dir = os.path.join(output_root, relative_path)
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(root, file)
            img = Image.open(input_path)

            if img.mode == "RGBA":
                img = img.convert("RGB")
                
            output_original = os.path.join(output_dir, file)
            img.save(output_original)

            mirrored = ImageOps.mirror(img)

            name, ext = os.path.splitext(file)
            mirrored_name = f"{name}_morror{ext}"

            output_mirror = os.path.join(output_dir, mirrored_name)
            mirrored.save(output_mirror)

print("Augementation Done")