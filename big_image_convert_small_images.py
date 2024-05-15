from PIL import Image
import os

def resize_image(img, target_width=90, target_height=90):
    return img.resize((target_width, target_height), Image.ANTIALIAS)

def remove_white_background(img):
    img = img.convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # Loại bỏ các pixel màu trắng
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def merge_images(image_paths, output_path):
    # Đọc, điều chỉnh kích thước và loại bỏ nền trắng của các ảnh
    images = [remove_white_background(resize_image(Image.open(path), target_width=48, target_height=48)) for path in image_paths]

    # Tính toán kích thước của ảnh kết quả
    width, height = images[0].size
    num_images = len(images)
    rows = (num_images - 1) // 12 + 1
    result_width = width * 12 + 10 * 11
    result_height = height * rows + 10 * (rows - 1)

    # Tạo ảnh kết quả mới
    result = Image.new('RGBA', (result_width, result_height), color=(255, 255, 255, 0))

    # Hợp nhất các ảnh
    for idx, img in enumerate(images):
        row = idx // 12
        col = idx % 12
        x = col * (width + 10)
        y = row * (height + 10)
        result.paste(img, (x, y), img)

    # Tạo ảnh mới với kích thước mong muốn
    new_result = Image.new('RGBA', (1044, 740), color=(255, 255, 255, 0))
    new_result.paste(result, ((1044 - result_width) // 2, (740 - result_height) // 2))

    # Lưu ảnh kết quả
    new_result.save(output_path)
    print(f"Đã hợp nhất, điều chỉnh kích thước và loại bỏ nền trắng của {num_images} ảnh thành {output_path}")

if __name__ == "__main__":
    # Đường dẫn đến thư mục chứa ảnh
    directory_path = "Pikachu/images"
    output_path = "Pikachu/images/merged_image.png"

    # Lấy danh sách các ảnh trong thư mục
    image_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(".png")]

    # Hợp nhất, điều chỉnh kích thước và loại bỏ nền trắng của các ảnh
    merge_images(image_paths, output_path)
