import os
import argparse
from PIL import Image, ImageFile
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

ImageFile.LOAD_TRUNCATED_IMAGES = True

def resize_image(image_path, max_size_kb):
    try:
        img = Image.open(image_path)
        img_format = img.format

        if os.path.getsize(image_path) <= max_size_kb * 1024:
            return

        quality = 85
        while os.path.getsize(image_path) > max_size_kb * 1024 and quality > 10:
            img.save(image_path, format=img_format, quality=quality)
            quality -= 5
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_directory(directory, max_size_kb=200):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png')):
                image_path = os.path.join(root, file)
                image_paths.append((image_path, max_size_kb))

    with Pool(cpu_count()) as pool:
        list(tqdm(pool.imap_unordered(resize_image_star, image_paths), total=len(image_paths)))

def resize_image_star(args):
    return resize_image(*args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images in a directory to be under a specified size while maintaining aspect ratio.")
    parser.add_argument('directory', type=str, help='Path to the target directory')
    parser.add_argument('--max_size_kb', type=int, default=200, help='Maximum size of the image in KB (default: 200KB)')

    args = parser.parse_args()
    process_directory(args.directory, args.max_size_kb)
