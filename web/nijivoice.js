// ComfyUI-NijiVoice拡張機能のフロントエンドスクリプト
import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// ノードの見た目をカスタマイズするための設定
const nodeStyles = {
    "NijiVoiceAPISetup": { color: "#ff9999", icon: "🔑" },
    "NijiVoiceCharacterList": { color: "#99ccff", icon: "📋" },
    "NijiVoiceTextInput": { color: "#99ff99", icon: "📝" },
    "NijiVoiceCharacterSelect": { color: "#ffcc99", icon: "👤" },
    "NijiVoiceGenerate": { color: "#cc99ff", icon: "🔊" },
    "NijiVoiceSaveAudio": { color: "#ffff99", icon: "💾" }
};

// APIキー入力フィールドをパスワードタイプに変更
function setupAPIKeyPasswordField(node, inputEl, inputData) {
    if (node.type === "NijiVoiceAPISetup" && inputData.name === "api_key") {
        // 既存の入力フィールドを削除
        if (inputEl.querySelector("input")) {
            inputEl.querySelector("input").remove();
        }
        
        // パスワードタイプの入力フィールドを作成
        const input = document.createElement("input");
        input.type = "password";
        input.value = inputData.value || "";
        input.placeholder = "APIキーを入力";
        
        // スタイル設定
        input.style.width = "100%";
        input.style.padding = "4px";
        input.style.border = "1px solid #666";
        input.style.borderRadius = "4px";
        
        // 値変更時のイベント
        input.addEventListener("change", (e) => {
            inputData.value = e.target.value;
            node.onWidgetChanged(inputData.name, e.target.value);
        });
        
        // 入力フィールドを追加
        inputEl.appendChild(input);
        return true; // カスタム処理を行ったことを示す
    }
    return false; // デフォルトの処理を行う
}

// キャラクター選択ドロップダウンの動的生成
function setupCharacterDropdown(node, inputEl, inputData) {
    if (node.type === "NijiVoiceCharacterSelect" && inputData.name === "character_index") {
        // 既存の入力フィールドを削除
        if (inputEl.querySelector("select")) {
            inputEl.querySelector("select").remove();
        }
        
        // ドロップダウンを作成
        const select = document.createElement("select");
        select.style.width = "100%";
        select.style.padding = "4px";
        select.style.border = "1px solid #666";
        select.style.borderRadius = "4px";
        
        // キャラクターリストが接続されているか確認
        const charactersInput = node.inputs ? node.inputs.find(input => input.name === "characters") : null;
        if (charactersInput && charactersInput.link !== null) {
            const linkId = charactersInput.link;
            const link = app.graph.links[linkId];
            if (link) {
                const sourceNode = app.graph.getNodeById(link.origin_id);
                if (sourceNode && sourceNode.outputs && sourceNode.outputs[link.origin_slot]) {
                    const characters = sourceNode.outputs[link.origin_slot].value;
                    if (Array.isArray(characters)) {
                        // キャラクターリストからオプションを生成
                        characters.forEach((character, index) => {
                            const option = document.createElement("option");
                            option.value = index;
                            option.text = `${character.name || "Unknown"} (${character.gender || "?"})`;
                            select.appendChild(option);
                        });
                        
                        // 現在の値を設定
                        select.value = inputData.value || 0;
                        
                        // 値変更時のイベント
                        select.addEventListener("change", (e) => {
                            const value = parseInt(e.target.value);
                            inputData.value = value;
                            node.onWidgetChanged(inputData.name, value);
                        });
                        
                        // ドロップダウンを追加
                        inputEl.appendChild(select);
                        return true;
                    }
                }
            }
        }
        
        // キャラクターリストが接続されていない場合のデフォルト表示
        const defaultOption = document.createElement("option");
        defaultOption.text = "キャラクターリストを接続してください";
        select.appendChild(defaultOption);
        select.disabled = true;
        inputEl.appendChild(select);
        return true;
    }
    return false;
}

// ノードのスタイルをカスタマイズ
function applyNodeStyle(node) {
    const style = nodeStyles[node.type];
    if (style) {
        // 背景色の設定
        if (style.color) {
            node.bgcolor = style.color;
        }
        
        // アイコンの設定
        if (style.icon) {
            const iconContainer = document.createElement("div");
            iconContainer.style.position = "absolute";
            iconContainer.style.top = "2px";
            iconContainer.style.right = "2px";
            iconContainer.style.fontSize = "16px";
            iconContainer.textContent = style.icon;
            
            // 既存のアイコンがあれば削除
            const existingIcon = node.domElement.querySelector(".nijivoice-icon");
            if (existingIcon) {
                existingIcon.remove();
            }
            
            iconContainer.classList.add("nijivoice-icon");
            node.domElement.appendChild(iconContainer);
        }
    }
}

// 拡張機能の初期化
app.registerExtension({
    name: "ComfyUI-NijiVoice",
    
    // ノード作成時のフック
    nodeCreated(node) {
        if (node.type && node.type.startsWith("NijiVoice")) {
            applyNodeStyle(node);
        }
    },
    
    // ウィジェットのカスタマイズ
    beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name && nodeData.name.startsWith("NijiVoice")) {
            // 元のonDrawForegroundを保存
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            
            // onDrawForegroundをオーバーライド
            nodeType.prototype.onDrawForeground = function(ctx) {
                if (onDrawForeground) {
                    onDrawForeground.apply(this, arguments);
                }
                
                // ノードのスタイルを適用
                applyNodeStyle(this);
            };
            
            // 元のonNodeCreatedを保存
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // onNodeCreatedをオーバーライド
            nodeType.prototype.onNodeCreated = function() {
                if (onNodeCreated) {
                    onNodeCreated.apply(this, arguments);
                }
                
                // ノードのスタイルを適用
                applyNodeStyle(this);
            };
        }
    },
    
    // ウィジェット描画のカスタマイズ
    nodeViewTemplate(nodeType, nodeData) {
        if (nodeData.name && nodeData.name.startsWith("NijiVoice")) {
            return {
                widgets: {
                    render: (node, inputEl, inputData) => {
                        // APIキー入力フィールドのカスタマイズ
                        if (setupAPIKeyPasswordField(node, inputEl, inputData)) {
                            return true;
                        }
                        
                        // キャラクター選択ドロップダウンのカスタマイズ
                        if (setupCharacterDropdown(node, inputEl, inputData)) {
                            return true;
                        }
                        
                        return false; // デフォルトの処理を行う
                    }
                }
            };
        }
    }
});

// コンソールに拡張機能のロード完了メッセージを表示
console.log("ComfyUI-NijiVoice extension loaded");
