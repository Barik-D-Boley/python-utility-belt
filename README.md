# Python Utility Belt

A collection of local, standalone Python productivity scripts managed by a central runner (`run.py`).

## Quick Start & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/barik-d-boley/python-utility-belt.git
   cd python-utility-belt
   ```

2. **Run any tool using its shortcut:**
   ```bash
   python run.py <shortcut>
   ```
   *(For example: `python run.py pdf` or `python run.py qr`)*

`run.py` automatically checks whether all required Python packages are installed for that tool. If any are missing, it will prompt you to automatically install them before running.

## Available Tools

| Shortcut | Tool Name | Description | Size / Footprint | Primary Dependencies | Subdirectory |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pdf` | **PDF Trimmer** | Crop, slice, or extract specific page ranges from PDF files. | Lightweight (~1 MB) | `pypdf` | [`pdf_trimmer/`](./pdf_trimmer) |
| `bg` | **Image BG Remover** | Remove image backgrounds locally without sending data to external APIs. | Heavy (~500 MB+) | `rembg`, `onnxruntime-directml`, `Pillow`, `numpy` | [`img_bg_remover/`](./img_bg_remover) |
| `qr` | **QR Code Generator** | Generate custom, high-resolution QR codes from text or URLs. | Lightweight (~5 MB) | `qrcode`, `Pillow`, `numpy` | [`qr_code_generator/`](./qr_code_generator) |

## Detailed Tool Specifications

### 1. PDF Trimmer (`pdf`)
* **Summary:** Quickly extracts target page ranges or crops large PDF documents locally without uploading sensitive files to online converter sites.
* **Working Directory:** Files to be processed are placed in `pdf_trimmer/input/`, and generated output files export to `pdf_trimmer/output/`.
* **Footprint:** Very fast, minimal RAM usage.

### 2. Image Background Remover (`bg`)
* **Summary:** Uses local ML models to isolate subjects and strip backgrounds from image files. Uses DirectML GPU acceleration where available.
* **Working Directory:** Source images go into `img_bg_remover/input/`, and processed transparent PNGs land in `img_bg_remover/output/`.
* **Footprint:** Requires an initial model download (~170 MB) on first launch and larger execution memory.

### 3. QR Code Generator (`qr`)
* **Summary:** Generates clean, scannable QR code PNG images for URLs, Wi-Fi details, or plain text.
* **Working Directory:** Output QR code files are exported to `qr_code_generator/output/`.
* **Footprint:** Instant execution, lightweight footprint.

## Developer Guide: Adding a New Tool

Follow these steps to expand the repository with a new utility:

### 1. Folder Setup
Create a new directory containing your script, individual `requirements.txt`, and input/output folders with `.gitkeep` files:

```text
my_new_tool/
├── input/
│   └── .gitkeep
├── output/
│   └── .gitkeep
├── my_tool.py
├── requirements.txt
└── README.md
```

### 2. Update `TOOLS` in `run.py`
Open `run.py` and register your new script in the `TOOLS` registry dictionary using 2-space indentation:

```python
TOOLS = {
  ...
  "mytool": {
    "script": Path("my_new_tool/main.py"),
    "reqs": Path("my_new_tool/requirements.txt"),
    "modules": ["required_module_name"],
  },
}
```

### 3. Test Execution
Run `python run.py mytool` from the project root. `run.py` will verify directory paths, check dependencies, prompt for installation if necessary, and execute the script inside `my-new-tool/`.