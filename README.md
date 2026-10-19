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

### Manual Package Installation (Optional)
If you prefer to pre-install dependencies without using `run.py` auto-installation:
- Install a single tool's dependencies: `pip install .[pdf]`
- Install all tools' dependencies at once: `pip install .[all]`

## Available Tools

| Shortcut | Tool Name | Description | Size / Footprint | Primary Dependencies | Subdirectory |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pdf` | **PDF Trimmer** | Extract page ranges natively without file bloat or re-encoding. | Lightweight (~1 MB) | `pypdf` | [`pdf_trimmer/`](./pdf_trimmer) |
| `bg` | **Image BG Remover** | Remove image backgrounds locally without sending data to external APIs. | Heavy (~500 MB+) | `rembg`, `onnxruntime-directml`, `Pillow`, `numpy` | [`img_bg_remover/`](./img_bg_remover) |
| `qr` | **QR Code Generator** | Generate custom, high-resolution QR codes from text or URLs. | Lightweight (~5 MB) | `qrcode`, `Pillow`, `numpy` | [`qr_code_generator/`](./qr_code_generator) |

## Detailed Tool Specifications

### 1. PDF Trimmer (`pdf`)
- **Summary:** Natively extracts target page ranges without re-compressing pages or inflating file sizes (a common issue with "Print to PDF"), preserving original vector text, formatting, and document quality.
- **Working Directory:** Files to be processed are placed in `pdf_trimmer/input/`, and generated output files export to `pdf_trimmer/output/`.
- **Footprint:** Very fast, minimal RAM usage.

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
Create a new directory containing your script and input/output folders with `.gitkeep` files:

```text
my_new_tool/
├── input/
│   └── .gitkeep
├── output/
│   └── .gitkeep
├── main.py
└── README.md
```

### 2. Add Dependencies to `pyproject.toml`
Open `pyproject.toml` and add your package dependencies under `[project.optional-dependencies]`:

```toml
[project.optional-dependencies]
...
mytool = ["some-package>=1.0.0"]
```

### 3. Update `TOOLS` in `run.py`
Register the new script shortcut in `run.py`:

```python
TOOLS = {
  ...
  "mytool": {
    "script": Path("my_new_tool/main.py"),
    "extra": "mytool",
    "modules": ["some_package"],
  },
}
```

### 4. Test Execution
Run `python run.py mytool` from the project root. `run.py` will verify directory paths, check dependencies, prompt for installation if necessary, and execute the script inside `my_new_tool/`.