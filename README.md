🕹️ Pygame版 Pac-Man 技術解説
1. アーキテクチャ - エンティティ駆動型 & 状態遷移型アーキテクチャ
このPac-Manは、エンティティ駆動型設計をベースに構成されています。
プレイヤー（Pac-Man）、敵（ゴースト）、エサ（ドット）、そして迷路（Maze）がそれぞれ独立したクラスとなっており、
各オブジェクトが自身の位置・向き・色・行動ロジックを自己完結的に保持しています。

また、各オブジェクトは状態遷移型の設計を採用しており、
ゴーストの行動パターンの変化や、エサの消滅、プレイヤーの移動方向変更など、
リアルタイムで状態が変化する仕組みになっています。

2. 技術スタック & 描画システム
技術スタック
Python 3.x
Pygameライブラリ（描画・イベント処理・サウンド管理・フレームレート制御）
描画システム
Pygameの**Surface（仮想キャンバス）**を直接操作。
迷路、キャラクター、エサを毎フレーム再描画するフレームベース描画。
各エンティティが**draw()メソッド**を持ち、描画処理を自身にカプセル化。
これにより、エンティティごとに描画責務が分離され、全体の保守性と拡張性を向上。
3. エンティティ設計 - 役割ごとのクラス設計
3-1. Pac-Manクラス
プレイヤーキャラクターとして、矢印キーによる操作を担当。
移動時に迷路構造をチェックし、壁衝突を防止。
エサ座標リストを参照して、エサを消滅させる。
位置・向き・速度を自身の内部状態として保持し、リセットや初期化も容易。
3-2. ゴーストクラス
敵キャラクターとして、AIによる自律移動を担当。
迷路とPac-Manの位置を常に参照し、AIタイプに応じた行動を選択。
Chaser（追跡型）: Pac-Manを最短距離で追跡。
Random（ランダム型）: 毎フレームランダム方向に進行。
壁衝突や袋小路対策のロジックも含む。
3-3. ドットクラス
迷路内に配置されたエサを担当。
Pac-Manが通過した際に消滅し、スコアに加算される。
3-4. Mazeクラス
マップデータ（壁・通路・エサ配置）を一元管理。
壁の位置や通行可能な道を保持し、各キャラクターの移動判定に参照される。
迷路自体の描画も担当し、エンティティと分離。
4. ゲームロジック & ゴーストAIアルゴリズム
4-1. プレイヤー操作（Pac-Man）
矢印キー入力をPygameイベントキューから取得。
迷路構造をチェックし、移動可能なら方向変更。
壁判定はブロック単位（BLOCK_SIZE）で行い、ドット通過も同様。
4-2. ゴーストAIの概要
Chaser（追跡型AI）
毎フレーム、Pac-Manの現在座標を取得。
ゴーストの周囲4方向のうち、Pac-Manに最短で近づける方向を選択。
壁衝突を考慮しつつ、最適な経路を選び続ける。
Random（ランダム型AI）
毎フレーム、ランダムに移動方向を選択。
移動先が壁の場合は、再選択して進行方向を決定。
壁や袋小路で立ち往生しないよう、適宜方向変更。
5. 設計パターン & 責務分離
5-1. メインループ構造
以下のシンプルなループで、全体の流れを制御：

画面クリア（黒背景に初期化）
キー入力処理（Pygameイベントキュー参照）
Pac-Manの移動とエサチェック
ゴーストのAI移動とPac-Man衝突判定
各エンティティの再描画
画面更新
メインループはフレーム制御とシンプルな進行管理のみ担当。
各オブジェクトのロジックや状態更新は各クラスに分離済み。
5-2. イベント駆動型構造
QUITイベント（ウィンドウクローズ）もイベントキューで管理。
プレイヤー操作（矢印キー）もイベントとして処理。
各エンティティは自身の内部状態に基づく行動を実行し、
外部からの過剰な干渉を回避。
6. ユーザーインタラクション & リアルタイム反映
毎秒30フレームで、ゲーム状態更新・描画をループ。
プレイヤー操作は即時反映し、遅延のない操作感を実現。
入力→状態更新→描画のサイクルを厳密に守る設計。
7. 衝突判定 & ゲームオーバー
Pac-Manとゴーストの座標距離を毎フレーム計算。
近接距離が一定以下になれば接触判定とし、即ゲームオーバー処理。
距離判定はBLOCK_SIZEの半分程度の閾値で判定。
8. 拡張性 & メンテナンス性
項目	拡張内容
ゴーストAI	新AIパターンを容易に追加可能
マップ変更	Mazeクラスの初期マップ定義を変更するだけで対応
スコア表示	任意の位置にスコア表示を追加可能
サウンド	PygameのSound機能をそのまま活用可能
9. まとめ
技術要素	内容
アーキテクチャ	エンティティ駆動＋状態遷移型
描画	Pygame Surface直接描画
AI	追跡型・ランダム型の両AI搭載
イベント処理	Pygameイベントキュー方式
拡張性	マップ・AI・スコア・UIなど柔軟対応可能
