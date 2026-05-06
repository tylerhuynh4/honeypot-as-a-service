import os
import shutil
from datetime import datetime
from cryptography.fernet import Fernet

LOG_FILE = 'honeypot.log'
ARCHIVE_DIR = 'log_archive'
KEY_FILE = 'secret.key'

# key mgmt

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    print(f"Key saved to {KEY_FILE} — back this up securely")

def load_key():
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("No secret.key found — run generate_key() first")
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# encryption

def encrypt_log(log_path, key):
    f = Fernet(key)
    with open(log_path, 'rb') as file:
        data = file.read()
    encrypted = f.encrypt(data)
    return encrypted

def decrypt_log(encrypted_path, key):
    f = Fernet(key)
    with open(encrypted_path, 'rb') as file:
        data = file.read()
    decrypted = f.decrypt(data)
    return decrypted.decode()

# archive

def archive_log():
    if not os.path.exists(LOG_FILE):
        print("No log file found, nothing to archive")
        return

    if os.path.getsize(LOG_FILE) == 0:
        print("Log file is empty, skipping archive")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    key = load_key()
    encrypted = encrypt_log(LOG_FILE, key)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f"honeypot_{timestamp}.log.enc"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)

    with open(archive_path, 'wb') as f:
        f.write(encrypted)

    print(f"Log archived and encrypted: {archive_path}")

    # clear the live log after archiving
    open(LOG_FILE, 'w').close()
    print("Live log cleared")

    # Upload S3 creds here
    # import boto3
    # s3 = boto3.client('s3')
    # bucket_name = 'your-bucket-name-here'
    # s3.upload_file(archive_path, bucket_name, archive_name)
    # print(f"Uploaded {archive_name} to s3://{bucket_name}")

def read_archive(archive_name):
    key = load_key()
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)
    decrypted = decrypt_log(archive_path, key)
    print(decrypted)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python archive_logs.py genkey     — generate encryption key")
        print("  python archive_logs.py archive    — encrypt and archive log")
        print("  python archive_logs.py read <file> — decrypt and read an archive")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'genkey':
        generate_key()
    elif command == 'archive':
        archive_log()
    elif command == 'read':
        if len(sys.argv) < 3:
            print("Usage: python archive_logs.py read <filename>")
            sys.exit(1)
        read_archive(sys.argv[2])
    else:
        print(f"Unknown command: {command}")