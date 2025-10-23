import requests
import os
import base64
from pydub import AudioSegment
from pydub.playback import play
import re

def get_podcast_content(file_path="podcast-content.md"):
    """Reads the podcast script from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{file_path}'.")
        return None

def convert_text_to_speech(api_key, text_content):
    """Calls the Gemini TTS API and returns the raw audio data."""
    url = "https://api.thucchien.ai/audio/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }

    # Extract conversation for the TTS engine
    # We will format it to clearly distinguish speakers.
    conversation = ""
    # Use regex to find speaker lines like __Anh Minh:__ or __Cô Lan:__
    lines = re.findall(r"__([A-Za-z\s]+):__\s*\((.*?)\)\s*(.*)", text_content)
    
    # Reconstruct the text for the TTS model
    tts_text = "TTS the following conversation between Anh Minh and Cô Lan:\n"
    for speaker, _, line in lines:
        speaker_name = "Anh Minh" if "Minh" in speaker else "Cô Lan"
        tts_text += f"{speaker_name}: {line.strip()}\n"

    payload = {
        "contents": [{
            "parts": [{"text": tts_text}]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "multiSpeakerVoiceConfig": {
                    "speakerVoiceConfigs": [
                        {
                            "speaker": "Anh Minh",
                            "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}
                        }, 
                        {
                            "speaker": "Cô Lan",
                            "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Puck"}}
                        }
                    ]
                }
            }
        },
        "model": "gemini-2.5-flash-preview-tts",
    }

    print("Đang gửi yêu cầu đến Google Gemini TTS API...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Yêu cầu thành công!")
        response_data = response.json()
        try:
            audio_data_b64 = response_data['candidates'][0]['content']['parts'][0]['inlineData']['data']
            return base64.b64decode(audio_data_b64)
        except (KeyError, IndexError) as e:
            print(f"Lỗi: Không tìm thấy dữ liệu âm thanh trong phản hồi API. {e}")
            print("Phản hồi đầy đủ:", response.text)
            return None
    else:
        print(f"Lỗi API: {response.status_code}")
        print(response.text)
        return None

def save_and_process_audio(raw_data, output_filename="podcast_output.wav"):
    """Saves raw PCM data to a WAV file using pydub."""
    if not raw_data:
        print("Không có dữ liệu âm thanh để xử lý.")
        return

    try:
        # The API returns PCM audio at 24000 Hz, 16-bit, single-channel (mono)
        print("Đang xử lý dữ liệu âm thanh bằng pydub...")
        audio_segment = AudioSegment(
            data=raw_data,
            sample_width=2,  # 16-bit = 2 bytes
            frame_rate=24000,
            channels=1
        )
        
        print(f"Đang lưu file âm thanh vào '{output_filename}'...")
        audio_segment.export(output_filename, format="wav")
        print(f"Đã lưu file thành công! Bạn có thể mở '{output_filename}'.")
        
        # Optional: Play the audio
        # print("Đang phát âm thanh...")
        # play(audio_segment)

    except Exception as e:
        print(f"Lỗi khi xử lý hoặc lưu file âm thanh: {e}")

def main():
    """Main function to run the TTS conversion."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Lỗi: Vui lòng thiết lập biến môi trường 'GEMINI_API_KEY'.")
        return

    podcast_script = get_podcast_content()
    if not podcast_script:
        return

    raw_audio_data = convert_text_to_speech(api_key, podcast_script)
    
    if raw_audio_data:
        save_and_process_audio(raw_audio_data)

if __name__ == "__main__":
    main()
