<<<<<<< HEAD
# ComfyUI-NijiVoice

ComfyUI-NijiVoiceは、ComfyUIから「にじぼいす」のAPIを呼び出して音声ファイルを生成するための拡張機能です。

## 機能

- にじぼいすAPIとの連携
- 利用可能なキャラクター一覧の取得
- テキストから音声の生成
- 生成した音声ファイルの保存

## インストール方法

1. ComfyUIがインストールされていることを確認してください。

2. このリポジトリをComfyUIの`custom_nodes`ディレクトリにクローンします：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI-NijiVoice.git
```

または、ZIPファイルをダウンロードして`custom_nodes`ディレクトリに展開することもできます。

3. 必要なPythonパッケージをインストールします：

```bash
pip install requests
```

4. ComfyUIサーバーを再起動します。

## 使用方法

### 1. APIキーの取得

にじぼいすAPIを使用するには、APIキーが必要です。以下の手順でAPIキーを取得してください：

1. [にじぼいス公式サイト](https://nijivoice.com/)にアクセスし、アカウントを作成またはログインします。
2. APIキーを取得します。

### 2. 基本的な使用フロー

1. **にじぼいす API設定**ノードでAPIキーを設定します。
2. **にじぼいす キャラクター一覧**ノードで利用可能なキャラクター一覧を取得します。
3. **にじぼいす キャラクター選択**ノードで使用するキャラクターを選択します。
4. **にじぼいす テキスト入力**ノードで読み上げるテキストと速度を設定します。
5. **にじぼいす 音声生成**ノードで音声を生成します。
6. **にじぼいす 音声保存**ノードで音声ファイルを保存します。

### 3. サンプルワークフロー

基本的なワークフローの例：

```
NijiVoiceAPISetup → NijiVoiceCharacterList → NijiVoiceCharacterSelect
                  ↓                                       ↓
             NijiVoiceTextInput ----------------------→ NijiVoiceGenerate → NijiVoiceSaveAudio
```

## 注意事項

- にじぼいすAPIの利用には、にじぼいすの利用規約に従う必要があります。
- 商用利用時はクレジット表記が必要です（「にじボイス」「Voiced by NIJI Voice」など）。
- APIの利用には文字数制限があります。詳細はにじぼいす公式サイトをご確認ください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 謝辞

- [にじぼいす](https://nijivoice.com/)：高品質な音声生成APIを提供していただきありがとうございます。
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)：素晴らしいUIフレームワークを提供していただきありがとうございます。
=======
# comfyui_custom_nodes
comfyui_custom_nodes
>>>>>>> 4a18cd1c6f683bfab96b8dcfd4cdfaae314f821b
