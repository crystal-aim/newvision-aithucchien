from dotenv import load_dotenv

import requests
import json
import base64

from scripts import dialogue
from pydub import AudioSegment

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
                "text": f"TTS the following conversation between Anh Minh (a 36-year-old therapist) and Cô Lan (a retired 62-year-old teacher):\n{dialogue}"
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