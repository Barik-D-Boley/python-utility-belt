import os
import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import warnings
import numpy as np
from PIL import Image
from rembg import remove, new_session
import onnxruntime as ort

# Mute ONNX internal log chatter and Python warning banners
warnings.filterwarnings("ignore")
ort.set_default_logger_severity(3)  # 3 = Error level (suppresses provider warnings)

# Helper class to suppress underlying C++ stderr output (DLL load errors)
class SuppressStderr:
  def __enter__(self):
    self.errnull_file = open(os.devnull, 'w')
    self.old_stderr_fileno = os.dup2(2, self.errnull_file.fileno())
    self.old_stderr = sys.stderr
    sys.stderr = self.errnull_file
    return self

  def __exit__(self, *_):
    sys.stderr = self.old_stderr
    os.dup2(self.old_stderr_fileno, 2)
    os.close(self.old_stderr_fileno)
    self.errnull_file.close()

def process_image_ai(input_path, output_path, session):
  print(f"\nProcessing (AI): {Path(input_path).name}...")
  img = Image.open(input_path)
  output = remove(img, session=session)
  output.save(output_path)
  print(f"Success! Saved to: {output_path}")

def process_image_color(input_path, output_path, threshold=35):
  print(f"\nProcessing (Color Keying): {Path(input_path).name}...")
  img = Image.open(input_path).convert("RGBA")
  data = np.array(img)

  bg_color = data[0, 0, :3].astype(float)
  print(f"Auto-detected background RGB: {tuple(bg_color.astype(int))}")

  rgb = data[:, :, :3].astype(float)
  color_distance = np.sqrt(np.sum((rgb - bg_color) ** 2, axis=2))

  transparent_mask = color_distance <= threshold
  data[transparent_mask, 3] = 0

  output_img = Image.fromarray(data)
  output_img.save(output_path)
  print(f"Success! Saved to: {output_path}")

def run_processing(input_path, output_path, mode, config):
  if mode == 'ai':
    process_image_ai(input_path, output_path, config['session'])
  else:
    process_image_color(input_path, output_path, config['threshold'])

def batch_process(input_dir, output_dir, images, mode, config):
  print(f"\nBatch processing {len(images)} images to '{output_dir}'...")
  output_dir.mkdir(parents=True, exist_ok=True)
  
  for img_path in images:
    out_path = output_dir / f"{img_path.stem}_nobg.png"
    run_processing(img_path, out_path, mode, config)
    
  print("\nBatch processing complete!")

def get_save_path(root, initial_name):
  root.deiconify()
  root.attributes('-topmost', True)
  root.focus_force()
  save_path = filedialog.asksaveasfilename(
    parent=root,
    title="Save image as...",
    defaultextension=".png",
    initialfile=initial_name,
    filetypes=[("PNG Image", "*.png")]
  )
  root.withdraw()
  return save_path

def select_image_from_list(images):
  print("\nAvailable images in 'input' folder:")
  for i, img_path in enumerate(images, start=1):
    print(f"  {i}. {img_path.name}")
    
  while True:
    choice = input(f"\nEnter image number (1-{len(images)}): ").strip()
    if choice.isdigit():
      index = int(choice) - 1
      if 0 <= index < len(images):
        return images[index]
    print("Invalid choice. Please enter a valid number from the list.")

def process_selected_image(root, images, mode, config):
  selected_img = select_image_from_list(images)
  save_path = get_save_path(root, f"{selected_img.stem}_nobg.png")
  
  if save_path:
    run_processing(selected_img, save_path, mode, config)
  else:
    print("Save cancelled.")

def has_nvidia_gpu():
  """Checks if an NVIDIA GPU driver exists on Windows."""
  if sys.platform == "win32":
    system_root = os.environ.get("SystemRoot", r"C:\Windows")
    return os.path.exists(os.path.join(system_root, "System32", "nvcuda.dll"))
  return True

