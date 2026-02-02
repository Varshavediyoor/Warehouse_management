import barcode
from barcode.writer import ImageWriter
from django.core.files import File
from io import BytesIO

def generate_barcode_image(code_text):
    CODE128 = barcode.get_barcode_class('code128')
    rv = BytesIO()
    code128 = CODE128(code_text, writer=ImageWriter())
    code128.write(rv)
    rv.seek(0)
    return rv
