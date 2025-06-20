import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 페이지 설정
st.set_page_config(page_title="보장 vs 위험 리스크 체감 시뮬레이터", layout="wide")
st.title("🧠 보장 vs 위험 리스크 체감 시뮬레이터")

# ----------------------------------------
st.header("1️⃣ 고객 정보 입력")
age = st.number_input("나이", min_value=10, max_value=100, step=1)
job = st.selectbox("직업군", ["사무직", "육체노동직", "자영업", "전업주부", "학생", "기타"])
family_history = st.multiselect("가족력 (해당사항 선택)", ["고혈압", "당뇨", "뇌혈관", "심장질환", "암"])
lifestyle = st.multiselect("생활 습관", ["흡연", "음주", "운동 부족", "스트레스 많음", "야근 잦음"])

# ----------------------------------------
st.header("2️⃣ 기존 보장 파일 업로드 (.xlsx)")
uploaded_file = st.file_uploader("보장 요약 파일을 업로드 해주세요", type=["xlsx"])

# ✅ 분석 대상 보장 항목 정의 (단 3개만)
coverage_keywords = {
    "일반 암": ["일반암"],
    "뇌 혈관": ["뇌혈관"],
    "허혈성 심장 질환": ["허혈성"]
}

existing_coverage = []
matched_summary = {}

# ✅ 보장 항목 자동 분석 및 금액 합산
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ 파일 업로드 완료. 보장 항목 자동 분석 중...")

    df_str = df.astype(str)

    for row_idx, row in df_str.iterrows():
        for col_idx, cell in enumerate(row):
            for label, keywords in coverage_keywords.items():
                if any(k in cell for k in keywords):
                    if col_idx > 0:
                        try:
                            left_val_raw = df.iloc[row_idx, col_idx - 1]
                            left_val = float(str(left_val_raw).replace(",", "").replace("원", "").strip())
                            matched_summary.setdefault(label, []).append(left_val)
                        except:
                            pass

    # 감지된 항목 요약 출력
    existing_coverage = list(matched_summary.keys())

    if existing_coverage:
        st.subheader("🧾 감지된 보장 항목 요약")
        for label in ["일반 암", "뇌 혈관", "허혈성 심장 질환"]:
            total = int(sum(matched_summary.get(label, [])))
            count = len(matched_summary.get(label, []))
            if count > 0:
                st.markdown(f"🔍 **{label}** → 합계: `{total:,}원` / 건수: `{count}건`")
    else:
        st.warning("❗ 지정한 보장 항목이 감지되지 않았습니다.")

# ----------------------------------------
st.header("3️⃣ 리스크 점수 계산")

risk_scores = {"일반 암": 0, "뇌 혈관": 0, "허혈성 심장 질환": 0}

# 나이 기반
if age >= 40:
    risk_scores["허혈성 심장 질환"] += 2
    risk_scores["뇌 혈관"] += 2
if age >= 50:
    risk_scores["일반 암"] += 2

# 가족력
if "고혈압" in family_history:
    risk_scores["허혈성 심장 질환"] += 2
if "뇌혈관" in family_history:
    risk_scores["뇌 혈관"] += 3
if "암" in family_history:
    risk_scores["일반 암"] += 3

# 생활습관
for item in lifestyle:
    if item in ["흡연", "음주", "야근 잦음"]:
        risk_scores["허혈성 심장 질환"] += 1
        risk_scores["일반 암"] += 1
    if item == "스트레스 많음":
        risk_scores["뇌 혈관"] += 2
    if item == "운동 부족":
        risk_scores["허혈성 심장 질환"] += 1

# 최대 10점 제한
for k in risk_scores:
    risk_scores[k] = min(risk_scores[k], 10)

# ----------------------------------------
st.header("4️⃣ 예측 위험도 시각화")

labels = list(risk_scores.keys())
scores = list(risk_scores.values())

fig, ax = plt.subplots()
bars = ax.bar(labels, scores, color='darkred')
ax.set_ylim(0, 10)
ax.set_ylabel("위험 점수 (0~10)")
ax.set_title("예측 질병 위험도")
st.pyplot(fig)

# ----------------------------------------
st.header("5️⃣ 보장 vs 리스크 비교 시나리오")

uncovered_risks = []

for risk in risk_scores:
    covered = "✅ 보장 있음" if risk in existing_coverage else "❌ 보장 없음"
    msg = f"🔍 **{risk}** 위험도 {risk_scores[risk]}/10 → {covered}"
    st.markdown(msg)
    if risk_scores[risk] >= 7 and risk not in existing_coverage:
        uncovered_risks.append(risk)
        st.warning("⚠️ 이 위험은 현재 보장되지 않고 있습니다. 대비가 필요해 보입니다.")

if uncovered_risks:
    st.markdown("---")
    st.subheader("❓ '이걸 막으려면 어떻게 해야 하죠?' 라는 질문이 드시나요?")
    st.markdown("📌 필요한 보장에 대해 함께 알아볼 수 있도록 도와드릴게요.")
