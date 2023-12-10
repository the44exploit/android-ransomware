
import os

def change(app_name, mipmap_folder, new_app_name):
    apktool_cmd = "apktool"

    decode_cmd = f"{apktool_cmd} d {app_name} -o decoded_apk"

    os.system(decode_cmd)
    
    try:
        manifest_path = "decoded_apk/AndroidManifest.xml"
        with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
            manifest_content = manifest_file.read()

        manifest_content = manifest_content.replace("android:label=\"@string/app_name\"", f"android:label=\"{new_app_name}\"")

        with open(manifest_path, 'w', encoding='utf-8') as manifest_file:
            manifest_file.write(manifest_content)
            
        os.system("rm -r decoded_apk/res/mipmap-*")
        
        replace_cmd = f"cp -r {mipmap_folder}/* decoded_apk/res/"
        os.system(replace_cmd)

        os.system(f"rm -r {app_name}")

        build_cmd = f"{apktool_cmd} b decoded_apk -o {app_name}"

        os.system(build_cmd)

        os.system("rm -r decoded_apk")
        os.system(f"rm -r {mipmap_folder}")
    except:
        pass

if __name__ == "__main__":
    app_name = input("Enter the name of the APK file: ")
    mipmap_folder = input("Enter the path to the new mipmap folder: ")

    change(app_name, mipmap_folder)

    print("App icon changed successfully!")
