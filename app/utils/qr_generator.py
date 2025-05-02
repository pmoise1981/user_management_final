import qrcode
from pathlib import Path

def generate_qr_code(data: str, output_path: str) -> str:
    """
    Generate a QR code image from the given data and save it to the specified path.

    :param data: The data to encode in the QR code.
    :param output_path: The file path to save the generated QR code image.
    :return: Path to the saved QR code image.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(output_file))  # ← Convert Path to string

    return str(output_file)

