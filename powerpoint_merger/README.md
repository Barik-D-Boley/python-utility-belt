# PowerPoint Merger

A lightweight Python command-line utility to cleanly merge multiple PowerPoint (`.pptx`) presentations into a single file without corrupting slide layouts or formatting.

## Prerequisites

- Python 3.8 or higher
- Microsoft PowerPoint installed (Windows)

## Usage

1. Place all `.pptx` files you wish to merge into the `powerpoint_merger/input/` directory.

2. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py ppm
```

3. Enter the desired output file name or press Enter for default (`merged_output.pptx`):

```text
Enter output file name (press Enter for default 'merged_output.pptx'): MET231_Weeks_1-6
```

4. Check the console output:

- **Success**: `Done! Merged file saved to 'C:\...\powerpoint_merger\output\MET231_Weeks_1-6.pptx'.`
- **Error**: `No .pptx files found in 'C:\...\powerpoint_merger\input'.`

Merged presentations automatically save to the `powerpoint_merger/output/` folder.