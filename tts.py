import requests
import os
from pathlib import Path
import time

# Danh sách các giọng nói
voices = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", 
    "Callirrhoe", "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba", 
    "Despina", "Erinome", "Algenib", "Rasalgethi", "Laomedeia", "Achernar", 
    "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird", "Zubenelgenubi", 
    "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat"
]

# Tạo thư mục voice_outputs nếu chưa có
output_dir = Path("voice_outputs")
output_dir.mkdir(exist_ok=True)

# API configuration
url = "https://api.thucchien.ai/audio/speech"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-kTSjM-tT7bjDjfJHuw8u-g"
}

# Văn bản mẫu để test
sample_text = "Xin chào, đây là một thử nghiệm chuyển văn bản thành giọng nói qua AI Thực Chiến gateway."

print(f"Bắt đầu tải {len(voices)} giọng mẫu...")
print("=" * 60)

success_count = 0
failed_voices = []

for i, voice in enumerate(voices, 1):
    try:
        print(f"[{i}/{len(voices)}] Đang tải giọng: {voice}... ", end="")
        
        # Tạo payload
        payload = {
            "model": "gemini-2.5-flash-preview-tts",
            "input": sample_text,
            "voice": voice
        }
        
        # Gọi API
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # Kiểm tra response
        if response.status_code == 200:
            # Lưu file MP3
            output_file = output_dir / f"{voice}.mp3"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content) / 1024  # KB
            print(f"✓ Thành công ({file_size:.1f} KB)")
            success_count += 1
        else:
            print(f"✗ Lỗi (HTTP {response.status_code})")
            failed_voices.append(voice)
            
    except Exception as e:
        print(f"✗ Lỗi: {str(e)}")
        failed_voices.append(voice)
    
    # Delay nhỏ giữa các request để tránh rate limit
    if i < len(voices):
        time.sleep(0.5)

print("=" * 60)
print(f"\nHoàn thành!")
print(f"✓ Thành công: {success_count}/{len(voices)}")
print(f"✗ Thất bại: {len(failed_voices)}/{len(voices)}")

if failed_voices:
    print(f"\nCác giọng thất bại: {', '.join(failed_voices)}")

print(f"\nCác file đã được lưu vào thư mục: {output_dir.absolute()}")%     