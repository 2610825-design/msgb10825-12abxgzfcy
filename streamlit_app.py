import streamlit as st

# 스트림릿 페이지 설정
st.set_page_config(page_title="용돈 관리 앱", page_icon="💰", layout="centered")

# ========================================
# 1. 초기화 (st.session_state)
# ========================================
# 웹 페이지가 새로고침되어도 데이터가 날아가지 않도록 상태를 저장합니다.
if "initial_money" not in st.session_state:
    st.session_state.initial_money = 0
if "money" not in st.session_state:
    st.session_state.money = 0
if "expense_list" not in st.session_state:
    st.session_state.expense_list = []
if "is_started" not in st.session_state:
    st.session_state.is_started = False

# ========================================
# 2. 화면 UI 구성
# ========================================
st.title("💰 용돈 관리 프로그램")

# [초기화 단계] 처음 용돈 설정
if not st.session_state.is_started:
    init_money = st.number_input(
        "현재 가지고 있는 용돈을 입력하세요:", min_value=0, step=100, value=10000
    )
    if st.button("용돈 설정 완료"):
        st.session_state.initial_money = init_money
        st.session_state.money = init_money
        st.session_state.is_started = True
        st.rerun()  # 화면 갱신

# [지출 입력 단계] 용돈이 설정된 후 실행
else:
    # 현재 잔액 상단 표시
    st.metric(label="💵 현재 남은 용돈", value=f"{st.session_state.money}원")

    # 사용 금액 입력 폼 (Enter 또는 버튼 클릭 시 제출)
    with st.form(key="expense_form", clear_on_submit=True):
        expense = st.number_input(
            "사용한 금액을 입력하세요 (0을 입력하고 제출하면 최종 결산):",
            min_value=0,
            step=100,
        )
        submit_button = st.form_submit_with_no_mt_id = st.form_submit_button(
            label="지출 기록하기"
        )

    # 지출 버튼이 눌렸을 때 로직 수행 (기존 while문 내부 조건문과 동일)
    if submit_button:
        # 조건문1: 0을 입력하면 프로그램 종료 (가상)
        if expense == 0:
            st.toast("💡 지출 입력을 종료했습니다.")

        # 조건문2: 잔액이 충분한지 확인
        elif st.session_state.money >= expense:
            st.session_state.expense_list.append(expense)  # 지출 리스트에 추가
            st.session_state.money -= expense  # 잔액 차감
            st.success(f"💰 [성공] {expense}원이 차감되었습니다.")
        else:
            st.error(
                f"❌ [경고] 용돈이 부족합니다! 금액을 다시 확인해주세요.\n현재 남은 용돈: {st.session_state.money}원"
            )

    # 처음부터 다시 시작하고 싶을 때 사용하는 리셋 버튼
    if st.button("🔄 처음부터 다시 입력하기"):
        st.session_state.clear()
        st.rerun()

    # ----------------------------------------
    # 3. 최종 결과 출력 (화면에 실시간으로 누적 표시)
    # ----------------------------------------
    st.markdown("---")
    st.subheader("📊 최종 용돈 관리 결산")

    st.write(f"**💵 최종 남은 용돈 금액:** {st.session_state.money}원")
    st.write("**📉 상세 지출 내역:**")

    # 만약 지출 내역이 비어있다면 안내 문구 출력
    if not st.session_state.expense_list:
        st.info(" - 지출 내역이 없습니다.")
    else:
        # 에러가 나던 item 부분을 반복문(for)으로 해결하여 전체 내역 출력
        for idx, item in enumerate(st.session_state.expense_list, 1):
            st.write(f"&nbsp;&nbsp;{idx}. 지출금액: {item}원")