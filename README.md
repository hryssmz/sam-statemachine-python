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
Value               http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/
--------------------------------------------------------------------------------

Successfully created/updated stack - samlocal-python in ap-northeast-1
```

`curl` コマンドで `Outputs` で表示されている API Gateway のエンドポイントにリクエストを送る。（`yoikxuk77m` の部分は各自で得られたものに置き換える）

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/
```

以下のように空の JSON 配列が得られれば成功。

```log
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
{"statusCode": 200, "headers": {}, "body": "[]", "multiValueHeaders": {}, "isBase64Encoded": false}
```

## 2. API 一覧

---

### 2.1. 実行状況一覧取得

---

実行例:

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/
```

JSON 出力:

```json
[
  {
    "startedAt": "2022-12-01T22:01:51.891498+00:00",
    "amount": "2",
    "id": "161df506-ce3c-48be-bb32-8ce7a177824f",
    "status": "pending"
  },
  {
    "startedAt": "2022-12-01T22:01:15.305990+00:00",
    "amount": "3",
    "id": "4ac83be2-6acc-4122-a04b-0f407dda79ea",
    "winnings": "[]",
    "finishedAt": "2022-12-01T22:01:21.687656+00:00",
    "status": "success"
  }
]
```

### 2.2. くじデータ一覧取得

---

実行例 1:

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/lotteries/
```

JSON 出力 1:

```json
[
  {
    "executionId": "4ac83be2-6acc-4122-a04b-0f407dda79ea",
    "number": "3",
    "createdAt": "2022-12-01T22:01:20.173598+00:00",
    "id": "26afab65-6d07-4efa-8362-50d9f5453e5d",
    "code": "9",
    "winning": "0"
  },
  {
    "executionId": "4ac83be2-6acc-4122-a04b-0f407dda79ea",
    "number": "2",
    "createdAt": "2022-12-01T22:01:19.126099+00:00",
    "id": "c5ef4cbd-d89e-4a99-bea9-28d280fb9ae8",
    "code": "9",
    "winning": "0"
  },
  {
    "executionId": "161df506-ce3c-48be-bb32-8ce7a177824f",
    "number": "1",
    "createdAt": "2022-12-01T22:01:54.558367+00:00",
    "id": "91f5571b-4cf4-45f4-a32b-b5183d975ad1",
    "code": "5",
    "winning": "0"
  },
  {
    "executionId": "161df506-ce3c-48be-bb32-8ce7a177824f",
    "number": "2",
    "createdAt": "2022-12-01T22:01:57.634293+00:00",
    "id": "84d785c0-9aa6-4bf4-9155-3715d83ed614",
    "code": "2",
    "winning": "0"
  },
  {
    "executionId": "4ac83be2-6acc-4122-a04b-0f407dda79ea",
    "number": "1",
    "createdAt": "2022-12-01T22:01:17.930292+00:00",
    "id": "6174f80f-e62f-4349-bd0d-1e79bbfc81d7",
    "code": "1",
    "winning": "0"
  }
]
```

実行例 2:

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/lotteries/?execution-id=161df506-ce3c-48be-bb32-8ce7a177824f
```

JSON 出力 2:

```json
[
  {
    "executionId": "161df506-ce3c-48be-bb32-8ce7a177824f",
    "number": "1",
    "createdAt": "2022-12-01T22:01:54.558367+00:00",
    "id": "91f5571b-4cf4-45f4-a32b-b5183d975ad1",
    "code": "5",
    "winning": "0"
  },
  {
    "executionId": "161df506-ce3c-48be-bb32-8ce7a177824f",
    "number": "2",
    "createdAt": "2022-12-01T22:01:57.634293+00:00",
    "id": "84d785c0-9aa6-4bf4-9155-3715d83ed614",
    "code": "2",
    "winning": "0"
  }
]
```

### 2.3. 新しく実行を開始

---

実行例:

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/ -H "Content-Type: application/json" -d "{\"amount\": 2}" -X POST
```

JSON 出力:

```json
{
  "execution_arn": "arn:aws:states:ap-northeast-1:000000000000:execution:LotteryStateMachine:161df506-ce3c-48be-bb32-8ce7a177824f",
  "execution_name": "161df506-ce3c-48be-bb32-8ce7a177824f",
  "start_date": "2022-12-01T22:01:50.766000+00:00"
}
```

### 2.4. データを削除

---

実行例:

```bat
curl -s http://localhost:4566/restapis/yoikxuk77m/dev/_user_request_/empty/ -X POST
```

JSON 出力:

```json
["ExecutionTable", "LotteryTable"]
```
