# wasureji

ファイルの受渡しを記録するソフトです。

ファイルをいつ、誰から、どのように受け取ったか、いつ、誰に、どのように渡したかをデータベースに記録します。

スキャンしてPDFファイルにした現物の管理にも活用できます。

プロトタイプです。

## インストール

### wasureji_server.exe

任意のフォルダに置きます。

事前に起動しておきます。

そのフォルダにwasureji.dbファイルが作られます。

### wasureji_input.exe

「SendTo」用のフォルダにコピーします。

※Windowsキー＋Rで、「ファイル名を指定して実行」ダイアログを開きます。

　「shell:sendto」を入力して、「OK」をクリックします。

　開いたフォルダが「SendTo」用のフォルダです。

　C:\Users\xxxxxxx\AppData\Roaming\Microsoft\Windows\SendToのようなフォルダ名で、プリンタのショートカットなどが入っています。

　そのフォルダにwasureji_input.exeファイルをコピーしてください。

### wasureji_all_in.exe

「SendTo」用のフォルダにコピーします。

### wasureji_all_out.exe

「SendTo」用のフォルダにコピーします。

### wasureji_utility.exe

任意のフォルダに置きます。


## 使用方法

wasureji_server.exeは、事前に起動しておきます。

記録したいファイルを右クリックして、wasureji_input.exeを選択します。

必要な項目を入力して、OKを押します。

記録した内容を確認するとき、修正するときも、同じように、右クリックして、wasureji_inputを選択します。

他で記録した内容は、コンボボックスから選択して入力することができます。

日付は、今日と昨日の日付がコンボボックスから選択して入力することができます。

### 出力項目の設定

「出力」（渡し先）は、１つのファイルに複数設定できます。

「追加」ボタン後に、各項目を設定し、「確定」ボタンを押します。

変更の場合は「変更」ボタン後に、各項目を修正し、「確定」ボタンを押します。

### 一括入力・出力

複数のファイルを選択してから、右クリックして、wasureji_all_in.exe または wasureji_all_out.exeを選択します。

wasureji_all_in.exeは、全てのファイルの入力項目を変更します。

wasureji_all_out.exeは、全てのファイルの出力項目を追加します。

### wasureji_utility.exe

「サーバー終了」ボタンで、wasureji_server.exeを終了します。

SQL文を入力して、「実行」ボタンで実行します。

`COMMIT`を自動で行わないので、必要に応じて`COMMIT`を実行してください。

## 開発予定

wasureji_clientの起動が遅い点を改良予定。

検索機能。検索後に置換や削除。

ファイルの移動、削除などの監視機能。

