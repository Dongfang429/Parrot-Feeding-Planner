#神秘代码1号(Type in Terminal first)：python -m pip install streamlit

#神秘代码2号(Type in Terminal next)：python -m streamlit run ParrotHthy.py

import streamlit as st

st.set_page_config(page_title="Avian Feeding Planner", layout="centered")

st.title("🦜 Parrot Feeding Planner / 鹦鹉喂食规划器")
st.caption("A rational feeding estimation tool for companion parrots")

st.divider()

# ----------------------------
# Inputs
# ----------------------------
weight_g = st.number_input("Body weight (g) / 体重(克)", min_value=30, max_value=2000, value=150)

goal = st.selectbox(
    "Feeding goal / 目标",
    ["Maintain / 维持", "Gain / 增重", "Lose / 减脂"]
)

activity = st.selectbox(
    "Activity level / 活动量",
    ["Low / 低", "Normal / 中等", "High / 高"]
)

# ----------------------------
# 🔧 Key assumptions 关键参数 (editable可调整)
# ----------------------------
with st.expander("🔧 Assumptions you can adjust / 可调参数", expanded=True):
    # 🔧 ”K“ factor for parrots 鹦鹉类公式常数”K“ (默认 175 default 175)
    K_psittacine = st.number_input("🔧 K factor (psittacine default = 175) / K常数（默认175）",
                                   min_value=50, max_value=300, value=175, step=5)

    # 🔧 Food energy density 鸟粮能量密度 (千卡每克 kcal/g)
    pellet_kcal_per_g = st.number_input("🔧 Food energy density (kcal/g) / 食物热量 (kcal/克) （默认3.5左右，特殊情况可调整）",
                                        min_value=2.0, max_value=6.0, value=3.53, step=0.05)

    st.caption("📌 Example reference: Tropican Lifetime Formula lists 3,528 kcal/kg ≈ 3.528 kcal/g.")

# ----------------------------
# 🧮 Energy calculation 能量计算
# ----------------------------
weight_kg = weight_g / 1000.0

# 🧮 计算公式：BER = K * (W_kg ^ 0.75) 
BER = K_psittacine * (weight_kg ** 0.75)

# Activity multiplier
if activity.startswith("Low"):
    act_mult = 1.15
elif activity.startswith("Normal"):
    act_mult = 1.30
else:
    act_mult = 1.50

MER = BER * act_mult  # Maintenance-ish estimate

# Goal multiplier (range output)
if goal.startswith("Maintain"):
    goal_low, goal_high = 0.95, 1.05
elif goal.startswith("Gain"):
    goal_low, goal_high = 1.10, 1.20
else:
    goal_low, goal_high = 0.80, 0.90

kcal_low = MER * goal_low
kcal_high = MER * goal_high

# ----------------------------
# Convert kcal -> grams of Food
# ----------------------------
pellet_g_low = kcal_low / pellet_kcal_per_g
pellet_g_high = kcal_high / pellet_kcal_per_g

# Diet portion suggestion (simple, adjustable later)
pellet_ratio_low, pellet_ratio_high = 0.70, 0.80

# If Formula are 70-80% of total diet by weight (rough heuristic):
# total_food_g ≈ pellet_g / pellet_ratio
total_food_g_low = pellet_g_low / pellet_ratio_high
total_food_g_high = pellet_g_high / pellet_ratio_low

st.subheader("📊 Recommended Daily Intake / 推荐每日摄入")

st.write(f"Detected size / 体型： **{'Small' if weight_g <= 120 else 'Medium' if weight_g <= 400 else 'Large'}**")
st.write(f"**Energy:** {kcal_low:.0f} – {kcal_high:.0f} kcal/day")
st.write(f"**Formula (if 100% Formula):** {pellet_g_low:.1f} – {pellet_g_high:.1f} g/day")

st.write(f"**Formula portion suggestion:** ~{int(pellet_ratio_low*100)}–{int(pellet_ratio_high*100)}% of diet")
st.write(f"**Estimated total food (rough):** {total_food_g_low:.1f} – {total_food_g_high:.1f} g/day")

st.info(
    "📌 This tool is a starting estimate.\n"
    "Monitor weight weekly. If weight changes >5% within ~2 weeks, adjust feeding and consult an avian vet."
)

with st.expander("🧾 What numbers were used? / 计算里用了哪些关键数值？"):
    st.write(f"🧮 BER = K × (W_kg^0.75)")
    st.write(f"🔧 K = {K_psittacine}")
    st.write(f"🔧 Activity multiplier = {act_mult}")
    st.write(f"🔧 Formula energy density = {pellet_kcal_per_g} kcal/g")

st.caption("⚠️ Prototype for educational and planning purposes only. Not a substitute for veterinary advice.")
