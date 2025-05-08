from PIL import Image
import pyzbar.pyzbar as pyzbar

img = Image.open("temp_qrcodes/invite_1.png")
decoded = pyzbar.decode(img)
print(decoded[0].data.decode() if decoded else "No data found")

