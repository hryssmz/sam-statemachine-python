# README

## 1. セットアップ手順

---

コマンドプロンプトでプロジェクトのルードディレクトリ（`samlocal-python`）に `cd` する。

### 1.1. `localstack` コンテナ作成

---

`localstack` コンテナを作成する。以下のコマンドを実行する。

```bat
docker compose -f docker\docker-compose.yml up -d
```

以下のように `localstack` コンテナと `localstack_network` ネットワークが作成されたら成功。

```log
[+] Running 2/2
 ⠿ Network localstack_network  Created
 ⠿ Container localstack        Started
```

### 1.2. ソースビルド

---

以下のコマンドを実行する。（コマンドが存在しない場合は `pip install aws-sam-cli-local` 実行後再度試す）

```bat
samlocal build
```

以下のように `Build Succeeded` が表示されたら成功。

```log
Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Validate SAM template: sam validate
[*] Invoke Function: sam local invoke
[*] Test Function in the Cloud: sam sync --stack-name {{stack-name}} --watch
[*] Deploy: sam deploy --guided
```

### 1.3. デプロイ

---

LocalStack に API Gateway や DynamoDB などのリソースをデプロイする。以下のコマンドを実行する。

```bat
bat\deploy.bat
```

以下のように `Outputs` が表示されていたら成功。

```log
...
--------------------------------------------------------------------------------
Outputs
--------------------------------------------------------------------------------
Key                 HelloWorldApi
Description         -
Value               http://localhost:4566/restapis/yoikxuk77m/test/_user_request_/
--------------------------------------------------------------------------------

Successfully created/updated stack - samlocal-python in ap-northeast-1
```

`curl` コマンドで `Outputs` で表示されている API Gateway のエンドポイントにリクエストを送る。（`yoikxuk77m` の部分は各自で得られたものに置き換える）

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/test/_user_request_/
```

以下のように空の JSON 配列が得られれば成功。

```json
[]
```

### 1.4. SAM アプリ実行環境との結合テスト

---

SAM アプリ実行環境からでも LocalStack のリソース（DynamoDB など）にアクセス出来ることを確認する。以下のコマンドを実行。

```bat
bat\invoke.bat
```

以下のように `"statusCode": 200` が表示されていたら成功。

```log
{"statusCode": 200, "headers": {}, "body": "[]", "multiValueHeaders": {}, "isBase64Encoded": false}END RequestId: 73fd1e78-f006-4cc5-8211-40381361e09a
REPORT RequestId: 73fd1e78-f006-4cc5-8211-40381361e09a  Init Duration: 0.10 ms  Duration: 339.60 ms Billed Duration: 340 ms Memory Size: 128 MB     Max Memory Used: 128 MB
```
