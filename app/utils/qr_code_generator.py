import qrcode
from pathlib import Path

def generate_qr_code(data: str, output_path: str) -> str:
    """
    Generates a QR code for the given data and saves it to the specified output path.

    Args:
        data (str): The data to encode in the QR code.
        output_path (str): The full path (including filename) where the QR code image will be saved.

    Returns:
        str: Path to the saved QR code image.
    """
    img = qrcode.make(data)
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path

