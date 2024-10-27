from pyicloud import PyiCloudService
import getpass
from datetime import datetime

# Authenticate with iCloud
apple_id = input("Enter your Apple ID: ")
password = getpass.getpass("Enter your password (input will be hidden): ")

api = PyiCloudService(apple_id, password)

# Handle two-factor authentication if enabled
if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received: ")
    result = api.validate_2fa_code(code)
    if not result:
        print("Failed to verify the security code.")
        exit(1)
    else:
        print("Successfully authenticated.")

elif api.requires_2sa:
    # Handle older two-step authentication
    print("Two-step authentication required.")
    devices = api.trusted_devices
    for i, device in enumerate(devices):
        device_name = device.get('deviceName', f'Device {i}')
        print(f"{i}: {device_name}")
    device_index = int(input("Select a device for authentication: "))
    device = devices[device_index]
    if not api.send_verification_code(device):
        print("Failed to send verification code.")
        exit(1)
    code = input("Enter the verification code you received: ")
    if not api.validate_verification_code(device, code):
        print("Failed to verify the code.")
        exit(1)

# Define file extensions to delete
extensions_to_delete = ['.mp4', '.heic', '.HEIC', '.jpeg', '.jpg', '.JPG']

# Fetch all photos
print("Fetching photo library...")
photos = api.photos.all

# Iterate over photos and delete matching files
print("Deleting specified file types (excluding files from 2024)...")
deleted_count = 0
skipped_count = 0

for photo in photos:
    photo_name = photo.filename
    photo_date = photo.created

    # Skip if photo is from 2024
    if photo_date.year == 2024:
        skipped_count += 1
        continue

    if any(photo_name.endswith(ext) for ext in extensions_to_delete):
        print(f"Deleting {photo_name} (Created on {photo_date.date()})")
        photo.delete()
        deleted_count += 1

print(f"\nDeletion complete. Total files deleted: {deleted_count}")
print(f"Total files skipped (from 2024): {skipped_count}")
