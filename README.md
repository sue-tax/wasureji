# wasureji

ファイルの受渡しを記録するソフトです。

ファイルをいつ、誰から、どのように受け取ったか、いつ、誰に、どのように渡したかをデータベースに記録します。

スキャンしてPDFファイルにした現物の管理にも活用できます。

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

## 使用方法

wasureji_server.exeは、事前に起動しておきます。

記録したいファイルを右クリックして、wasureji_inputを選択します。

必要な項目を入力して、OKを押します。

記録した内容を確認するとき、修正するときも、同じように、右クリックして、wasureji_inputを選択します。

他で記録した内容は、コンボボックスから選択して入力することができます。

日付は、今日と昨日の日付がコンボボックスから選択して入力することができます。

## 開発予定

渡し先は、１つのファイルに複数設定可能に。

ファイルの一括入力。

検索機能。

ファイルの移動、削除などの監視機能。

