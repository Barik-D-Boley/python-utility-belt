# QR Code Generator

A lightweight Python command-line utility to generate permanent, static QR code images from any web link or URL.

## Prerequisites

* Python 3.8 or higher
* `pip` package manager

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script from your terminal:

```bash
python generate_qr.py
```

2. Enter your URL when prompted:

```text
Provide the url: https://github.com/Barik-D-Boley
```

3. Check the console output:

* **Success**: `Success: QR code created and saved as 'qr.png'.`
* **Error**: `Error: No URL was provided.` (or specific error message)

The output file `qr.png` will appear in your project root folder.