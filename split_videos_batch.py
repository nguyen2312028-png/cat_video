import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# === CẤU HÌNH ===
INPUT_FOLDER = "input_videos"
OUTPUT_FOLDER = "outputs"
MIN_DURATION = 60
MAX_DURATION = 75
FONT_SIZE = 40
FONT_COLOR = "white"
FONT = "Arial"  # ✅ An toàn vì hệ điều hành nào cũng có

def add_ep_text(video_clip, ep_num):
    txt = TextClip(f"Ep{ep_num}", fontsize=FONT_SIZE, color=FONT_COLOR, font=FONT)
    txt = txt.set_position(("right", "bottom")).set_duration(video_clip.duration)
    return CompositeVideoClip([video_clip, txt])

def split_video(input_path, output_subfolder):
    clip = VideoFileClip(input_path)
    duration = clip.duration
    start = 0
    ep_num = 1

    while start < duration:
        remaining = duration - start
        segment_length = random.randint(MIN_DURATION, MAX_DURATION)
        end = duration if remaining < MIN_DURATION else min(start + segment_length, duration)
        subclip = clip.subclip(start, end)
        subclip = add_ep_text(subclip, ep_num)
        out_path = os.path.join(output_subfolder, f"ep{ep_num}.mp4")
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")
        start = end
        ep_num += 1

def process_all_videos():
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print("📂 Đã tạo thư mục input_videos/. Hãy bỏ video vào đó rồi chạy lại.")
        return
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith((".mp4", ".mov", ".mkv"))]
    if not files:
        print("⚠️ Không tìm thấy video nào trong input_videos/")
        return
    for filename in files:
        input_path = os.path.join(INPUT_FOLDER, filename)
        name_no_ext = os.path.splitext(filename)[0]
        output_subfolder = os.path.join(OUTPUT_FOLDER, name_no_ext)
        os.makedirs(output_subfolder, exist_ok=True)
        print(f"▶️ Đang xử lý: {filename}")
        split_video(input_path, output_subfolder)
    print("✅ Hoàn tất xử lý tất cả video.")

if __name__ == "__main__":
    process_all_videos()
