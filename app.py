import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# --- 1. 한글 폰트 설정 ---
font_path = os.path.join("fonts", "NanumGothic.ttf")
fontprop = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=fontprop)

# --- 2. 페이지 설정 및 타이틀 ---
st.set_page_config(page_title="보장 vs 위험 리스크 체감 시뮬레이터", layout="wide")
st.title("🧠 보장 vs 위험 리스크 체감 시뮬레이터")

# --- 3. 사용자 입력 ---
st.header("1️⃣ 고객 정보 입력")
age = st.number_input("나이", min_value=10, max_value=100, step=1)
job = st.selectbox("직업군", ["사무직", "육체노동직", "자영업", "전업주부", "학생", "기타"])
family_history = st.multiselect("가족력 (해당사항 선택)", ["고혈압", "당뇨", "뇌혈관", "심장질환", "암"])
lifestyle = st.multiselect("생활 습관", ["흡연", "음주", "운동 부족", "스트레스 많음", "야근 잦음"])

# --- 4. 리스크 점수 계산 ---
st.header("2️⃣ 리스크 점수 계산")

risk_scores = {"일반 암": 0, "뇌 혈관": 0, "허혈성 심장 질환": 0}

if age >= 40:
    risk_scores["허혈성 심장 질환"] += 2
    risk_scores["뇌 혈관"] += 2
if age >= 50:
    risk_scores["일반 암"] += 2

if "고혈압" in family_history:
    risk_scores["허혈성 심장 질환"] += 2
if "뇌혈관" in family_history:
    risk_scores["뇌 혈관"] += 3
if "암" in family_history:
    risk_scores["일반 암"] += 3

for item in lifestyle:
    if item in ["흡연", "음주", "야근 잦음"]:
        risk_scores["허혈성 심장 질환"] += 1
        risk_scores["일반 암"] += 1
    if item == "스트레스 많음":
        risk_scores["뇌 혈관"] += 2
    if item == "운동 부족":
        risk_scores["허혈성 심장 질환"] += 1

for k in risk_scores:
    risk_scores[k] = min(risk_scores[k], 10)

# --- 5. 위험도 시각화 ---
st.header("3️⃣ 예측 위험도 시각화")

labels = list(risk_scores.keys())
scores = list(risk_scores.values())

fig, ax = plt.subplots()
bars = ax.bar(labels, scores, color='darkred')
ax.set_ylim(0, 10)
ax.set_ylabel("위험 점수 (0~10)")
ax.set_title("예측 질병 위험도")
st.pyplot(fig)

# --- 6. 보장 vs 리스크 비교 시나리오 ---
st.header("4️⃣ 보장 vs 리스크 비교 시나리오")

st.info("💡 현재는 기존 보장 입력 기능이 없어 모든 위험은 '❌ 보장 없음'으로 표시됩니다.")

uncovered_risks = []

for risk in risk_scores:
    covered = "❌ 보장 없음"
    msg = f"🔍 **{risk}** 위험도 {risk_scores[risk]}/10 → {covered}"
    st.markdown(msg)
    if risk_scores[risk] >= 7:
        uncovered_risks.append(risk)
        st.warning("⚠️ 이 위험은 현재 보장되지 않고 있습니다. 대비가 필요해 보입니다.")

if uncovered_risks:
    st.markdown("---")
    st.subheader("❓ '이걸 막으려면 어떻게 해야 하죠?' 라는 질문이 드시나요?")
    st.markdown("📌 필요한 보장에 대해 함께 알아볼 수 있도록 도와드릴게요.")
