# Python Utility Belt

A collection of local, standalone Python productivity scripts managed by a central runner (`run.py`).

## Quick Start & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/barik-d-boley/python-utility-belt.git
cd python-utility-belt
```

2. **Run any tool using its shortcut or scaffold a new one:**
```bash
python run.py <shortcut>
```
*(For example: `python run.py pdft`, `python run.py pdfm`, or `python run.py new`)*

`run.py` automatically checks whether all required Python packages are installed for that tool. If any are missing, it will prompt you to automatically install them before running.

### Manual Package Installation (Optional)
If you prefer to pre-install dependencies without using `run.py` auto-installation:
- Install a single tool's dependencies: `pip install .[pdf-trim]` or `pip install .[pdf-merge]`
- Install all PDF dependencies: `pip install .[pdf]`
- Install all tools' dependencies at once: `pip install .[all]`

## Available Tools

| Shortcut | Tool Name | Description | Size / Footprint | Primary Dependencies | Subdirectory |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `bg` | **Image BG Remover** | Remove image backgrounds locally without sending data to external APIs. | Heavy (~500 MB+) | `rembg`, `onnxruntime-directml`, `Pillow`, `numpy` | [`img_bg_remover/`](./img_bg_remover) |
| `cite` | **Citation Cleaner** | Strip bracketed citations `[1]` from `.txt` and `.docx` files. | Lightweight (~2 MB) | `python-docx` | [`gemini_citation_remover/`](./gemini_citation_remover) |
| `pdfm` | **PDF Merger** | Merge PDFs and images natively, dynamically scaling images to fit page dimensions. | Lightweight (~5 MB) | `pypdf`, `Pillow`, `cryptography` | [`pdf_merger/`](./pdf_merger) |
| `pdft` | **PDF Trimmer** | Extract page ranges natively without file bloat or re-encoding. | Lightweight (~1 MB) | `pypdf`, `cryptography` | [`pdf_trimmer/`](./pdf_trimmer) |
| `ppm` | **PowerPoint Merger** | Cleanly merge multiple PowerPoint (`.pptx`) presentations into a single file. | Lightweight (~1 MB) | `pywin32` | [`powerpoint_merger/`](./powerpoint_merger) |
| `qr` | **QR Code Generator** | Generate custom, high-resolution QR codes from text or URLs. | Lightweight (~5 MB) | `qrcode`, `Pillow`, `numpy` | [`qr_code_generator/`](./qr_code_generator) |

## Developer Guide: Adding a New Tool

Automate new tool scaffolding using `scaffold.py` directly through `run.py`:

### 1. Run the Scaffold Generator
Run the generator from the project root directory:

```bash
python run.py new
```

Follow the interactive prompts:
- **Shortcut name** (e.g., `xyz`)
- **Display Name** (e.g., `XYZ Extractor`)
- **Folder Name** (e.g., `xyz_extractor`)
- **Short Description** (e.g., `Extracts specific data from files`)

### 2. Automated Repository Scaffold
`scaffold.py` creates the folder structure and registers your new tool across the project in alphabetical order:
- Creates `my_tool/main.py` with starter boilerplate using 2-space indents.
- Creates `my_tool/input/` and `my_tool/output/` subdirectories with `.gitkeep` files.
- Creates `my_tool/README.md` formatted to repository documentation standards.
- Creates `my_tool/CHECKLIST.txt` to track remaining manual steps.
- Updates `pyproject.toml` under `[project.optional-dependencies]` (and updates the `all` extra array).
- Updates `TOOLS` in `run.py`.
- Inserts a new row in the root `README.md` **Available Tools** table.

### 3. Complete the Post-Setup Checklist
Open `my_tool/CHECKLIST.txt` inside your new tool directory and complete the post-setup steps:
1. Write core script logic in `main.py`.
2. Add package dependencies to `pyproject.toml`.
3. Update module import names for dependency checking in `run.py`.
4. Update tool-level `README.md` with usage instructions and output examples.
5. Update dependency list and footprint column in root `README.md`.
6. Test with `python run.py <shortcut>`, commit via GitHub Desktop, and delete `CHECKLIST.txt`.