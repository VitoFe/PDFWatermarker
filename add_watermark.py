from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from argparse import ArgumentParser
from PIL import Image
import io


def add_watermark(input_pdf, output_pdf, watermark_png, opacity, position, maxheight, offsetX, offsetY):
    with Image.open(watermark_png) as img:
        w_width, w_height = img.size
        alpha = Image.new('L', img.size, int(255 * opacity))
        img.putalpha(alpha)
        if maxheight > 0 and w_height > maxheight:
            scale_ratio = maxheight / w_height
            new_width = int(scale_ratio * w_width)
            resized_img = img.resize((new_width, maxheight))
            watermark_img = ImageReader(resized_img)
            w_width, w_height = resized_img.size
        else:
            watermark_img = ImageReader(img)

        with open(input_pdf, 'rb') as file:
            reader = PdfFileReader(file)
            writer = PdfFileWriter()

            for i in range(reader.getNumPages()):
                page = reader.getPage(i)
                width = page.mediaBox.getWidth()
                height = page.mediaBox.getHeight()
                if position == 'center':
                    x = (width - w_width) / 2
                    y = (height - w_height) / 2
                elif position == 'top-left':
                    x = 0 + offsetX
                    y = height - w_height + offsetY
                elif position == 'top-right':
                    x = width - w_width - offsetX
                    y = height - w_height + offsetY
                elif position == 'bottom-left':
                    x = 0 + offsetX
                    y = 0 + offsetY
                elif position == 'bottom-right':
                    x = width - w_width - offsetX
                    y = 0 + offsetY
                else:
                    raise ValueError("Invalid position specified. Must be one of: center, top-left, top-right, bottom-left, bottom-right")

                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(width, height))
                can.drawImage(watermark_img, int(x), int(y), mask='auto')
                can.save()

                packet.seek(0)
                overlay = PdfFileReader(packet).getPage(0)
                page.mergePage(overlay)

                writer.addPage(page)

            with open(output_pdf, 'wb') as out_file:
                writer.write(out_file)


if __name__ == '__main__':
    parser = ArgumentParser(description='Add a watermark to a PDF file')
    parser.add_argument('input', help='input PDF file path')
    parser.add_argument('output', help='output PDF file path')
    parser.add_argument('watermark', help='watermark PNG file path')
    parser.add_argument('--opacity', type=float, default=0.5, help='watermark opacity (default: 0.5)')
    parser.add_argument('--position', default='bottom-right', choices=['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'], help='where the watermark should be placed (default: bottom-right)')
    parser.add_argument('--maxheight', type=int, default=0, help='max height of the watermar (default: image height)')
    parser.add_argument('--offsetX', type=int, default=0, help='offset on the X axis (default: 0)')
    parser.add_argument('--offsetY', type=int, default=0, help='offset on the Y axis (default: 0)')
    args = parser.parse_args()

    add_watermark(args.input, args.output, args.watermark, args.opacity, args.position, args.maxheight, args.offsetX, args.offsetY)
