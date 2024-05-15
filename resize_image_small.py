from PIL import Image

def resize_image(input_image_path, output_image_path, size=(80, 130)):
    """
    Thay đổi kích thước hình ảnh và giữ hình ảnh không bị vỡ và mờ đi.

    Parameters:
    - input_image_path: Đường dẫn đến hình ảnh gốc.
    - output_image_path: Đường dẫn đến hình ảnh sau khi thay đổi kích thước.
    - size: Kích thước mới của hình ảnh (mặc định là (50, 50)).
    """
    with Image.open(input_image_path) as img:
        resized_img = img.resize(size, Image.ANTIALIAS)
        resized_img.save(output_image_path)

# Sử dụng hàm resize_image
input_path = "Solitaire/cards/1H.png"  # Đường dẫn đến hình ảnh gốc
output_path = "Solitaire/cards/1H.png"  # Đường dẫn đến hình ảnh sau khi thay đổi kích thước

resize_image(input_path, output_path, size=(80, 125))  # Kích thước mới nhỏ hơn
