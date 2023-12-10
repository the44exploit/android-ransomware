

from scripts.change_app_icon import change
from scripts.AppIconGenerator import generate_icons
from scripts.decrypter import xyz
from scripts.keystore_operations import perform_keystore_operations
import sys
import base64
import string
import os
import shutil
import random
import zipfile
import signal

GREEN = "\033[32m"
WHITE = '\033[0m'
RED = '\033[91m'

print("""
\033[1;96m
*******************************
        The 44 Exploit
*******************************

\033[1;92mYouTube: \033[0;94mhttps://www.youtube.com/@deepkul-roy
\033[1;92mGitHub:  \033[0;94mhttps://github.com/the44exploit

*******************************
\033[0m
""")


print(GREEN, end='')

def extract_apk(apk_path, output_directory):
    with zipfile.ZipFile(apk_path, "r") as zip_ref:
        zip_ref.extractall(output_directory)

def save_to_file(data, filename):
    with open(filename, "w") as file:
        file.write(data)

def repack_apk(input_directory, output_apk):
    with zipfile.ZipFile(output_apk, "w") as zipf:
        for root, _, files in os.walk(input_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_directory)
                zipf.write(file_path, arcname)

def x():
    return base64.urlsafe_b64encode(bytes([random.randint(0, 255) for _ in range(32)]))

def k(length=5):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def a(x, n):
    y = '|'.join(str(ord(c) ^ n_byte) for c, n_byte in zip(x, n))

    z = k()
    w = base64.urlsafe_b64encode(f"{n.decode()}{z}{y}".encode()).decode()
    return f"{z}{w}"
    
def delete_directories(directory_paths):
    for directory_path in directory_paths:
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
            except Exception as e:
                print(f"Error deleting directory '{directory_path}': {e}")
            
def signal_handler(sig, _):
    print()
    delete_directories(["output_apk","images","decoded_apk"])
    
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

delete_directories(["output_apk","images","decoded_apk"])

def main():
    choice = input(GREEN + "Do you want to create an encrypter or a decrypter? (encrypt/decrypt): " + WHITE)

    if choice.lower() == "decrypt":
        xyz()
        sys.exit()
    original_apk_path = "app/app.apk"

    extraction_directory = "output_apk"

    os.makedirs(extraction_directory, exist_ok=True)

    extract_apk(original_apk_path, extraction_directory)

    password = input(GREEN + "Enter the encryption key: " + WHITE)
    if password == "":
        sys.exit()

    print(GREEN + "Enter your message. Press Enter on an empty line to finish." + WHITE)
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    message = '\n'.join(lines)

    new_apk_path = input(GREEN + "Please enter the desired output filename (e.g., app_output.apk): " + WHITE)

    n = x()

    password_file_path = os.path.join(extraction_directory, "res/raw/a.txt")
    save_to_file(a(password, n), password_file_path)

    message_file_path = os.path.join(extraction_directory, "res/raw/b.txt")
    save_to_file(message, message_file_path)


    repack_apk(extraction_directory, new_apk_path)

    try:
        shutil.rmtree(extraction_directory)
    except Exception as e:
        print(f"{RED}Failed to delete extraction directory: {e}{WHITE}")

    print(f"The APK has been saved to {GREEN}{new_apk_path}{WHITE}")
    
    directory_path = "/data/data/com.termux/files/home"
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print()
        user_input = input(GREEN + "Do you want to change the app icon and app name? (yes/no): " + WHITE).lower()
        if user_input == "yes":
            input_image_path = input(GREEN + "Enter the path to your input image: " + WHITE)
            new_app_name = input(GREEN + "Enter the new app name: " + WHITE)
            images = "images"
            os.makedirs(images, exist_ok=True)
            generate_icons(input_image_path, images)
            change(new_apk_path, images, new_app_name)
    print()
    proceed_with_signing = input(GREEN + "Do you want to sign the APK? (yes/no): " + WHITE).lower()
    if proceed_with_signing == 'yes':
        print(GREEN)
        perform_keystore_operations(new_apk_path)

    print(RED)
    print("Exiting...")

if __name__ == "__main__":
    main()
