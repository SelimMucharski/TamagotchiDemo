from PIL import Image
import os
import sys

TARGET_SIZE = (100, 100)

def resize_pngs(input_dir):
    output_dir = os.path.join(input_dir, "out")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGBA")
                    img_resized = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                    img_resized.save(output_path, "PNG")

                print(f"OK: {filename}")

            except Exception as e:
                print(f"Błąd przy {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python resize.py <ścieżka_do_folderu>")
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print("Podana ścieżka nie jest folderem.")
        sys.exit(1)

    resize_pngs(folder)
