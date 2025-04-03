# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 12:41:23 2025

@author: Roh Jun Seok
"""
'''
카드 소비 데이터 분석 : bc_card.txt : 원본 데이터 (2019.6 전체 소비 데이터의 일부)

1. 데이터 로드 및 전처리
2. 데이터프레임 형식으로 저장
3. 데이터 분석

1. 서울시 거주/비거주 고객의 소비 분석
- 서울시 거주/비거주 고객 수 구하기
- 총 소비액 구하기
- 성별 소비액 구하기
- 카드 이용 건수 구하기

2. 편의점 소비 정보 분석
- 편의점 소비액 구하기
- 강남구 편의점 소비액 분석

3. 서울시 거주 고객의 소비액 / 비거주 고객의 소비액 구하기
4. 거주지 소재 편의점 소비액 구하기
'''
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('./data/bc_card_data/bc_card_out2020_03.txt', 
                 sep='\t', 
                 engine='python',
                 encoding='utf-8')

df.columns
'''
['REG_YYMM', 'MEGA_CTY_NO', 'MEGA_CTY_NM', 'CTY_RGN_NO', 'CTY_RGN_NM',
 'ADMI_CTY_NO', 'ADMI_CTY_NM', 'MAIN_BUZ_CODE', 'MAIN_BUZ_DESC',
 'TP_GRP_NO', 'TP_GRP_NM', 'TP_BUZ_NO', 'TP_BUZ_NM', 'CSTMR_GUBUN',
 'CSTMR_MEGA_CTY_NO', 'CSTMR_MEGA_CTY_NM', 'CSTMR_CTY_RGN_NO',
 'CSTMR_CTY_RGN_NM', 'SEX_CTGO_CD', 'AGE_VAL', 'FLC', 'AMT', 'CNT']
'''

'''
REG_YYMM: 연월
MEGA_CTY_NO: 이용지역 시도 코드 (가맹점주소 기준)
MEGA_CTY_NM: 이용지역 시도명 (가맹점주소 기준)
CTY_RGN_NO: 이용지역 시군구 코드 (가맹점주소 기준)
CTY_RGN_NM: 이용지역 시군구명 (가맹점주소 기준)
ADMI_CTY_NO: 이용지역 법정동코드 (가맹점주소 기준)
ADMI_CTY_NM: 이용지역 법정동명 (가맹점주소 기준)
MAIN_BUZ_CODE: 업종 분류 코드
MAIN_BUZ_DESC: 업종 분류명
TP_GRP_NO: 업종 그룹 코드
TP_GRP_NM: 업종 그룹명
TP_BUZ_NO: 세부 업종 코드
TP_BUZ_NM: 세부 업종명
CSTMR_GUBUN: 고객 구분(내국인 뿐)
CSTMR_MEGA_CTY_NO: 고객 거주지 시도 코드
CSTMR_MEGA_CTY_NM: 고객 거주지 시도명
CSTMR_CTY_RGN_NO: 고객 거주지 시군구 코드
CSTMR_CTY_RGN_NM: 고객 거주지 시군구명
SEX_CTGO_CD: 성별(1: 남성, 2: 여성)
AGE_VAL: 연령대
FLC: 고객 생애주기
AMT: 이용 금액 (이용 금액 합계)
CNT: 이용 건수 (이용 건수 합계)
'''

df.info()
df.describe()

df['CSTMR_CTY_RGN_NM'].value_counts()

#--- 1. 데이터 전처리
#--- 1-1. 결측치 및 중복 데이터 처리
df.isnull().sum()
# 결측치는 없음
df.shape
# (1589494, 23)

df = df.drop_duplicates()
df.shape
# (1589494, 23)
# 중복 데이터도 없음

#--- 1-2. 데이터 타입 변환
# REG_YYMM을 문자열로 변환
df['REG_YYMM'] = df['REG_YYMM'].astype(str)

#--- 1-3. 문자열 데이터 정제
# 주요 문자열 컬럼의 앞뒤 공백 제거
str_columns = ['CSTMR_MEGA_CTY_NM', 'MEGA_CTY_NM', 'CTY_RGN_NM', 
               'CSTMR_CTY_RGN_NM', 'TP_BUZ_NM', 'MAIN_BUZ_DESC', 'TP_GRP_NM']

for col in str_columns:
    df[col] = df[col].str.replace(' ', '')

#--- 1-4. 범주형 변수 및 파생 변수 생성
# 성별 변수 매핑
gender_map = {1: '남성', 2: '여성'}
df['SEX'] = df['SEX_CTGO_CD'].map(gender_map)

# 서울시 거주 여부 파생 변수 생성
df['CST_seoul'] = df['CSTMR_MEGA_CTY_NM'] == '서울특별시'

# FLC 컬럼의 값 분포 확인
df['FLC'].unique()

# 2. 서울시 거주/비거주 고객의 소비 분석

# 2-1. 서울시 거주/비거주 고객 수 구하기
df['CST_seoul'].value_counts()

customer_count = df.groupby('CST_seoul').size()
customer_count

print(f'서울시에 거주하는 고객 수는 총 {customer_count.iloc[1]}명, 비거주 고객 수는 {customer_count.iloc[0]}명입니다.')
print(f'비율은 각각 거주 고객 수가 약 {customer_count.iloc[1]/len(df)*100:.2f}%, 비거주 고객 수는 약 {customer_count.iloc[0]/len(df)*100:.2f}%를 차지하고 있습니다.')
'''
서울시에 거주하는 고객 수는 총 901072명, 비거주 고객 수는 688422명입니다.
비율은 각각 거주 고객 수가 약 56.69%, 비거주 고객 수는 약 43.31%를 차지하고 있습니다.
'''

# 2-2. 총 소비액 구하기
total_amt = df.groupby('CST_seoul')['AMT'].sum()
print(f'총 소비액은 서울시 거주 고객이 총 {total_amt.iloc[1]}원, 비거주 고객이 총 {total_amt.iloc[0]}원 소비한 것으로 확인됩니다.')
'''
총 소비액은 서울시 거주 고객이 총 1,385,914,569,631원, 
비거주 고객이 총 1,940,899,349,900원 소비한 것으로 확인됩니다.
'''

# 2-3. 성별 소비액 구하기
sex_amt = df.groupby(['CST_seoul', 'SEX'])['AMT'].sum()
print(f'성별 소비액은 서울시 거주 고객 중 남성의 경우가 총 {sex_amt.iloc[2]}원, 여성의 경우가 총 {sex_amt.iloc[3]}원 소비한 것으로 확인되며,')
print(f'비거주 고객 중 남성의 경우에는 총 {sex_amt.iloc[0]}원, 여성의 경우가 총 {sex_amt.iloc[1]}원 소비한 것으로 나타났습니다.')
'''
성별 소비액은 서울시 거주 고객 중 남성의 경우가 총 682,678,945,342원, 여성의 경우가 총 703,235,624,289원 소비한 것으로 확인되며,
비거주 고객 중 남성의 경우에는 총 1,015,425,463,575원, 여성의 경우가 총 925,473,886,325원 소비한 것으로 나타났습니다.
'''

# 2-4. 카드 이용 건수 구하기
total_cnt = df.groupby('CST_seoul')['CNT'].sum()
print(f'카드 이용 건수는 서울시 거주 고객이 총 {total_cnt.iloc[1]}건, 비거주 고객이 총 {total_cnt.iloc[0]}건 이용한 것으로 확인됩니다.')
'''
카드 이용 건수는 서울시 거주 고객이 총 58,970,629건, 
비거주 고객이 총 53,351,160건 이용한 것으로 확인됩니다.
'''

# 3. 편의점 소비 정보 분석
# 편의점 거래 내역 추출
convenience = df[df['TP_BUZ_NM'] == '편의점']

# 3-1. 편의점 소비액 구하기
convenience_amt = convenience['AMT'].sum()
print(f'편의점에서 소비된 금액은 총 {convenience_amt}원으로 나타납니다.')
'''
편의점에서 소비된 금액은 총 79,987,167,291원으로 나타납니다.
'''

# 3-2. 강남구 편의점 소비액
gangnam_convenience = convenience[convenience['CTY_RGN_NM'] == '강남구']
gangnam_convenience_amt = gangnam_convenience['AMT'].sum()
print(f'강남구 편의점에서 소비된 금액은 총 {gangnam_convenience_amt}원으로 나타납니다.')
'''
강남구 편의점에서 소비된 금액은 총 8,170,947,461원으로 나타납니다.
'''

# 3. 서울시 거주 고객과 비거주 고객의 소비액 비교
total_amt = df.groupby('CST_seoul')['AMT'].sum()
print(f'총 소비액은 서울시 거주 고객이 총 {total_amt.iloc[1]}원, 비거주 고객이 총 {total_amt.iloc[0]}원 소비한 것으로 확인됩니다.')
'''
총 소비액은 서울시 거주 고객이 총 1,385,914,569,631원, 
비거주 고객이 총 1,940,899,349,900원 소비한 것으로 확인됩니다.
'''

# 4. 거주지 소재 편의점 소비액 구하기

# 고객의 거주지와 가맹점 위치가 동일한 경우:
# - 고객 시도와 가맹점 시도 비교: CSTMR_MEGA_CTY_NM vs MEGA_CTY_NM
# - 고객 시군구와 가맹점 시군구 비교: CSTMR_CTY_RGN_NM vs CTY_RGN_NM
convenience_local = convenience[
    (convenience['CSTMR_MEGA_CTY_NM'] == convenience['MEGA_CTY_NM']) &
    (convenience['CSTMR_CTY_RGN_NM'] == convenience['CTY_RGN_NM'])
]
local_convenience_amt = convenience_local['AMT'].sum()
print(f'고객의 거주지와 가맹점의 위치가 동일한 경우, 편의점 소비액은 총 {local_convenience_amt}원입니다.')
'''
고객의 거주지와 가맹점의 위치가 동일한 경우, 편의점 소비액은 총 44,184,614,834원입니다.
'''

#--- 5. 시각화
plt.figure()
plt.boxplot(df['AMT'])
plt.title("AMT 박스플롯")
plt.xlabel("AMT")
plt.ylabel("값")
plt.show()

df['AMT'].max()
# 1,689,312,273

plt.style.use('seaborn-v0_8-pastel')

# 1. 서울시 거주/비거주별 총 소비액 플롯
residence_labels = ['비거주', '거주']
residence_amt = [total_amt.iloc[0], total_amt.iloc[1]]
colors = ['skyblue', 'salmon']  # 각 그룹을 위한 색상 지정

plt.figure(figsize=(8, 6))
bars = plt.bar(residence_labels, residence_amt, color=colors, edgecolor='black', width=0.8)
plt.title("서울시 거주/비거주별 총 소비액", fontsize=16)
plt.xlabel("거주 여부", fontsize=14)
plt.ylabel("총 소비액 (원)", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 각 막대 위에 값 표시 (천 단위 구분기호 포함)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height*1.005, f'{height:,.0f}원', 
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()

# 2. 서울시 거주 고객 성별 소비액 플롯
# 성별 소비액은 그룹화 결과에서 거주(True) 부분만 추출
residents_sex_amt = sex_amt.loc[True]
labels = list(residents_sex_amt.index)
values = residents_sex_amt.values
# 남성과 여성에 대해 다른 색상 적용
sex_colors = ['cornflowerblue', 'lightpink']

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values, color=sex_colors, edgecolor='black', width=0.8)
plt.title("서울시 거주 고객 성별 소비액", fontsize=16)
plt.xlabel("성별", fontsize=14)
plt.ylabel("소비액 (원)", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height*1.005, f'{height:,.0f}원', 
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()

# 3. 편의점 소비액 비교 (전체 vs 강남구)
labels = ['전체 편의점', '강남구 편의점']
values = [convenience_amt, gangnam_convenience_amt]
comp_colors = ['mediumpurple', 'gold']

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values, color=comp_colors, edgecolor='black', width=0.8)
plt.title("편의점 소비액 비교", fontsize=16)
plt.xlabel("구분", fontsize=14)
plt.ylabel("편의점 소비액 (원)", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height*1.005, f'{height:,.0f}원', 
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()

# 전체 편의점 소비액과 강남구 편의점 소비액
# non_gangnam_amt는 전체 소비액에서 강남구 소비액을 뺀 값입니다.
non_gangnam_amt = convenience_amt - gangnam_convenience_amt

# 도넛 차트를 위한 데이터: 강남구 소비액과 기타(전체 - 강남구) 소비액
pie_labels = ['강남구 편의점', '기타 편의점']
pie_values = [gangnam_convenience_amt, non_gangnam_amt]
pie_colors = ['mediumpurple', 'palegoldenrod']

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(pie_values, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%',
                                   startangle=90, textprops={'fontsize': 12})

# 가운데에 원을 그려 도넛 형태로 변환
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("편의점 소비액 중 강남구 편의점 비중", fontsize=16)
plt.tight_layout()
plt.show()

# 비거주지 소재 소비액 계산 (전체 편의점 소비액 - 거주지 소재 소비액)
non_local_amt = convenience_amt - local_convenience_amt

# 데이터 구성: 두 그룹의 실제 소비액
labels = ['거주지 소재 소비액', '비거주지 소재 소비액']
values = [local_convenience_amt, non_local_amt]

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values, color=['mediumseagreen', 'lightskyblue'], 
               edgecolor='black', width=0.8)
plt.title("거주지 소재 vs 비거주지 소재 편의점 소비액", fontsize=16)
plt.xlabel("소비 유형", fontsize=14)
plt.ylabel("소비액 (원)", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 각 막대 위에 실제 소비액을 표시 (천 단위 구분기호 추가)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height * 1.005, f'{height:,.0f}원',
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()


# 전체 편의점 소비액 대비 거주지 소재 소비액의 비율 계산 (백분율)

import matplotlib.pyplot as plt

local_pct = local_convenience_amt / convenience_amt * 100
non_local_pct = 100 - local_pct

fig, ax = plt.subplots(figsize=(10, 2))
# 거주지 소재 소비액 (왼쪽 부분)
ax.barh(0, local_pct, color='mediumseagreen', edgecolor='black', height=0.5, label='거주지 소재 소비액')
# 비거주지 소재 소비액 (오른쪽 부분)
ax.barh(0, non_local_pct, left=local_pct, color='lightskyblue', edgecolor='black', height=0.5, label='비거주지 소재 소비액')

ax.set_xlim(0, 100)
ax.set_title("전체 편의점 소비액 대비 거주지 소재 소비액 비율", fontsize=16)
ax.set_xlabel("비율 (%)", fontsize=14)
ax.set_yticks([])  # y축 눈금 제거

# 각 부분에 백분율 값 표시
ax.text(local_pct / 2, 0, f'{local_pct:.1f}%', va='center', ha='center', fontsize=12, color='black')
ax.text(local_pct + non_local_pct / 2, 0, f'{non_local_pct:.1f}%', va='center', ha='center', fontsize=12, color='black')

# 범례를 축 밖, 아래쪽에 배치하고, 여백을 확보
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2)

# tight_layout를 사용하되, rect 인자로 하단 여백 확보 (여기서는 하단 15% 확보)
plt.tight_layout(rect=[0, 0.15, 1, 1])
plt.show()












































