import requests
import json
import os
import base64
from typing import Dict, List, Tuple, Any, Optional

class NijiVoiceAPI:
    """にじぼいすAPIとの通信を行うクラス"""
    
    BASE_URL = "https://api.nijivoice.com/api/platform/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_voice_actors(self) -> List[Dict[str, Any]]:
        """利用可能な音声キャラクター一覧を取得する"""
        url = f"{self.BASE_URL}/voice-actors"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get("voiceActors", [])
        except requests.exceptions.RequestException as e:
            print(f"キャラクター一覧の取得に失敗しました: {e}")
            return []
    
    def generate_voice(self, voice_actor_id: str, script: str, speed: float = 1.0, format: str = "mp3") -> Optional[Dict[str, Any]]:
        """音声を生成する"""
        url = f"{self.BASE_URL}/voice-actors/{voice_actor_id}/generate-voice"
        
        data = {
            "script": script,
            "speed": str(speed),
            "format": format
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json().get("generatedVoice")
        except requests.exceptions.RequestException as e:
            print(f"音声生成に失敗しました: {e}")
            return None
    
    def generate_encoded_voice(self, voice_actor_id: str, script: str, speed: float = 1.0, format: str = "mp3") -> Optional[str]:
        """Base64エンコードされた音声を生成する"""
        url = f"{self.BASE_URL}/voice-actors/{voice_actor_id}/generate-encoded-voice"
        
        data = {
            "script": script,
            "speed": str(speed),
            "format": format
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json().get("base64EncodedAudio")
        except requests.exceptions.RequestException as e:
            print(f"エンコード音声生成に失敗しました: {e}")
            return None
    
    def get_credit_balance(self) -> Optional[Dict[str, Any]]:
        """クレジット残高を取得する"""
        url = f"{self.BASE_URL}/balances"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"クレジット残高の取得に失敗しました: {e}")
            return None

class NijiVoiceAPISetup:
    """APIキーの設定と認証を行うノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "default": ""})
            }
        }
    
    RETURN_TYPES = ("NIJIVOICE_API",)
    FUNCTION = "setup_api"
    CATEGORY = "NijiVoice"
    
    def setup_api(self, api_key):
        api = NijiVoiceAPI(api_key)
        return (api,)

class NijiVoiceCharacterList:
    """利用可能なキャラクター一覧を取得するノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api": ("NIJIVOICE_API",)
            }
        }
    
    RETURN_TYPES = ("NIJIVOICE_CHARACTERS",)
    FUNCTION = "get_characters"
    CATEGORY = "NijiVoice"
    
    def get_characters(self, api):
        characters = api.get_voice_actors()
        return (characters,)

class NijiVoiceTextInput:
    """音声生成用のテキスト入力ノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "こんにちは、にじぼいすです。"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.4, "max": 3.0, "step": 0.1})
            }
        }
    
    RETURN_TYPES = ("NIJIVOICE_PARAMS",)
    FUNCTION = "prepare_params"
    CATEGORY = "NijiVoice"
    
    def prepare_params(self, text, speed):
        params = {
            "text": text,
            "speed": speed
        }
        return (params,)

class NijiVoiceCharacterSelect:
    """音声キャラクターを選択するノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "characters": ("NIJIVOICE_CHARACTERS",),
                "character_index": ("INT", {"default": 0, "min": 0, "max": 999})
            }
        }
    
    RETURN_TYPES = ("NIJIVOICE_CHARACTER",)
    FUNCTION = "select_character"
    CATEGORY = "NijiVoice"
    
    def select_character(self, characters, character_index):
        if not characters or character_index >= len(characters):
            print("キャラクターが選択できません。インデックスが範囲外か、キャラクターリストが空です。")
            return (None,)
        
        selected_character = characters[character_index]
        return (selected_character,)

class NijiVoiceGenerate:
    """音声を生成するノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api": ("NIJIVOICE_API",),
                "params": ("NIJIVOICE_PARAMS",),
                "character": ("NIJIVOICE_CHARACTER",),
                "format": (["mp3", "wav"], {"default": "mp3"})
            }
        }
    
    RETURN_TYPES = ("NIJIVOICE_AUDIO",)
    FUNCTION = "generate_audio"
    CATEGORY = "NijiVoice"
    
    def generate_audio(self, api, params, character, format):
        if character is None:
            print("キャラクターが選択されていません。")
            return (None,)
        
        character_id = character.get("id")
        if not character_id:
            print("キャラクターIDが取得できません。")
            return (None,)
        
        text = params.get("text", "")
        speed = params.get("speed", 1.0)
        
        # Base64エンコードされた音声を取得
        encoded_audio = api.generate_encoded_voice(character_id, text, speed, format)
        if not encoded_audio:
            print("音声の生成に失敗しました。")
            return (None,)
        
        audio_data = {
            "base64_data": encoded_audio,
            "format": format,
            "character_name": character.get("name", "unknown"),
            "text": text
        }
        
        return (audio_data,)

class NijiVoiceSaveAudio:
    """生成された音声を保存するノード"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_data": ("NIJIVOICE_AUDIO",),
                "filename": ("STRING", {"default": "nijivoice_audio"}),
                "directory": ("STRING", {"default": "./outputs"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "save_audio"
    CATEGORY = "NijiVoice"
    OUTPUT_NODE = True
    
    def save_audio(self, audio_data, filename, directory):
        if audio_data is None:
            print("音声データがありません。")
            return ("",)
        
        # ディレクトリが存在しない場合は作成
        os.makedirs(directory, exist_ok=True)
        
        base64_data = audio_data.get("base64_data")
        format = audio_data.get("format", "mp3")
        
        if not base64_data:
            print("音声データが不正です。")
            return ("",)
        
        # ファイル名に拡張子を追加
        full_filename = f"{filename}.{format}"
        file_path = os.path.join(directory, full_filename)
        
        try:
            # Base64データをデコードしてファイルに保存
            audio_binary = base64.b64decode(base64_data)
            with open(file_path, "wb") as f:
                f.write(audio_binary)
            
            print(f"音声ファイルを保存しました: {file_path}")
            return (file_path,)
        except Exception as e:
            print(f"音声ファイルの保存に失敗しました: {e}")
            return ("",)

# ノードのマッピング
NODE_CLASS_MAPPINGS = {
    "NijiVoiceAPISetup": NijiVoiceAPISetup,
    "NijiVoiceCharacterList": NijiVoiceCharacterList,
    "NijiVoiceTextInput": NijiVoiceTextInput,
    "NijiVoiceCharacterSelect": NijiVoiceCharacterSelect,
    "NijiVoiceGenerate": NijiVoiceGenerate,
    "NijiVoiceSaveAudio": NijiVoiceSaveAudio
}

# ノードの表示名マッピング
NODE_DISPLAY_NAME_MAPPINGS = {
    "NijiVoiceAPISetup": "にじぼいす API設定",
    "NijiVoiceCharacterList": "にじぼいす キャラクター一覧",
    "NijiVoiceTextInput": "にじぼいす テキスト入力",
    "NijiVoiceCharacterSelect": "にじぼいす キャラクター選択",
    "NijiVoiceGenerate": "にじぼいす 音声生成",
    "NijiVoiceSaveAudio": "にじぼいす 音声保存"
}