def setup_method():
  print("\nSelect Removal Method:")
  print("  1. AI Model (Best for photos, complex subjects, objects)")
  print("  2. Auto-Color Keying (Best for CAD renders with solid flat backgrounds)")
  
  method = input("\nEnter choice (1 or 2) [Default is 1]: ").strip()
  
  if method == '2':
    threshold_input = input("\nEnter color sensitivity threshold (10-50) [Press Enter for default 35]: ").strip()
    threshold = int(threshold_input) if threshold_input.isdigit() else 35
    return 'color', {'threshold': threshold}
  else:
    print("\nSelect AI Precision Level:")
    print("  1. Standard (Fastest - u2net)")
    print("  2. High Detail (Better for fine meshes/holes - isnet-general-use)")
    print("  3. Ultra Detail (Highest accuracy - birefnet-general)")
    
    models = {
      '1': ('u2net', 'Standard'),
      '2': ('isnet-general-use', 'High Detail'),
      '3': ('birefnet-general', 'Ultra Detail')
    }
    
    choice = input("\nEnter choice (1, 2, or 3) [Default is 2]: ").strip()
    model_code = models.get(choice, ('isnet-general-use', 'High Detail'))[0]
    
    print(f"\nInitializing {model_code} AI model...")

    hardware_options = [
      ('CUDAExecutionProvider', 'NVIDIA GPU'),
      ('CoreMLExecutionProvider', 'Apple GPU'),
      ('DirectMLExecutionProvider', 'DirectML GPU (AMD/Intel)'),
    ]

    session = None
    available_providers = ort.get_available_providers()

    for provider_code, provider_name in hardware_options:
      print(f"Checking for {provider_name}...", end=" ", flush=True)
      
      if provider_code not in available_providers:
        print("Unavailable (package not installed).")
        continue

      if provider_code == 'CUDAExecutionProvider' and not has_nvidia_gpu():
        print("Unavailable (no NVIDIA hardware or drivers).")
        continue

      try:
        with SuppressStderr():
          test_session = new_session(model_code, providers=[provider_code])
        
        active_providers = test_session.inner_session.get_providers()
        if provider_code in active_providers:
          print("Available and active!")
          session = test_session
          break
        else:
          print("Unavailable.")
      except Exception:
        print("Unavailable.")

    if session is None:
      print("Falling back to CPU...", end=" ", flush=True)
      session = new_session(model_code, providers=['CPUExecutionProvider'])
      print("Active.")

    print("\nAI Model loaded successfully!")
    return 'ai', {'session': session}

def main():
  root = tk.Tk()
  root.withdraw()
  
  input_folder = Path("input")
  output_folder = Path("output")
  input_folder.mkdir(exist_ok=True)
  
  extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
  images = []
  for ext in extensions:
    images.extend(input_folder.glob(ext))
    
  num_images = len(images)
  
  if num_images == 0:
    print(f"No images found in the '{input_folder}' folder.")
    print("Please place your images (.jpg, .jpeg, .png, .webp) inside the 'input' folder and run the script again.")
    root.destroy()
    return

  mode, config = setup_method()

  if num_images == 1:
    img_path = images[0]
    print(f"\nFound exactly one image in 'input' folder: {img_path.name}")
    save_path = get_save_path(root, f"{img_path.stem}_nobg.png")
    
    if save_path:
      run_processing(img_path, save_path, mode, config)
    else:
      print("Save cancelled.")
      
  else:
    print(f"\nFound {num_images} images in the '{input_folder}' folder.")
    print("1. Process ALL images automatically to the 'output' folder")
    print("2. Select ONE image from list and choose where to save it")
    
    choice = input("\nEnter 1 or 2: ").strip()
    
    if choice == '1':
      batch_process(input_folder, output_folder, images, mode, config)
    elif choice == '2':
      process_selected_image(root, images, mode, config)
    else:
      print("Invalid choice. Exiting.")

  root.destroy()

if __name__ == "__main__":
  main()