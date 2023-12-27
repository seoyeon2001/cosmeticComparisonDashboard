import streamlit as st
import pandas as pd

### 파일 읽어오기
def read_data(file):
    raw = pd.read_csv(file)
    return raw

tab1, tab2, tab3, tab4 = st.tabs(["상품 필터링", "상품 고르기", "상품 비교하기", "서비스 소개"])

### 데이터 읽어오기
raw = read_data('./raw.csv')

with tab1:
    ### 카테고리 선택
    category = st.columns(3)

    with category[0]: # 중분류 선택
        select_middle_category = st.selectbox('중분류', ['베이스메이크업','아이메이크업', '립메이크업'])
        middle = raw[raw['중분류'] == select_middle_category]

    with category[1]: # 소분류 선택
        if select_middle_category == '베이스메이크업':
            select_detail_category = st.selectbox('소분류', ['컨실러', '쿠션', '파운데이션', '메이크업픽서', '파우더'])
            detail = middle[middle['소분류'] == select_detail_category]

        elif select_middle_category == '아이메이크업':
            select_detail_category = st.selectbox('소분류', [ '아이브로우', '아이라이너', '아이섀도우/팔레트', '마스카라'])
            detail = middle[middle['소분류'] == select_detail_category]

        elif select_middle_category == '립메이크업':
            select_detail_category = st.selectbox('소분류', ['립에센스/립밤', '립글로스', '립펜슬/립라이너', '립틴트/락커'])
            detail = middle[middle['소분류'] == select_detail_category]

    ### 범위 선택
    slider1 = st.columns(2)
    with slider1[0]:
        slider_range_price = st.slider("판매 금액의 범위를 설정하세요", detail['판매가격'].min(), detail['판매가격'].max(), 
                                (detail['판매가격'].min(), detail['판매가격'].max()))
    with slider1[1]:
        slider_range_sale = st.slider("할인율의 범위를 설정하세요", detail['할인율'].min(), detail['할인율'].max(), 
                                (detail['할인율'].min(), detail['할인율'].max()))

    slider2 = st.columns(2)
    with slider2[0]:
        slider_range_star = st.slider("별점의 범위를 설정하세요", detail['별점'].min(), detail['별점'].max(), 
                                (detail['별점'].min(), detail['별점'].max()))
    with slider2[1]:
        slider_range_review = st.slider("리뷰 개수의 범위를 설정하세요", detail['리뷰수'].min(), detail['리뷰수'].max(), 
                                (detail['리뷰수'].min(), detail['리뷰수'].max()))

    # 필터 적용버튼
    start_button = st.button("필터 적용하기")

    ### 필터링
    if start_button:
        filtering = detail[ (detail['판매가격'] >= slider_range_price[0]) & (detail['판매가격'] <= slider_range_price[1]) 
                      & (detail['할인율'] >= slider_range_sale[0]) & (detail['할인율'] <= slider_range_sale[1])
                      & (detail['별점'] >= slider_range_star[0]) & (detail['별점'] <= slider_range_star[1]) 
                      & (detail['리뷰수'] >= slider_range_review[0]) & (detail['리뷰수'] <= slider_range_review[1]) ]

        # 성공문구 + 풍선이 날리는 특수효과 
        st.success("필터 적용 성공!")
        st.balloons() # 확인용

    try:
        ### 필터링한 상품 csv파일 만들기
        filtering.to_csv("filtering.csv", index=False)
    except:
        pass

    ### 필터링한 데이터 파일 가져오기
    filter_item = read_data('./filtering.csv')

    st.dataframe(filter_item)
    

