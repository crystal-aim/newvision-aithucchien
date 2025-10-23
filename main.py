from dotenv import load_dotenv

import requests
import json
import base64


def convert_curl_to_python():
    """
    Converts the given curl command to a Python script using the requests library.
    """
    url = "https://api.thucchien.ai/gemini/v1beta/models/gemini-2.5-pro-preview-tts:generateContent"
    
    headers = {
        "x-goog-api-key": "sk-MzujiChtWpC5Xn2pHNOQ5g",
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "TTS the following conversation between Anh Minh and Cô Lan:\n                Cô Lan: (Thở dài) Cô cũng muốn hỏi han chuyện học hành, bạn bè của tụi nó, muốn kể chuyện ngày xưa... mà lại sợ làm phiền. Nhiều khi cô hỏi một tiếng và nó chỉ ừ hử qua loa rồi thôi. Thành ra mình cứ cảm giác như người vô hình trong chính nhà mình vậy đó, cháu ạ. (Ngập ngừng) Nhiều khi cô cũng tự hỏi, có phải mình đã già, đã lạc hậu quá rồi không...\n                Anh Minh: Dạ, cháu cảm ơn cô đã trải lòng mình. Cái cảm giác 'vô hình' cô nói, nghe thật xót xa. Cháu tin là nhiều bậc cha mẹ, ông bà ngoài kia cũng có chung nỗi niềm này. Đây không phải chuyện của riêng nhà mình đâu cô ạ."
            }]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "multiSpeakerVoiceConfig": {
                    "speakerVoiceConfigs": [{
                        "speaker": "Cô Lan",
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "Gacrux"
                            }
                        }
                    }, {
                        "speaker": "Anh Minh",
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "Alnilam"
                            }
                        }
                    }]
                }
            }
        },
        "model": "gemini-2.5-pro-preview-tts",
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        
        response_json = response.json()
        
        # Extract the base64 encoded data
        audio_data_base64 = response_json['candidates'][0]['content']['parts'][0]['inlineData']['data']
        
        # Decode the base64 data
        audio_data = base64.b64decode(audio_data_base64)
        
        # Write the decoded data to a file
        with open("out.pcm", "wb") as f:
            f.write(audio_data)
            
        print("Successfully generated and saved audio to out.pcm")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    convert_curl_to_python()
