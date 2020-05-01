# sw_tool

## 概要
 このリポジトリはSW2.5向けのバフ・デバフ管理ツールです

## 必要なツール
 - git (直接zipファイルをダウンロードする場合は必要なし)
 - python3.x

## 使い方
 現在はPythonで書かれているので、Pythonのパスを通す必要があります。(将来的には、他の言語で書き直す可能性があります。) サードパーティモジュールは現在のところ使用していないので、pip などはおそらく必要ないです。使用したい場合は、以下のコマンドを叩いてください。

 ```console
 $ git clone https://github.com/t4t5u0/sw_tool_prot.git
 $ cd sw_tool_prot
 $ python prompt.py
 ```

環境によっては、`python` と叩くと、python2系が立ち上がることがあります。適宜`python3` に置き換えてコマンドを叩いてください。


## ユーザ定義データの追加
template.json の様式を参考にして、`./json_data/` にjsonファイルを配置し、

```console
$ cd sw_tool_prot
$ python database_commands.py -d skill_list
```

と叩いてください