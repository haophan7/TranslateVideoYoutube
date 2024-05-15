from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import time

translator = Translator()

outls = []

# Lấy transcript của video
tx = YouTubeTranscriptApi.get_transcript('gzRXsXQJXmw', languages=['en'])
for i in tx:
    outtxt = i['text']
    try:
        # Dịch từ tiếng Anh sang tiếng Việt
        translated_text = translator.translate(outtxt, src='en', dest='vi').text
        outls.append(translated_text)

        # Ghi nội dung đã dịch vào tệp văn bản
        with open("translated_output.txt", "a", encoding="utf-8") as opf:
            opf.write(translated_text + "\n")
    except KeyboardInterrupt:
        print("Dịch bị ngắt bởi người dùng.")
        break
    except Exception as e:
        print("Đã xảy ra lỗi:", str(e))
        time.sleep(1)  # Đợi 1 giây trước khi thử lại

# Hiển thị thông báo khi dịch hoàn tất
print("Đã dịch video từ tiếng Anh có phụ đề sang tiếng Việt thành công.")
