본 프로젝트는 쇼핑몰 상품 관리 API를 설계 및 구현한 과제입니다.
할인율, 쿠폰 등 다양한 가격 정책이 적용된 최종 판매가 계산 로직을 중심으로 설계되었으며,
클린 아키텍처와 도메인 주도 설계(DDD) 패턴을 기반으로 유연하고 확장 가능한 구조를 지향합니다.

## 실행방법
```docker-compose up --build```

## 설계 의도
확장성: 쿠폰 정책, 할인 정책이 다양해지는 상황을 고려해 Strategy 패턴 적용

응집력 높은 도메인 설계: Product, Coupon 등 핵심 도메인을 중심으로 도메인 계층 설계

프레임워크 의존도 제거: domain 계층은 FastAPI 및 ORM과 분리

테스트 용이성: Repository, Service 등을 인터페이스로 추상화하여 유닛 테스트가 쉬움

## 프로젝트 구조

```
├── docker-compose.yml
├── milie
│   ├── adapter # 외부 의존성 구현체
│   │   └── repository
│   │       ├── coupon_repository.py
│   │       └── product_repository.py
│   ├── api # API 라우터 정의
│   │   └── v1
│   │       ├── coupon_router.py
│   │       ├── product_router.py
│   │       └── schema.py
│   ├── application # 유즈케이스 / 서비스 계층
│   │   ├── coupon
│   │   │   └── coupon_service.py
│   │   └── product
│   │       └── product_service.py
│   ├── config.py
│   ├── Dockerfile
│   ├── domain # 핵심 도메인 모델 및 정책
│   │   ├── coupon
│   │   │   ├── collection.py
│   │   │   ├── entity.py
│   │   │   ├── exception.py
│   │   │   ├── policy.py
│   │   │   └── value_object.py
│   │   └── product
│   │       ├── discount_policy.py
│   │       ├── entity.py
│   │       └── value_object.py
│   ├── factory # service, repository DI를 위한 factory
│   │   ├── repository_factory.py
│   │   └── service_factory.py
│   ├── infrastructure # ORM 모델 및 DB 연동
│   │   └── orm
│   │       └── sql_alchemy
│   │           ├── base.py
│   │           ├── coupon
│   │           │   ├── model.py
│   │           │   └── repository_impl.py
│   │           ├── product
│   │           │   ├── model.py
│   │           │   └── repository_impl.py
│   │           └── session.py
│   ├── main.py
│   ├── requirements.txt
│   ├── shared
│   │   └── logger.py
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── coupons
│       │   ├── test_coupon.py
│       │   └── test_coupons_collection.py
│       └── product
│           └── test_product.py
└── README.MD
```

## API 명세서

### 상품 등록
Method: POST

Endpoint: /api/v1/products

설명: 상품을 등록합니다.

요청예시:
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Millie'\''s library",
  "base_price": 10000,
  "shipping_fee": 2500,
  "discount_policy_type": "RATE",
  "discount_value": 0.1
}'
```

### 상품 목록 조회
Method: GET

Endpoint: /api/v1/products

설명: 상품 목록을 조회합니다.(페이징)

요청예시:
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/products?offset=0&limit=10' \
  -H 'accept: application/json'
```

### 상품 상세 조회
Method: GET

Endpoint: /api/v1/products/{product_id}

설명: 상품을 상세 조회합니다. 사용 가능한 쿠폰도 같이 조회합니다.

요청예시:
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/products/1' \
  -H 'accept: application/json'
```

### 상품 가격 조회
Method: GET

Endpoint: /api/v1/products/{product_id}/price

설명: 상품의 가격을 조회합니다. 할인율과 쿠폰에 따른 가격을 조회합니다.

요청예시:
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/products/1/price?coupon_ids=1&coupon_ids=2&quantity=1' \
  -H 'accept: application/json'
```

### 상품 쿠폰 연결
Method: POST

Endpoint: /api/v1/products/{product_id}/coupons

설명: 해당 상품에 쿠폰을 연결합니다.

요청예시:
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/products/1/coupons' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "coupon_ids": [
    2
  ]
}'
```


### 쿠폰 생성
Method: POST

Endpoint: /api/v1/coupons

설명: 쿠폰을 생성합니다.

요청예시:
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/coupons' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "배송비 무료",
  "type": "배송비 무료",
  "expired_date": "2025-12-31T23:59:59",
  "usage_limit": 1
}'
```


## PS
어쩔 수 없는 변명이지만, 과제를 받았을 당시 해외여행을 왔던 터라 시간이 많이 부족했습니다...
테스트코드도 불안정하고 핵심코드도 작성을 못하였습니다.
염치없지만 양해를 부탁 드리겠습니다..(지금도 귀국 비행기 시간때문에 지금 commit을 해야합니다..)