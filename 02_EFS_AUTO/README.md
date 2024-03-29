# EFS AUTO

## 0. Index

[1. 목적 및 아키텍처](#1-목적-및-아키텍처)

- [1-1. 목적](#1-1-목적)

- [1-2. 아키텍처](#1-2-아키텍처)

[2.필요 서비스](#2-필요-서비스)

[3. 상세 설명](#3-상세-설명)

- [3-1. CloudTrail](#3-1-cloudtrail)

- [3-2. EventBridge](#3-2-eventbridge)

- [3-3. Lambda](#3-3-lambda)

- [3-4. SSM Document](#3-4-ssm-document)

[4. 문제점 및 개선하고 싶은 사항](#4-문제점-및-개선하고-싶은-사항)

- [4-1. 문제점](#4-1-문제점)

- [4-2. 개선하고 싶은 사항](#4-2-개선하고-싶은-사항)

---

## 1. 목적 및 아키텍처

### 1-1. 목적

EFS Access Point를 생성하고나서 EFS 관리 서버에 직접 마운트를 등록하는 반복적인 작업을 자동화로 해결하고자 만들었습니다.

### 1-2. 아키텍처

![efs_auto drawio](https://github.com/may-30/toy-project/assets/155306250/1efa5dc5-dfdd-45b3-8cb8-1a2c8d2f7831)

---

## 2. 필요 서비스

- CloudTrail

- EventBridge

- Lambda

- SSM Document

---

## 3. 상세 설명

### 3-1. CloudTrail

CloudTrail은 기본적으로 생성되는 Cloud 기반 로그를 추적하기 위해 사용되는 서비스이지만 CloudTrail에서 발생하는 API를 활용하기 위해서는 특별한 작업이 필요합니다.

![스크린샷 2024-03-19 오후 10 27 57](https://github.com/may-30/toy-project/assets/155306250/b6773bb4-eaba-469b-bc85-616949887add)

바로 `CloudTrail 추적`을 생성해야 합니다.

### 3-2. EventBridge

CloudTrail 추적을 생성하고나서 EFS 서비스의 `CreateAccessPoint`를 특정 지은 EventBridge를 생성합니다.

```json
{
  "source": ["aws.elasticfilesystem"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["elasticfilesystem.amazonaws.com"],
    "eventName": ["CreateAccessPoint"]
  }
}
```

### 3-3. Lambda

이번 로직의 가장 핵심적인 부분이며 사전적인 조건으로는 아래 사진처럼 `Lambda 함수의 환경 변수`를 설정해주어야 합니다.

![스크린샷 2023-12-08 10 56 36](https://github.com/may-30/toy-project/assets/155306250/7df426be-e695-406e-85df-edb625148acc)

`Lambda 함수의 환경 변수`를 설정해주면 Lambda 함수에서 `os.environ['환경변수값']`처럼 사용 가능합니다.

### 3-4. SSM Document

Lambda 함수 내부 로직에 포함되어 있는 단계로 EFS 관리 서버에 명령어를 전송하여 EFS 마운트를 진행합니다.

---

## 4. 문제점 및 개선하고 싶은 사항

### 4-1. 문제점

Lambda 함수에서 Command 내용이 포함되어 있어 해당 내용을 완전 분리해야 한다는 생각을 하게 되었습니다.

이유는 Lambda 함수 서비스의 경우 주로 Admin 권한을 가지고 있는 SA, DevOps 뿐만 아니라 외주 개발사의 경우에도 들어와서 보는 경우도 있기 때문에 Command 관련한 내용은 감추는 것이 좋을 것 같다는 생각이 들었습니다.

### 4-2. 개선하고 싶은 사항

AWS 서비스 중 SSM Automation을 활용하여 Command 내용을 가려야 합니다.

---
