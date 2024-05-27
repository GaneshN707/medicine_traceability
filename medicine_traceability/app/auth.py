import re
import qrcode
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

#                                             QRCode Generator                                            #
############################################################################################################
def generate_qr_code(qr_value, medicine_id, batch_no, manifacture_date):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(qr_value)
    qr.make(fit=True)

    # Create an image from the QR code instance
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # file_path = "static/img/qrcodes"
    # filename = f"{medicine_id}_{batch_no}_{manifacture_date}.png"  # You can modify the filename as needed
    # file_location = os.path.join(file_path, filename)

    # qr_image.save(file_location)  # Change the filename as needed
    # print(file_location)

    # Save the image to a BytesIO buffer
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")

    # Create an InMemoryUploadedFile from the buffer
    image_file = InMemoryUploadedFile(
        buffer, None, f"{medicine_id}_{batch_no}_{manifacture_date}.png", 'image/png', buffer.tell(), None
    )

    return image_file


#                                             Authenticate User                                            #
############################################################################################################
def name_valid(name):
    if all(char.isalpha() or char.isspace() for char in name) and len(name) > 1:
        return True
    else:
        return False

def password_valid(pass1):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, pass1, pass2):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif password_valid(pass1) == False:
        return "Password Should be in Proper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"

