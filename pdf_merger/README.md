# PDF Merger Utility

A lightweight Python command-line utility to merge multiple PDF files—including AES-encrypted documents like CAD certificates—from a designated inputs folder into a single output document.

## Prerequisites

* Python 3.8 or higher
* `pip` package manager

## Installation

1. Clone or download this repository.
2. Ensure you have an `inputs` folder in the root directory. Place the PDF files you want to merge inside this folder (files will be merged in alphabetical/numerical order, e.g., `01_cswa_certificate.pdf`, `02_autodesk_certificate.pdf`).
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script from your terminal:

```bash
python merge_pdfs.py
```

*(Note: On some Windows setups, you may need to use `py merge_pdfs.py`)*

2. Check the console output:

* **Success**: `Success! Merged file saved to: merged_output.pdf`
* **Error**: `Error: 'inputs' folder not found at ...` or `No PDF files found in 'inputs/'.`

The final merged file `merged_output.pdf` will appear in your project root folder.