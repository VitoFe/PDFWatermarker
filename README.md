# PDFWatermarker 📑
Add a watermark to a PDF file using Python. The script uses the PyPDF2 and reportlab libraries to read and write PDF files, and PIL to read and modify the watermark image.

### Dependencies
You can install the required libraries using pip: `pip install PyPDF2 reportlab pillow`

### Usage
`python add_watermark.py input_pdf output_pdf watermark_png [--opacity OPACITY] [--position POSITION] [--maxheight MAXHEIGHT] [--offsetX OFFSETX] [--offsetY OFFSETY]`

where:
- `input_pdf`: path to the input PDF file.
- `output_pdf`: path to the output PDF file with the watermark added.
- `watermark_png`: path to the watermark image file (in PNG format).
- `--opacity`: opacity of the watermark (default is 0.5).
- `--position`: position of the watermark (default is 'bottom-right').
- `--maxheight`: maximum height of the watermark (default is the original height of the image).
- `--offsetX`: offset on the X-axis of the watermark placement (default is 0).
- `--offsetY`: offset on the Y-axis of the watermark placement (default is 0).

The position argument can take one of the following values: 'center', 'top-left', 'top-right', 'bottom-left', or 'bottom-right'.
