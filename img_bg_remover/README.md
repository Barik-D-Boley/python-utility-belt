# Image Background Remover

A Python command-line utility with native file dialog support that automatically removes backgrounds from images using either AI models or auto-color keying.

## Prerequisites

* Python 3.8 or higher
* `pip` package manager
* `tkinter` (included with standard Python installers on Windows/macOS; Linux users may need `python3-tk`)

## Usage

1. Place your target image(s) (`.jpg`, `.jpeg`, `.png`, `.webp`) inside the `img_bg_remover/input/` folder.
2. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py bg
```

3. Follow the on-screen prompts to select your processing mode and settings:

```text
Select Removal Method:
  1. AI Model (Best for photos, complex subjects, objects)
  2. Auto-Color Keying (Best for CAD renders with solid flat backgrounds)

Enter choice (1 or 2) [Default is 1]: 1

Select AI Precision Level:
  1. Standard (Fastest - u2net)
  2. High Detail (Better for fine meshes/holes - isnet-general-use)
  3. Ultra Detail (Highest accuracy - birefnet-general)

Enter choice (1, 2, or 3) [Default is 2]: 2

Initializing isnet-general-use AI model...
Checking for NVIDIA GPU... Unavailable (no NVIDIA hardware or drivers).
Checking for Apple GPU... Unavailable (package not installed).
Checking for DirectML GPU (AMD/Intel)... Available and active!

AI Model loaded successfully!
```

4. Choose single image save or batch processing:

* **Single Image Processing**: If only one image exists (or if selected from the list when multiple exist), a native File Explorer save window will open allowing you to choose the target location and filename.
* **Batch Processing**: Automatically processes every image in the `img_bg_remover/input/` folder and saves the results to the `output/` folder with `_nobg.png` appended.

```text
Found 3 images in the 'input' folder.
1. Process ALL images automatically to the 'output' folder
2. Select ONE image from list and choose where to save it

Enter 1 or 2: 1

Batch processing 3 images to 'output'...

Processing (AI): render1.png...
Success! Saved to: output/render1_nobg.png

Processing (AI): photo2.jpg...
Success! Saved to: output/photo2_nobg.png

Batch processing complete!
```

5. Check the console output:

* **Success**: `Success! Saved to: <path>`
* **Cancelled**: `Save cancelled.`
* **Error**: `No images found in the 'input' folder.` (Prompts you to add images and re-run).