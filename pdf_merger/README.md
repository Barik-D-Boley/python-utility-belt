# PDF Merger

A lightweight Python command-line utility to merge multiple PDF files and images into a single document natively while automatically resizing images to match PDF page dimensions.

## Prerequisites

- Python 3.8 or higher
- `pip` package manager

## Usage

1. Place your target PDF(s) and image(s) inside the `pdf_merger/input/` folder.
2. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py pdfm
```

3. Enter the output filename when prompted (or press **Enter** to use the default `merged_output.pdf`):

```text
Enter output filename (default: merged_output.pdf):
> 

Merging files:
  - Adding PDF: Signed_E611_Form.pdf
  - Resizing & Adding Image: IDA_Rexburg.PNG
  - Resizing & Adding Image: Parking_Receipt.jpg
  - Resizing & Adding Image: Rexburg_IDA.PNG
```

*(Note: PDFs will automatically be placed first in alphabetical order, followed by images in alphabetical order).*

4. A native File Explorer save window will open pre-focused on the project directory with your chosen filename pre-filled. Confirm or adjust the destination and click **Save**.

5. Check the console output:

- **Success**: `Success! Merged file saved to: '/path/to/output/merged_output.pdf'`
- **Cancelled**: `Save operation cancelled.`
- **Error**: `Error: 'input' folder not found at ...` (or specific error message)