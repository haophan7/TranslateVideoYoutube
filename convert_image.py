from rembg import remove
from PIL import Image, ImageOps

input_path = 'Solitaire/images/ronery.png'
output_path = 'Solitaire/images/ronery.png'  # Lưu ảnh với định dạng PNG để giữ nền trong suốt

input_image = Image.open(input_path)
output_image = remove(input_image)

# Chuyển đổi ảnh sang chế độ RGBA nếu nó không phải là chế độ này
if output_image.mode != "RGBA":
    output_image = output_image.convert("RGBA")

# Tạo ảnh có nền trong suốt
new_image = Image.new("RGBA", output_image.size, (255, 255, 255, 0))
final_image = Image.alpha_composite(new_image, output_image)

# Lưu ảnh
final_image.save(output_path)
