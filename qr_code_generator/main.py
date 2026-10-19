import os
import qrcode

url = input("\nProvide the url: ").strip()

# Check if the user entered anything
if not url:
  print("Error: No URL was provided.")
else:
  # Get custom filename or fall back to default
  filename = input("Enter file name (press Enter for default 'qr.png'): ").strip()
  if not filename:
    filename = "qr.png"
  elif not filename.lower().endswith((".png", ".jpg", ".jpeg")):
    filename += ".png"

  # Ensure the "output" directory exists
  output_dir = "output"
  os.makedirs(output_dir, exist_ok=True)
  
  filepath = os.path.join(output_dir, filename)

  try:
    qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_M,
      box_size=10,
      border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate black-and-white static image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    print(f"Success: QR code created and saved to '{filepath}'.\n")

  except Exception as e:
    print(f"Error: Failed to generate QR code. {e}\n")