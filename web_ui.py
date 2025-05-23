import os
import json
from typing import Dict, Any, Optional

class NijiVoiceWebUI:
    """フロントエンドのUIカスタマイズを行うクラス"""
    
    @classmethod
    def INPUT_WIDGETS(cls):
        """カスタムウィジェットの定義"""
        return {
            "NijiVoiceAPISetup": {
                "api_key": {"widget": "password"}
            },
            "NijiVoiceCharacterSelect": {
                "character_index": {"widget": "dropdown", "dynamic": True}
            }
        }
    
    @classmethod
    def DISPLAY_UI(cls):
        """ノードの表示カスタマイズ"""
        return {
            "NijiVoiceAPISetup": {"color": "#ff9999", "icon": "🔑"},
            "NijiVoiceCharacterList": {"color": "#99ccff", "icon": "📋"},
            "NijiVoiceTextInput": {"color": "#99ff99", "icon": "📝"},
            "NijiVoiceCharacterSelect": {"color": "#ffcc99", "icon": "👤"},
            "NijiVoiceGenerate": {"color": "#cc99ff", "icon": "🔊"},
            "NijiVoiceSaveAudio": {"color": "#ffff99", "icon": "💾"}
        }
    
    @classmethod
    def CHARACTER_DROPDOWN_HANDLER(cls, characters):
        """キャラクター選択ドロップダウンの動的生成"""
        options = []
        for i, character in enumerate(characters):
            options.append({
                "value": i,
                "label": f"{character.get('name', 'Unknown')} ({character.get('gender', '?')})"
            })
        return options
