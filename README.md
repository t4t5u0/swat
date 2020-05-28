## sw_tool

# 概要
 このリポジトリはSW2.5向けのバフ・デバフ管理ツールです

# 必要なツール

Windows
 - [Windows ターミナル](https://www.microsoft.com/ja-jp/p/windows-terminal-preview/9n0dx20hk701?activetab=pivot:overviewtab)

Linux, Mac
 - git (直接zipファイルをダウンロードする場合は必要なし)
 - python3.x

# 使い方

Windows

sw_tool_prot直下にあるprompt.exe をWindows ターミナル 上にドラッグ・アンド・ドロップして、Windowsターミナル上で起動してください

Linux, Mac の場合

 ```bash
 $ git clone https://github.com/t4t5u0/sw_tool_prot.git
 $ cd sw_tool_prot
 $ python prompt.py
 ```

環境によっては、`python` と叩くと、python2系が立ち上がることがあります。適宜`python3` に置き換えてコマンドを叩いてください。


# ユーザ定義データの追加
template.json の様式を参考にして、`./json_data/` にjsonファイルを配置し、

```bash
$ cd sw_tool_prot
$ vim hoge.json
$ python database_commands.py  --skill_list
```

と叩いてください

## コマンドの解説

開発中のものです。ほぼ確定で変更されます。
ユーザシナリオの一例

```console
$ python prompt.py
Hello
─────────────────────────────────────────────────────────────────────
- コマンド一覧は helps で見ることができます
- help cmd を使用すると cmd の詳細を見ることができます
─────────────────────────────────────────────────────────────────────
> append ch1 ch2
ch1 をキャラクタリストに追加しました
ch2 をキャラクタリストに追加しました
> change ch1
ch1 を効果の対象にします
> start
> add ヘイスト
【ヘイスト】 to ch1
【ヘイスト】 to ch1
> check
ch1
skill name:【ヘイスト】     skill effect:{'付与': '移動力+12m'} round:         3
skill name:【ヘイスト】     skill effect:{'付与': '主動作追加(if 1d6 -> 5 or 6)'} round:         3
> add ウェポン
0 【エンチャント・ウェポン】
1 【ファイア・ウェポン】
2 【アイシクル・ウェポン】
3 【ソニック・ウェポン】
4 【ブラント・ウェポン】
5 【ウェポン・マスター】
追加したい技能の番号を入力してください:5
0 {'戦闘特技付与': '<<かいくぐり>>'}
1 {'戦闘特技付与': '<<ターゲッティング>>'}
2 {'戦闘特技付与': '<<武器習熟A:**>>'}
3 {'戦闘特技付与': '<<両手利き>>'}
4 {'戦闘特技付与': '<<囮攻撃Ⅰ>>'}
5 {'戦闘特技付与': '<<牽制攻撃Ⅰ>>'}
6 {'戦闘特技付与': '<<挑発攻撃Ⅰ>>'}
7 {'戦闘特技付与': '<<全力攻撃Ⅰ>>'}
8 {'戦闘特技付与': '<<必殺攻撃Ⅰ>>'}
9 {'戦闘特技付与': '<<鎧抜き>>'}
追加したい効果の番号を入力してください:3
【ウェポン・マスター】 to ch1
> check
ch1
skill name:【ヘイスト】     skill effect:{'付与': '移動力+12m'} round:         3
skill name:【ヘイスト】     skill effect:{'付与': '主動作追加(if 1d6 -> 5 or 6)'} round:         3
skill name:【ウェポン・マスター】 skill effect:{'戦闘特技付与': '<<両手利き>>'} round:        18
> end
【ヘイスト】1d6: 5
> start
...
> exit
終了しますか？ [Y/n] y
```