with tab2:
    if 'tmp' not in st.session_state:
        st.session_state.tmp = []  
    
    # 상품 데이터
    st.markdown("<p style='text-align:center'>" + '최대 3개까지 선택 가능합니다!' + "</p>", unsafe_allow_html=True)

    for j in range(len(filter_item)//3+1):
        images = st.columns(3)
        for i in range(3):
            try:
                with images[i]:                    
                    check = st.columns(2)

                    with check[0]:
                        st.write("<p style='text-align:center'>" + filter_item.iloc[i+3*j , 1] + "</p>", unsafe_allow_html=True)

                    with check[1]:
                        button_list = st.button('선택 ' + str(i+3*j))

                        if button_list:
                            st.session_state.tmp.append(i+3*j)

                    value = filter_item.iloc[i+3*j, 0]
                    st.image(value, caption=filter_item.iloc[i+3*j, 2])            
            except: 
                pass 

    # 중복 제거
    result = []
    
    for tmp in st.session_state.tmp:
        if tmp not in result:
            result.append(tmp)

    if len(result) > 3:
        result = result[-3:]
    else:
        result = result

    st.write(result)

    # 비교 상품 csv파일 만들기
    comparison = filter_item.loc[result]
    comparison.to_csv("comparison.csv", index=False)


with tab3:
    ### 데이터 읽어오기
    cp = read_data('./comparison.csv')

    ### 카테고리 보여주기
    st.header(select_middle_category + "의  " + select_detail_category + " 상품 카테고리", divider='rainbow')


    ### 선택한 상품이 2개일 때 보여주기
    if len(cp) == 2:
        item = st.columns(2)

        for i in range(2):
            
            with item[i]:
                st.markdown("<p style='text-align:center'>" + cp['브랜드'][i] + "</p>", unsafe_allow_html=True)
                st.image(cp['이미지 주소'][i])
                st.markdown("<p style='text-align:center'>" + cp['상품명'][i] + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 판매 가격: " + str(cp['판매가격'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 할인율: " + str(cp['할인율'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 리뷰수: " + str(cp['리뷰수'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 별점: " + str(cp['별점'][i]) + "</p>", unsafe_allow_html=True)

                with st.expander("상품 상세 이미지 확인하기"):
                    image_list = cp['상품 상세 이미지'][i]
                    image_list = image_list.replace("'", "")[1:-1].split(', ')
                    for value in image_list:
                        st.image(image_list)

    ### 선택한 상품이 3개일 때 보여주기
    elif len(cp) == 3:
        item = st.columns(3)

        for i in range(3):

            with item[i]:
                st.markdown("<p style='text-align:center'>" + cp['브랜드'][i] + "</p>", unsafe_allow_html=True)
                st.image(cp['이미지 주소'][i])
                st.markdown("<p style='text-align:center'>" + cp['상품명'][i] + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 판매 가격: " + str(cp['판매가격'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 할인율: " + str(cp['할인율'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 리뷰수: " + str(cp['리뷰수'][i]) + "</p>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'> 별점: " + str(cp['별점'][i]) + "</p>", unsafe_allow_html=True)

                with st.expander("상품 상세 이미지 확인하기"):
                    image_list = cp['상품 상세 이미지'][i]
                    image_list = image_list.replace("'", "")[1:-1].split(', ')
                    for value in image_list:
                        st.image(image_list)

with tab4:
    st.markdown('<h1>타겟 대상</h1>', unsafe_allow_html=True)
    st.markdown('<ol><li>대학생 창업 투자 전문 회사<br>- 중소벤처기업부에서 시행하는 청년전용창업자금 사업에 참여한 기업</li><li>메이크업이 없는 쇼핑몰 회사<br>- 브랜디의 마케팅팀</li></ol>', unsafe_allow_html=True)
    
    st.markdown('<h1>사용 방법</h1>', unsafe_allow_html=True)
    st.markdown('''<ol><li>상품 필터링에서 중분류와 소분류를 선택한다.</li>
                <li>원하는 범위를 설정한다.</li>
                <li>필터 적용하기 버튼을 클릭한다.</li>
                <li>풍선이 나오면 성공</li>
                <li>상품 고르기 탭으로 넘어간다.</li>
                <li>원하는 상품을 최소 2개 최대 3개를 선택한다.</li>
                <li>상품 비교하기 탭으로 넘어간다.</li>
                <li>선택한 상품을 비교한다.</li></ol>
                ''', unsafe_allow_html=True)
    
    st.markdown('<h1>활용 의미</h1>', unsafe_allow_html=True)
    st.markdown('''
                카드고릴라와 같이 카드는 혜택이나 연회비 등에 따라 원하는 조건과 혜택을 한눈에 확인할 수 있는 사이트가 존재한다. 
                그러나 화장품의 경우 한눈에 두 개 이상의 상품을 확인할 수 있는 사이트가 존재하지 않다.
                한눈에 비교하기 위해서는 여러 창의 띄워야하는 단점이 존재한다. 따라서 이러한 부분에서 문제점을 느끼고 해결하기 위한 서비스를 만들었다.
                <br><br>
                해당 서비스 사용을 통하여 여러 창의 띄울 필요가 없으며, 한눈에 비교할 수 있다는 장점이 있다. 
                또한, 과정이 복잡하지 않아 한 번의 사용으로 사용 방법을 파악할 수 있다.
                ''', unsafe_allow_html=True)
    
    st.markdown('<h1>데이터 수집</h1>', unsafe_allow_html=True)
    st.markdown('<p><b>사이트</b>: https://chicor.com/main</p>', unsafe_allow_html=True)
    st.markdown('<p><b>크롤링한 정보</b>: 이미지 url, 브랜드명, 상품명, 판매가격, 원가, 할인율, 리뷰 수, 리뷰 점수</p>', unsafe_allow_html=True)
    st.markdown('<p><b>유의사항</b>: 데이터의 양이 많아 처음에 오류가 한번 발생한다. 이 문제는 다시 실행하면 해결이 가능하다.</p>', unsafe_allow_html=True)


