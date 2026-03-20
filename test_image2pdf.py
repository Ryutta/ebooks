import os
from PIL import Image
from image2pdf import image_to_pdf

# Create test directories
os.makedirs("test_out/image", exist_ok=True)

# Create a landscape image
img1 = Image.new('RGB', (1920, 1080), color = 'red')
img1.save('test_out/image/1.png')

# Create a portrait image
img2 = Image.new('RGB', (1080, 1920), color = 'blue')
img2.save('test_out/image/2.png')

# Test image2pdf
image_to_pdf(1, 2, "test_out", "")

print("Done. Check test_out/pdf/1_2.pdf")
