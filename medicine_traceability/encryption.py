from cryptography.fernet import Fernet
import json

# Generate a key
key = Fernet.generate_key()

# Create a Fernet cipher using the key
cipher_suite = Fernet(key)

# Sample dictionary
data = {
    "medicine_id": "medicine_id",
    "medicine_name": "medicine_name",
    "batch_no": "batch_no",
    "Medicine_Used": "Medicine_Used",
    "manifacture_date": "manifacture_date",
    "expire_date": "expire_date",
    "medice_mrp": "medice_mrp",
}
    
# Convert dictionary to bytes
data_bytes = json.dumps(data).encode()

# Encrypt the data
encrypted_data = cipher_suite.encrypt(data_bytes)

qr_value = str(cipher_suite) + "#######################" + str(encrypted_data)

# Decrypt the data
decrypted_data = cipher_suite.decrypt(encrypted_data)

# Convert bytes back to dictionary
decrypted_dict = json.loads(decrypted_data.decode())

print("Original Data: ", data)
print("Encrypted Data: ", encrypted_data)
print("Decrypted Data: ", decrypted_dict)
print("QR Code: ", qr_value)
