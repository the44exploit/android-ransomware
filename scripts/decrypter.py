import os
from scripts.keystore_operations import perform_keystore_operations
from scripts.change_app_icon import change
from scripts.AppIconGenerator import generate_icons
import shutil
import zipfile
        
GREEN = "\033[32m"
WHITE = '\033[0m'
RED = '\033[91m'
        
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
                

def xyz():
    decryption_key = input(GREEN + "Enter the decryption key: " + WHITE)
    output = input(GREEN + "Please enter the desired output filename (e.g., app_output.apk): " + WHITE)

    apk_path = "app/app2.apk"
    extraction_directory = "decrypt_apk"
    
    os.makedirs(extraction_directory, exist_ok=True)

    extract_apk(apk_path, extraction_directory)

    decryption_key_file_path = os.path.join(extraction_directory, "res/raw/a.txt")
    save_to_file(decryption_key, decryption_key_file_path)

    repack_apk(extraction_directory, output)
    try:
        shutil.rmtree(extraction_directory)
    except Exception as e:
        print(f"{RED}Failed to delete extraction directory: {e} {WHITE}")

    print(f"The APK has been saved to {GREEN}{output}{WHITE}")
    
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
            change(output, images, new_app_name)
    print()
    proceed_with_signing = input(GREEN + "Do you want to sign the APK? (yes/no): " + WHITE).lower()
    if proceed_with_signing == 'yes':
        print(GREEN)
        perform_keystore_operations(output)
    print (RED)
    print("Exiting...")
