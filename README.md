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
| `bg` | **Image BG Remover** | Remove image backgrounds locally without sending data to external APIs. | Heavy (~500 MB+) | `rembg`, `onnxruntime-directml`, `Pillow`, `numpy` | [`img_bg_remover/`](./img_bg_remover) |
| `cite` | **Citation Cleaner** | Strip bracketed citations `[1]` from `.txt` and `.docx` files. | Lightweight (~2 MB) | `python-docx` | [`citation_cleaner/`](./citation_cleaner) |
| `pdf` | **PDF Trimmer** | Extract page ranges natively without file bloat or re-encoding. | Lightweight (~1 MB) | `pypdf` | [`pdf_trimmer/`](./pdf_trimmer) |
| `ppm` | **PowerPoint Merger** | Cleanly merge multiple PowerPoint (`.pptx`) presentations into a single file. | Lightweight (~1 MB) | `pywin32` | [`powerpoint_merger/`](./powerpoint_merger) |
| `qr` | **QR Code Generator** | Generate custom, high-resolution QR codes from text or URLs. | Lightweight (~5 MB) | `qrcode`, `Pillow`, `numpy` | [`qr_code_generator/`](./qr_code_generator) |


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

> **Importing Existing Repositories:** If you clone or copy an existing GitHub repository into this project as a tool, delete its hidden `.git` folder so Git and GitHub Desktop track it as a standard directory rather than an isolated submodule:
>
> ```powershell
> Remove-Item -Recurse -Force .\<folder_name>\.git
> ```

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

### 4. Update Root Documentation
Document the new tool in the root `README.md` so users can discover it:
- Add a new row to the **Available Tools** table with its shortcut, name, description, size footprint, primary dependencies, and subdirectory link.
- Add a numbered entry under **Detailed Tool Specifications** detailing its purpose, input/output paths, and performance characteristics.

### 5. Test Execution
Run `python run.py mytool` from the project root. `run.py` will verify directory paths, check dependencies, prompt for installation if necessary, and execute the script inside `my_new_tool/`.