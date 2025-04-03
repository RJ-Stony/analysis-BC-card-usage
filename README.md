# 💳 BC Card Usage & 설날 이벤트 분석

BC 카드 소비 데이터를 기반으로 지역/업종별 소비 흐름을 파악하고,  
설날 이벤트 관련 텍스트를 자연어 처리 기법으로 분석한 프로젝트입니다.

---

## 📁 프로젝트 구조

```
analysis-BC-card-usage-main/
├── bc_card_analysis.py               # ✅ BC 카드 데이터 기반 소비 분석
├── newyear_event_text_analysis.py    # ✅ 설날 행사 관련 텍스트 분석
├── result/                           # 📊 분석 결과 시각화 및 이미지 저장
├── .gitignore
└── README.md
```

---

## 🔍 주요 기능

### 1. 카드 사용 분석 (`bc_card_analysis.py`)
- BC 카드 데이터를 기반으로 업종·지역별 소비금액 분석
- pandas + matplotlib을 활용한 그래프 시각화
- 연령/성별 또는 요일별 소비 트렌드 분석 가능

### 2. 설날 텍스트 분석 (`newyear_event_text_analysis.py`)
- 명절 행사 관련 문서 또는 문장을 전처리
- 형태소 분석 및 불용어 제거
- WordCloud를 통해 핵심 키워드 시각화

---

## 🛠 사용 기술

- Python 3.12+
- pandas, matplotlib, seaborn
- konlpy, wordcloud 등 NLP 도구

---

## 📌 참고 사항

- 분석에 사용되는 데이터 파일은 코드 내에서 상대경로 또는 지정경로로 로드됩니다.
- WordCloud 한글 출력 시 폰트 설정 확인 필요
