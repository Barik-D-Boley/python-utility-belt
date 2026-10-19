# PDF Page Extractor

A lightweight Python command-line utility to extract and trim specific pages from PDF files natively without rasterizing text or inflating file sizes.

## Prerequisites

* Python 3.8 or higher
* `pip` package manager

## Usage

1. Place your target PDF(s) inside the `pdf_trimmer/input/` folder.
2. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py pdf
```

3. Select your PDF (if multiple exist), enter your page selections, and enter the file name:

```text
Multiple PDFs found in the 'input' folder:

1. textbook.pdf
2. sample_reading.pdf

Select a PDF number to process:
> 1
Selected: 'textbook.pdf'
Success! The document has 25 pages.

Enter the pages you want to keep (e.g., 17-19, 13, 18, 21):
> 17-19

Extracting 3 pages...

Opening Save window...

Enter the name of the file:
> textbook_trimmed
```

*(Note: If only one PDF is present in `pdf_trimmer/input/`, it will automatically select it without prompting for a number).*

4. A native File Explorer save window will open pre-focused on the root directory with `textbook_trimmed.pdf` pre-filled. Confirm or adjust the destination and click **Save**.

5. Check the console output:

* **Success**: `Done! Saved natively to: '/path/to/output/textbook_trimmed.pdf'`
* **Cancelled**: `Save cancelled by user. Exiting.`
* **Error**: `Error: No PDF files found in the 'input' folder.` (or specific error message)