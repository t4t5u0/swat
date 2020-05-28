# SWAT (Sword World Assistant Tool)

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

sw_tool直下にある `main.exe` をWindows ターミナル 上にドラッグ・アンド・ドロップして、Windowsターミナル上で起動してください

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
$ cd swat
$ vim hoge.json
$ python database_commands.py  --skill_list
```

と叩いてください

## コマンドの解説

### ユーザシナリオの一例

```console
$ python main.py 
Hello
────────────────────────────────────────────────────────────────────────────────────────────────────
- コマンド一覧は helps で見ることができます
- help cmd を使用すると cmd の詳細を見ることができます
────────────────────────────────────────────────────────────────────────────────────────────────────
> append gil -n ch1
<gil> をキャラクタリストに追加しました
<gil> を効果の対象にします
(gil)> add 追加攻撃 両手利き カウンター
gil に 《追加攻撃》 を付与しました
gil に 《両手利き》 を付与しました
0 【カウンター・マジック】
1 《カウンター》
2 【カウンター・デーモン】
追加したい技能の番号を入力してください:1
gil に 《カウンター》 を付与しました
(gil)> end
【ヘイスト】の処理を行ってください
(gil)> start
手番開始時に行う処理はありません
(gil)> ck
     名前      |                スキル名                 残りラウンド          効果        
────────────────────────────────────────────────────────────────────────────────────────────────────
      gil      |              《追加攻撃》                    -1       1H<格闘>での攻撃時、1H<格闘>による攻撃を1回追加
               |              《両手利き》                    -1       片手武器を2本、両腕に装備して扱える
               |             《カウンター》                   -1       近接攻撃時に対し、回避の代わりに攻撃を行う
               |              【ヘイスト】                     2       移動力+12m          
               |              【ヘイスト】                     2       主動作追加(5 or 6)  
────────────────────────────────────────────────────────────────────────────────────────────────────
(gil)> end
【ヘイスト】の処理を行ってください
(gil)> ck
     名前      |                スキル名                 残りラウンド          効果        
────────────────────────────────────────────────────────────────────────────────────────────────────
      gil      |              《追加攻撃》                    -1       1H<格闘>での攻撃時、1H<格闘>による攻撃を1回追加
               |              《両手利き》                    -1       片手武器を2本、両腕に装備して扱える
               |             《カウンター》                   -1       近接攻撃時に対し、回避の代わりに攻撃を行う
               |              【ヘイスト】                     3       移動力+12m          
               |              【ヘイスト】                     3       主動作追加(5 or 6)  
────────────────────────────────────────────────────────────────────────────────────────────────────
(gil)> start
手番開始時に行う処理はありません
(gil)> ap swift mola -n ch2 ch3
<swift> をキャラクタリストに追加しました
<mola> をキャラクタリストに追加しました
(gil)> ls
     name         nick   
──────────────────────────
      gil         ch1    
     swift        ch2    
     mola         ch3    
(gil)> ch ch2
<swift> を効果の対象にします
(swift)> ck --all
     名前      |                スキル名                 残りラウンド          効果        
────────────────────────────────────────────────────────────────────────────────────────────────────
      gil      |              《追加攻撃》                    -1       1H<格闘>での攻撃時、1H<格闘>による攻撃を1回追加
               |              《両手利き》                    -1       片手武器を2本、両腕に装備して扱える
               |             《カウンター》                   -1       近接攻撃時に対し、回避の代わりに攻撃を行う
               |              【ヘイスト】                     2       移動力+12m          
               |              【ヘイスト】                     2       主動作追加(5 or 6)  
────────────────────────────────────────────────────────────────────────────────────────────────────
     swift     |                                                                           
────────────────────────────────────────────────────────────────────────────────────────────────────
     mola      |                                                                           
──────────────────────────────────────────────────────────────────────────────────────────────────── 
(swift)> kill ch*
<gil> を削除しました。
<swift> を削除しました。
<mola> を削除しました。
> exit
終了しますか？ [Y/n] y
```

## 開発について
バグを報告したり、ドキュメントを改善したい場合は、GitHubのIssue、またはTwitterをご利用ください。

### 報告 
バグがあった場合は、ログや状況を添えて報告をお願いします

### 要望
なぜそれが必要なのか理由を添えてお願いします

## SWについて
「ソードワールド2.5」は株式会社KADOKAWAとグループSNEが権利を保有する北沢慶氏およびグループSNEの著作物です。

## Donation
kyash
![kyash://qr/u/6543631933160167877](https://cdn.discordapp.com/attachments/422717592407375872/715611669560295524/kyash_qr.jpg)

[Amazonウィッシュリスト](https://www.amazon.jp/hz/wishlist/ls/1IZFSBX7TAFX1?ref_=wl_share)

## LICENSE
[MIT License](https://github.com/t4t5u0/sw_tool/blob/develop/LICENSE)
