# QR Code Generator

A lightweight Python command-line utility to generate permanent, static QR code images from any web link or URL.

## Prerequisites

* Python 3.8 or higher
* `pip` package manager

## Usage

1. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py qr
```

2. Enter your URL when prompted:

```text
Provide the url: https://github.com/Barik-D-Boley
```

3. Enter the file name or press enter to name it qr.png
```text
Enter file name (press Enter for default 'qr.png'): name
```

4. Check the console output:

* **Success**: `Success: QR code created and saved to 'output\name.png'.`
* **Error**: `Error: No URL was provided.` (or specific error message)

Generated QR codes automatically save to the `output/` folder.