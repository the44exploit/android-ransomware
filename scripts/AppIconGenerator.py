


import os
try:
    from PIL import Image
except ImportError:
    pass

RED = '\033[91m'

def resize_image(input_path, output_path, size):
    original_image = Image.open(input_path)
    width, height = original_image.size
    aspect_ratio = height/width
    new_height = int(size * aspect_ratio)
    resized_image = original_image.resize((size, new_height))
    resized_image.save(output_path)

def create_mipmap_folders(output_folder):
    resolutions = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']

    for resolution in resolutions:
        folder_path = os.path.join(output_folder, f'mipmap-{resolution}')
        os.makedirs(folder_path, exist_ok=True)

def copy_to_mipmap_folders(input_image_path, output_folder):
    resolutions = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']

    for resolution in resolutions:
        output_path = os.path.join(output_folder, f'mipmap-{resolution}', 'ic_launcher.png')

        round_output_path = os.path.join(output_folder, f'mipmap-{resolution}', 'ic_launcher_round.png')

        size = get_size_for_resolution(resolution)

        resize_image(input_image_path, output_path, size)
        resize_image(input_image_path, round_output_path, size)

def get_size_for_resolution(resolution):
    if resolution == 'mdpi':
        return 48
    elif resolution == 'hdpi':
        return 72
    elif resolution == 'xhdpi':
        return 96
    elif resolution == 'xxhdpi':
        return 144
    elif resolution == 'xxxhdpi':
        return 192
    else:
        return 96

def generate_icons(input_image_path, output_folder):
    try:
        create_mipmap_folders(output_folder)
        copy_to_mipmap_folders(input_image_path, output_folder)
    except Exception as e:
        print(RED + "Oops! There was an error generating the images.")

if __name__ == "__main__":
    input_image_path = "path_to_your_input_image.png"
    output_folder = "images"
    generate_icons(input_image_path, output_folder)
