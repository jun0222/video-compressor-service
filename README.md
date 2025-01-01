## 概要

```python
# server.pyでサーバーを起動
python3 stage2/server.py

# client.pyでクライアントを起動
# 配置しているファイルがアップロード、変換される
python3 stage2/client.py
```

## TODO

- [ ] 解像度とか command line arg で指定できるようにする
- [ ] 音声のメタデータがない場合のハンドリング
- [ ] 動画の受け取りをより実践的に

## シーケンス

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Backend
    participant Storage
    User->>Frontend: ファイル選択
    Frontend->>Frontend: ファイル存在チェック
    Frontend->>Frontend: ファイルサイズ確認
    Frontend->>Backend: TCP接続要求
    Backend->>Backend: ポート待ち受け
    Backend-->>Frontend: 接続確立
    Frontend->>Frontend: ファイル分割
    Frontend->>Frontend: データ圧縮
    Frontend->>Frontend: ファイル暗号化
    loop ファイル送信
        Frontend->>Backend: ファイルデータ送信
        Backend->>Backend: データ検証
        alt 送信エラー
            Backend-->>Frontend: エラー通知
            Frontend->>Backend: 再送処理
        end
    end
    Backend->>Backend: データ解凍
    Backend->>Backend: ファイル復号化
    Backend->>Backend: ファイル結合
    Backend->>Storage: ファイル保存
    Storage-->>Backend: 保存完了
    Backend-->>Frontend: 完了通知
    Frontend-->>User: アップロード完了表示
    Frontend->>Backend: 切断要求
    Backend-->>Frontend: 切断完了
```
