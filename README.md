# SWAT (Sword World Assistant Tool)

# WIP Go で書き直し

## 概要
 SWATはSW2.5向けのバフ・デバフ管理ツールです
 ルールブックⅠ、Ⅱ、Ⅲの範囲＋α をカバーしています

## 必要なツール

Windows
 - [Windows ターミナル](https://www.microsoft.com/ja-jp/p/windows-terminal-preview/9n0dx20hk701?activetab=pivot:overviewtab)

Linux, Mac
 - git (直接zipファイルをダウンロードする場合は必要なし)
 - python3.x

## 使い方

### Windows

`/swat`直下にある `main.exe` をWindows ターミナル 上にドラッグ・アンド・ドロップして、Windowsターミナル上で起動してください

### Linux, Mac の場合

 ```bash
 $ git clone https://github.com/t4t5u0/swat.git
 $ cd swat
 $ python prompt.py
 ```

環境によっては、`python` と叩くと、python2系が立ち上がることがあります。適宜`python3` に置き換えてコマンドを叩いてください。


## ユーザ定義データの追加
template.json の様式を参考にして、`./json_data/` にjsonファイルを配置し、

```bash
$ cd swat/json_data
$ vim hoge.json
$ python database_commands.py  --skill_list
```

と叩いてください

## コマンドの解説

### ユーザシナリオの一例

![](https://cdn.discordapp.com/attachments/422691044669390849/718151445911830538/unknown.png)

## 開発について
バグを報告したり、ドキュメントを改善したい場合は、[GitHubのIssue](https://github.com/t4t5u0/swat/issues)、または[Twitter](https://www.twitter.com/i4mwh4ti4m)をご利用ください。

### 報告 
バグがあった場合は、ログや状況を添えて報告をお願いします

### 要望
なぜそれが必要なのか理由を添えてお願いします

## SWについて
「ソードワールド2.5」は株式会社KADOKAWAとグループSNEが権利を保有する北沢慶氏およびグループSNEの著作物です。

## LICENSE
[MIT License](https://github.com/t4t5u0/sw_tool/blob/develop/LICENSE)
