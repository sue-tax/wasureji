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

各プログラムの通信用に、50054番のポートを使っています。

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


## 記録項目

各項目はフリーフォーマットです。

ただし、「,」（カンマ）と「"」（ダブルクォーテーション）は、入力しないでください。


### 基本項目

書類名　「確定申告書」、「登記簿謄本」など

顧客名　「〇〇社」、「田中△△」など

区分名　「令和Ｘ年分」など

※現バージョンでは、あまり重要ではありません。ファイル名で把握できるなら設定は不要です。

なお、将来の開発を予定している簡易なバージョン管理機能では、重要です。

### 入力項目

いつ　日付を入力、単に文字列として扱うのでフォーマットは自由、時間を入力してもよいです。wasureji_utilityで検索条件で範囲指定を行うつもりなら、フォーマットを統一した方が良いでしょう。

誰から　会社、担当者、官公庁などを入力

何で　メール、郵便、宅配便、持参、ダウンロードなどを入力

### 出力項目

いつ　日付を入力、単に文字列として扱うのでフォーマットは自由、時間を入力してもよいです。wasureji_utilityで検索条件で範囲指定を行うつもりなら、フォーマットを統一した方が良いでしょう。


誰へ　会社、担当者、官公庁などを入力

何で　メール、郵便、宅配便、持参などを入力

## 使用方法

wasureji_server.exeは、事前に起動しておきます。

記録したいファイルを右クリックして、wasureji_input.exeを選択します。

必要な項目を入力して、OKを押します。

記録した内容を確認するとき、修正するときも、同じように、右クリックして、wasureji_inputを選択します。

他で記録した内容は、コンボボックスから選択して入力することができます。

日付は、今日と昨日の日付がコンボボックスから選択して入力することができます。

ＯＫを押したときに、区分名、顧客名、書類名をクリップボードにコピーします。

### 出力項目の設定

「出力」（渡し先）は、１つのファイルに複数設定できます。

「追加」ボタン後に、各項目を設定し、「確定」ボタンを押します。

変更の場合は「変更」ボタン後に、各項目を修正し、「確定」ボタンを押します。

### 一括入力・出力

複数のファイルを選択してから、右クリックして、wasureji_all_in.exe または wasureji_all_out.exeを選択します。

wasureji_all_in.exeは、全てのファイルの入力項目を変更します。

wasureji_all_out.exeは、全てのファイルの出力項目を追加します。

### wasureji_utility.exe

#### サーバー終了

「サーバー終了」ボタンで、wasureji_server.exeを終了します。

#### ＳＱＬ実行

SQL文を入力して、「実行」ボタンで実行します。

コミットを自動で行わないので、必要に応じて「COMMIT」ボタンでコミットを実行してください。

#### 検索等

表示の下のチェックボックスをチェックして、検索後に表示する項目を指定します。

検索条件の下のチェックボックスにチェックして、検索条件を入力します。

「いつ」は、範囲指定できます。

複数の検索条件を指定した場合は、ＡＮＤ条件になります。

「表示」ボタンをクリックすると、検索結果が表示されます。

検索結果は、「Excel」ボタンでExcelファイルに書き込みます。

Excelファイルは、wasureji_utility.exeをインストールしたフォルダに、`wasureji.xlsx`や`wasureji_2.xlsx`のようなファイル名で保存されます。

「再読込」ボタンで、コンボボックスの候補を更新します。

※現バージョンでは、~~「Ｅｘｃｅｌ」（出力）、~~「置換」、「削除」はサポートしていません。


## 開発予定

~~wasureji_clientの起動が遅い点を改良予定。~~

ファイルの簡易なバージョン管理機能。

~~検索機能。~~検索後に置換や削除。

ファイルの移動、削除などの監視機能。

