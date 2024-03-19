# Toy Project

## 0. Index

[1. 01_SSO_SCRAP](#1-01_sso_scrap)

[2. 02_EFS_AUTO](#2-02_efs_auto)

## 1. 01_SSO_SCRAP

SSO (AWS IAM Identity Center)의 정보를 셀레니움 + Boto3 + Openpyxl 기반으로 동작시켜 최종 엑셀 파일로 다운로드할 수 있게 동작하는 코드입니다.

- [바로 가기](./01_SSO_SCRAP/)

---

## 2. 02_EFS_AUTO

EFS Access Point를 생성하면 CloudTrail API를 Lambda 함수의 Trigger로 잡는 EventBridge를 생성하여 SSM Document를 실행하여 EFS 관리 서버에 자동으로 마운트하는 코드입니다.

- [바로 가기](./02_EFS_AUTO/)

---