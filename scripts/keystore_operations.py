import subprocess
import os

def generate_keystore(keystore_name, key_alias, keystore_password, key_password):
    keytool_command = [
        'keytool',
        '-genkey',
        '-v',
        '-keystore', keystore_name,
        '-keyalg', 'RSA',
        '-keysize', '2048',
        '-validity', '1000',
        '-alias', key_alias,
        '-keypass', key_password,
        '-storepass', keystore_password
    ]
    subprocess.run(keytool_command)

def sign_app_with_keystore(app_name, keystore_name, key_alias, keystore_password, key_password):
    jarsigner_command = [
        'jarsigner',
        '-verbose',
        '-sigalg', 'SHA1withRSA',
        '-digestalg', 'SHA1',
        '-keystore', keystore_name,
        '-storepass', keystore_password,
        '-keypass', key_password,
        app_name, key_alias
    ]
    subprocess.run(jarsigner_command)

def align_apk(app_name):
    aligned_app_name = app_name.replace('.apk', '_signed.apk')

    zipalign_command = [
        'zipalign',
        '-v', '4',
        app_name,
        aligned_app_name
    ]

    try:
        # Run the zipalign command using subprocess
        subprocess.run(zipalign_command, check=True)
        os.remove(app_name)
    except subprocess.CalledProcessError as e:
        print(f"Error aligning APK: {e}")

def perform_keystore_operations(app_name):
    has_keystore = input("Do you have a keystore? (yes/no): ").lower() == 'yes'

    if has_keystore:
        keystore_name = input("Enter the path of your keystore file: ")
        key_alias = input("Enter key alias: ")
        keystore_password = input("Enter keystore password: ")
        key_password = input("Enter key password: ")
    else:
        create_new_keystore = input("Do you want to create a new keystore? (yes/no): ").lower() == 'yes'
    
        if create_new_keystore:
            keystore_name = input("Enter new keystore name: ")
            key_alias = input("Enter key alias: ")
            keystore_password = input("Enter keystore password: ")
            key_password = input("Enter key password: ")
        
            generate_keystore(keystore_name, key_alias, keystore_password, key_password)
        else:
            print("No keystore will be created. Exiting...")
            exit()
    
    sign_app_with_keystore(app_name, keystore_name, key_alias, keystore_password, key_password)

    align_apk(app_name)


