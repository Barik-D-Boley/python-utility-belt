import qrcode

url = input("Provide the url: ").strip()

# Check if the user entered anything
if not url:
  print("Error: No URL was provided.")
else:
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
    filename = "qr.png"
    img.save(filename)

    print(f"Success: QR code created and saved as '{filename}'.")

  except Exception as e:
    print(f"Error: Failed to generate QR code. {e}")