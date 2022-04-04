![version](https://img.shields.io/badge/version-1.0.2-blue)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# 주유소 유가 정보 센서

즐겨찾는 주유소의 유가 정보를 보여줍니다. 전국평균 유가 정보 센서도 자동으로 추가됩니다.\
이 센서는 `오피넷`의 전국유가정보와 `카카오 플레이스`의 상점 정보에서 데이터를 가져옵니다.

<br>

## Screenshot
![screenshot1](https://user-images.githubusercontent.com/49514473/79197668-1b227700-7e6d-11ea-9208-cca012131709.png)\
\
![screenshot2](https://user-images.githubusercontent.com/49514473/79197659-18278680-7e6d-11ea-88b8-bcfd945f3080.png)

<br>

## Version history
| Version | Date        |               |
| :-----: | :---------: | ------------- |
| v1.0    | 2020.04.14  | 최초 버전 |
| v1.0.2  | 2022.04.04  | device_state_attributes -> extra_state_attributes |

<br>


## Installation

### 직접 설치
- HA 설치 경로 아래 custom_component 에 파일을 넣어줍니다.
<br>`<config directory>/custom_components/oil_price/sensor.py`
<br>`<config directory>/custom_components/oil_price/__init__.py`
<br>`<config directory>/custom_components/oil_price/manifest.json`
- configuration.yaml 파일에 설정을 추가합니다.
- Home Assistant 를 재시작합니다.

### HACS로 설치
- HACS > Integrations 메뉴 선택
- 우측 상단 메뉴 버튼 클릭 후 Custom repositories 선택
- Add Custom Repository URL 에 `https://github.com/GrecHouse/oil_price` 입력, \
  Category에 `Integration` 선택 후 ADD
- HACS > Integrations 메뉴에서 우측 하단 + 버튼 누르고 `[KR] Oil Price Sensor` 검색하여 설치

<br>

## Usage

### 주유소 키 값 얻기
- [카카오맵](https://map.kakao.com/)에서 추가하려는 주유소를 찾습니다.
- 주유소 이름을 눌러 상세 정보 페이지로 이동합니다.\
\
![3](https://user-images.githubusercontent.com/49514473/79194363-60dc4100-7e67-11ea-9fc0-814246e35239.png)\

- 주소창의 URL 에서 마지막에 숫자로 된 부분을 이용하면 됩니다.\
place.map.kakao.com/`11111111`\
\
![4](https://user-images.githubusercontent.com/49514473/79194371-633e9b00-7e67-11ea-94d7-7b8ee241e121.png)

<br>

### configuration
- 아래와 같이 HA에 설정을 추가합니다.

**configuration.yaml 기본설정 :**
```yaml
sensor:
  - platform: oil_price
```

**configuration.yaml 상세설정 :**
```yaml
sensor:
  - platform: oil_price
    type: '02'  
    station_id:
      - '11111111'
      - '22222222'
```

<br>

**Configuration variables:**

|옵션|값|
|--|--|
|platform| (필수) oil_price |
|type| (옵션) 기름 종류.<br>미설정시 기본값은 '02'(휘발유) |
|station_id| (옵션) 주유소 키 리스트.<br>미설정시 전국평균가격만 센서로 추가됨 |
<br>

**type variable:**
|값|종류|
|--|--|
|01|고급휘발유|
|02|휘발유|
|03|경유|
|04|LPG|
|05|등유|

- `05/등유` 는 카카오 플레이스 정보에서 제공되지 않습니다.
<br>

## 설명
- 전국평균유가 `sensor.oil_price_avg` 는 기본적으로 생성됩니다.
- 전국평균 속성 중 `price diff` 는 전일대비 가격 변동 내역입니다.
- 추가한 주유소들은 `sensor.oil_price_[station_id]` 로 생성됩니다.

<br>

### 센서 카드 샘플
![sensor-card](https://user-images.githubusercontent.com/49514473/79198317-4194e200-7e6e-11ea-83ad-b52e0e2ef1ca.png)

### mini-graph 카드 샘플
![mini-graph-card](https://user-images.githubusercontent.com/49514473/79198311-3f328800-7e6e-11ea-84b1-3d10e17e58ce.png)


## 버그 또는 문의사항
네이버 카페 [HomeAssistant](https://cafe.naver.com/koreassistant/) `그렉하우스` \
네이버 카페 [모두의스마트홈](https://cafe.naver.com/stsmarthome/) `그렉하우스`



