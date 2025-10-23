from dotenv import load_dotenv
load_dotenv()

import requests
import json
import base64
import os

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai/v1"
AI_API_KEY =  os.getenv("API_KEY")
AUDIO_SAVE_PATH = "generated_podcast_background.wav"

# --- Bước 1: Gọi API để tạo âm thanh ---
url = f"{AI_API_BASE}/chat/completions"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {AI_API_KEY}"
}
data = {
  # Giả định tên model, bạn có thể cần thay đổi thành model tạo âm thanh chính xác
  "model": "music-generation-v1", 
  "messages": [
      {
          "role": "user",
          "content": "Background music for an audio podcast, calm and inspiring."
      }
  ]
}

try:
  print("Sending request to generate audio...")
  response = requests.post(url, headers=headers, data=json.dumps(data))
  response.raise_for_status()

  result = response.json()
  # Giả định cấu trúc response cho audio, có thể cần điều chỉnh
  # Dựa trên cấu trúc của image, tôi đoán audio sẽ nằm trong 'audio' thay vì 'images'
  base64_string = result['choices'][0]['message']['audio'][0]['audio_url']['url']
  print("Audio data received successfully.")

  # --- Bước 2: Giải mã và lưu file âm thanh ---
  # Loại bỏ tiền tố 'data:audio/wav;base64,' nếu có
  if ',' in base64_string:
      header, encoded = base64_string.split(',', 1)
  else:
      encoded = base64_string

  audio_data = base64.b64decode(encoded)

  with open(AUDIO_SAVE_PATH, 'wb') as f:
      f.write(audio_data)
  
  print(f"Audio saved to {AUDIO_SAVE_PATH}")

except requests.exceptions.RequestException as e:
  print(f"An error occurred: {e}")
  print(f"Response body: {response.text if 'response' in locals() else 'No response'}")
except (KeyError, IndexError) as e:
  print(f"Failed to parse audio data from response: {e}")
  print(f"Response body: {response.text if 'response' in locals() else 'No response'}")

