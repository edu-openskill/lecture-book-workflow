# 5.5. Lambda 구현

S3의 original/ 경로로 업로드된 이미지를 감지하여 Lambda가 자동으로 리사이즈한 뒤 resized/ 경로에 저장하는 흐름을 구현합니다. 핵심 목표는 “업로드 이벤트 수신 → 원본 다운로드 → 이미지 처리 → 결과 업로드”의 파이프라인을 안정적으로 구성하는 것입니다.

---

## 1) Lambda 리사이즈 함수

코드 탭을 클릭하여 **코드 소스** 섹션으로 이동하여 리사이즈하는 함수를 생성합니다.

![image.png](5%205%20Lambda%20%EA%B5%AC%ED%98%84/image.png)

해당 에디터에 아래 함수를 입력하고 데이터 왼쪽 사이드에 보이는 **Deploy**를 실행합니다. 업데이트 문구와 오른쪽 하단에 Successfully updated… 문구를 확인합니다.

---

### **Lambda 리사이즈 함수 구성(코드 파트별 설명)**

### **1. 기본 구성 및 이벤트 로그**

```python
import json
import boto3
# PIL(Pillow): Image는 Pillow가 제공하는 이미지 처리 모듈(클래스/객체) 입니다.
from PIL import Image 
import io

# S3 클라이언트 생성
s3 = boto3.client("s3")

def lambda_handler(event, context):
    print("=== S3 Upload Event ===")
    print(json.dumps(event))  
    
    ##아래 코드를 순서대로 추가합니다.
```

이 Lambda 함수는 S3의 original/ 경로에 이미지가 업로드되면(ObjectCreated 이벤트) 실행됩니다. 실행 시 이벤트 내용을 로그로 출력하여, 어떤 버킷의 어떤 파일이 업로드되었는지 확인할 수 있습니다.

---

### **2. 이벤트 수신: bucket / objectKey 추출 및 필터링**

```python
# 1) 이벤트에서 bucket / key 추출
bucket = event["Records"][0]["s3"]["bucket"]["name"]
key = event["Records"][0]["s3"]["object"]["key"]

# original/ 경로만 처리
if not key.startswith("original/"):
    print("[SKIP] original/ 경로가 아닙니다.")
    return {"status": "ignored"}

# uuid 추출 (original/{uuid}.{ext} → uuid)
file_name = key.replace("original/", "")
uuid = file_name.rsplit(".", 1)[0]

print(f"[INFO] original file key: {key}")
print(f"[INFO] uuid: {uuid}")
```

S3 이벤트에서 bucket과 key(objectKey)를 추출하고, original/로 시작하는 파일만 처리합니다. 이후 원본 key에서 UUID를 추출해 리사이즈 결과 경로를 구성하는 기준값으로 사용합니다.

---

### **3. 이미지 처리: 원본 다운로드(GetObject) + 변환/리사이즈 + JPEG 저장**

```python
# 2) S3에서 원본 이미지 다운로드
original_obj = s3.get_object(Bucket=bucket, Key=key)
original_bytes = original_obj["Body"].read()
```

```python
# 3) Pillow로 이미지 처리
image = Image.open(io.BytesIO(original_bytes))
image = image.convert("RGB")        # JPEG 저장 대비
image.thumbnail((800, 800))         # 긴 변 기준 800px

buffer = io.BytesIO()
image.save(buffer, format="JPEG", quality=85)
buffer.seek(0)
```

원본 이미지를 S3에서 내려받은 뒤, Pillow로 이미지를 열어 RGB로 변환하고(JPEG 저장 대비), thumbnail((800, 800))로 긴 변 기준 800px로 축소합니다. 처리 결과는 메모리 버퍼(BytesIO)에 JPEG로 저장하여 이후 업로드에 사용합니다.

---

### **4. 결과 저장: resized/ 경로로 업로드(PutObject)**

```python
# 4) 리사이즈된 파일 S3에 업로드
resized_key = f"resized/{uuid}.jpg"

s3.put_object(
    Bucket=bucket,
    Key=resized_key,
    Body=buffer,
    ContentType="image/jpeg",
)

print(f"[SUCCESS] 리사이즈 이미지 업로드 완료: {resized_key}")
```

리사이즈 결과는 resized/{uuid}.jpg 규칙으로 업로드합니다. 원본과 결과는 동일 UUID로 연결되므로, 서버는 규칙만 알고 있어도 결과 경로를 안정적으로 계산할 수 있습니다.

---

### **5. 메타데이터(응답/로그) 구성**

```python
# 5) 최종 응답
return {
    "status": "success",
    "originalKey": key,
    "resizedKey": resized_key
}
```

함수는 처리 결과를 확인할 수 있도록 originalKey와 resizedKey를 반환합니다. 운영 단계에서는 필요에 따라 size, width/height 같은 메타데이터를 추가로 계산해 로그로 남기거나 서버(DB 저장)에 활용할 수 있습니다.

---

## 2) Lambda 계층

lambda_handler 함수에서 from PIL import Image는 Pillow 라이브러리의 이미지 처리 기능을 사용하기 위한 임포트입니다. 다만 AWS Lambda 런타임에는 Pillow가 기본 포함돼 있지 않기 때문에, Pillow를 **Layer**로 추가해 함수에서 사용할 수 있도록 구성합니다.

<aside>
💡

계층은 라이브러리, 사용자 지정 런타임 또는 기타 종속 항목을 포함하는 ZIP 아카이브입니다. 

</aside>

![image.png](5%205%20Lambda%20%EA%B5%AC%ED%98%84/image%201.png)

Add a Layer를 클릭합니다.

---

![image.png](5%205%20Lambda%20%EA%B5%AC%ED%98%84/image%202.png)

ARN 지정을 클릭하여 arn:aws:lambda:ap-northeast-2:770693421928:layer:Klayers-p311-Pillow:10을 입력 후 확인을 클릭하면 등록된 리전의 ARN을 확인할 수 있습니다.

![image.png](5%205%20Lambda%20%EA%B5%AC%ED%98%84/image%203.png)

<aside>
💡

**ARM이란?**

ARN은 AWS에서 리소스(Lambda Layer, S3 버킷 등)를 식별하는 고유한 주소(식별자)입니다. 아래 주소에서 리전별 Layer ARN을 확인할 수 있으며, 확인한 ARN을 Lambda Layer 식별자로 입력해 계층을 추가합니다.

```java
https://api.klayers.cloud/api/v2/p3.11/layers/latest/ap-northeast-2/html
```

![image.png](5%205%20Lambda%20%EA%B5%AC%ED%98%84/image%204.png)

</aside>

---