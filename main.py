import qrcode
import svgwrite
from PIL import Image
import base64
from io import BytesIO

def generate_vector_svg_qr_with_logo(data, logo_path, output_path, qr_size=1000, logo_size_ratio=0.2):
    # Generate QR code matrix directly
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the SVG QR code (vector format)
    qr_matrix = qr.modules
    cell_size = qr_size / len(qr_matrix)  # Calculate cell size dynamically
    dwg = svgwrite.Drawing(output_path, size=(qr_size, qr_size))
    dwg.add(dwg.rect(insert=(0, 0), size=(qr_size, qr_size), fill='white'))  # Background

    for y, row in enumerate(qr_matrix):
        for x, cell in enumerate(row):
            if cell:
                dwg.add(dwg.rect(insert=(x * cell_size, y * cell_size), size=(cell_size, cell_size), fill='black'))

    # Process the logo
    logo = Image.open(logo_path)
    logo_size = int(qr_size * logo_size_ratio)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Convert the logo to Base64 for embedding
    logo_buffer = BytesIO()
    logo.save(logo_buffer, format="PNG")
    logo_base64 = base64.b64encode(logo_buffer.getvalue()).decode()

    # Embed the logo as an image in the center of the QR code
    logo_x = (qr_size - logo_size) / 2
    logo_y = (qr_size - logo_size) / 2
    dwg.add(dwg.image(href=f"data:image/png;base64,{logo_base64}", insert=(logo_x, logo_y), size=(logo_size, logo_size)))

    # Save the SVG file
    dwg.save()
    print(f"High-quality vector SVG QR code with logo saved to {output_path}")

# Example usage
data = "https://example.com"
logo_path = "logo.jpg"       # Path to your logo
output_path = "qr_with_logo.svg"  # Output path for the QR code
generate_vector_svg_qr_with_logo(data, logo_path, output_path)
