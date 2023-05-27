# Python-RPA
RPA

## 概要 Description
pywinauto を使用したRPA  
音声認識を使用したRPA  

- ブラウザの操作  

## 特徴 Features

- ブラウザをキー操作で制御します  
- RPA パッケージに pywinauto を使用します  
- 音声入力に voice_input_juu7g パッケージを使用します(音声認識の場合)  

## 依存関係 Requirement

- Python 3.8.5  
- pywinauto 0.6.8  
- voice_input_juu7g (音声認識の場合)

## 使い方 Usage

- 操作
	- ブラウザの接続
		- コンボボックスから制御するブラウザを選択
		- 制御するタブの名称の一部を入力フィールドに指定  
			他のタブと区別がつく名称を入れます
		- 接続ボタンを押す
			接続ボタンの背景が緑になれば操作開始です
			- 緑：成功
			- 赤：タイムアウト
			- 黄：複数候補がある
	- ブラウザの制御
		- ボタンを押すとボタンに表示されている動作を行います
		- 検索ボタンを押す場合、ボタンの下の入力フィールドに検索ワードを入力します

- 画面の説明
	- ボタン
		- 下：下に一ページ分スクロール
		- 次のページ：ページの下の「次のページ」ボタンを押して次のページを表示
		- 上：上に一ページ分スクロール
		- トップ：ページの一番上にスクロール
		- ボトム：ページの一番下にスクロール
		- 次のリンク：次のリンク位置にカーソルを移動（Tab キーの動き）
		- 戻る：表示を戻す（）
		- 見る：カーソルのあるリンク先を表示
		- 検索：入力フィールドの文字を検索

- 画面の説明(音声認識の場合)  
	- ボタン
		- 下に：下に１ページ分スクロール
		- 次のページ：ページの下の「次のページ」ボタンを押して次のページを表示
		- 上に：上に１ページ分スクロール
		- 一番上に：ページの一番上にスクロール
		- 一番下に：ページの一番下にスクロール
		- 次のリンク：次のリンク位置にカーソルを移動（Tab キーの動き）
		- 戻る：表示を戻す
		- 表示：カーソルのあるリンク先を表示
		- 閉じる：タブを閉じます
		- 検索：入力フィールドの文字を検索
		- 音声認識：音声認識をオンにします。「終わり」と認識するとオフします。

## 制限事項  

- Chrome での「次のページ」の動作は不安定です  
- 「次のページ」ボタンは、はてなブログのグループサイトを想定しています  

## 依存関係パッケージのインストール方法 Installation

- pip install pywinauto  
- pip install git+https://github.com/juu7g/Python-voice-input.git (音声認識の場合)

## プログラムの説明サイト Program description site

- [pywinautoでRPA（自動化）◇導入編【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/rpa/pywinauto/introduction)  
- [pywinautoでRPA（自動化）◇ブラウザ編【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/rpa/pywinauto/browser)  
- [音声認識でブラウザを操作【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/rpa/pywinauto/voice-browser)

## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSEを確認してください。  
This software is released under the MIT License, see LICENSE.

