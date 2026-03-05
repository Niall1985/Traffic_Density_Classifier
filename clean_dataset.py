import os
import random

DATASET_PATH = "Final_Dataset/training"

classes = ["High", "Low", "Medium"]

class_counts = {}

for class_name in classes:
    class_path = os.path.join(DATASET_PATH, class_name)
    images = os.listdir(class_path)
    class_counts[class_name] = len(images)

print("Original class counts:")
for k, v in class_counts.items():
    print(k, ":", v)

min_count = min(class_counts.values())
print("\nMinimum class count:", min_count)

for class_name in classes:
    class_path = os.path.join(DATASET_PATH, class_name)
    images = os.listdir(class_path)

    if len(images) > min_count:
        images_to_remove = random.sample(images, len(images) - min_count)

        for img_name in images_to_remove:
            img_path = os.path.join(class_path, img_name)
            os.remove(img_path)

        print(f"Undersampled {class_name}: removed {len(images_to_remove)} images")

print("\nDataset is now balanced.")