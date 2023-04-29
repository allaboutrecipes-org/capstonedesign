import pandas as pd
import folium
from haversine import haversine
import requests
from urllib.parse import quote
import webbrowser

pd.set_option('mode.chained_assignment',  None)

def Calculate_location():
    addr = input('현재 위치의 도로명 주소를 입력해주세요!:')
    
    kakao_key = "472dabcffea1b9dd890b49b2a3758fba"
    local_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{local_url}?query={quote(addr)}'
    result = requests.get(url, headers = {"Authorization":f"KakaoAK {kakao_key}"}).json()
    
    x1 = float(result['documents'][0]['y'])
    y1 = float(result['documents'][0]['x'])
    user_coord = (x1,y1)
    print('현재 위치는 :', user_coord)
    
    Market = pd.read_csv('C:\\Python_VScode\\OpenSourceProject\\Final_location.csv',encoding='CP949')
    
    market = Market[['위도','경도']]
    market_mark = market[['위도','경도']].values[:len(market)].tolist()
    
    m = folium.Map(location=[x1, y1], zoom_start=15)
    folium.Marker(location=[x1, y1], popup="현재 위치", icon=folium.Icon(color="red", icon="star")).add_to(m)
    
    for i in range(len(market)):
        folium.Circle(location = market_mark[i],radius=20,color='blue',fill=True).add_to(m)
    m.save('C:\\Python_VScode\\OpenSourceProject\\map.html')
    
    order = int(0)
    distance = list()
    market_name = list()
    while order < 100 :
        market_lat = float(Market.loc[order,'위도'])
        market_long = float(Market.loc[order,'경도'])
        market_name.append(Market.loc[order,'시장/마트 이름'])
        distance.append(haversine((x1,y1),(market_lat,market_long), unit='km'))
        order += 1
    
    dict_market_info = {"시장/마트 이름":market_name, "거리(km)":distance}
    size_distance = pd.DataFrame(dict_market_info)
    S_D = size_distance.sort_values('거리(km)')
    S_D.to_csv('C:\Python_VScode\OpenSourceProject\Market_distance.csv',encoding='CP949')
    
    return S_D
    
    
    
    
def Calculate_Price():
    df = pd.read_csv('C:\\Python_VScode\\OpenSourceProject\\Dec_market.csv',encoding='CP949')
    distance = pd.read_csv('C:\\Python_VScode\\OpenSourceProject\\Market_distance.csv',encoding='CP949')

    df_essential = df[['시장/마트 이름','품목 이름','가격(원)']]

    df_essential.replace({'고등어(생물,국산)','고등어(냉동,국산)','고등어(생물,수입산)','고등어(냉동,수입산)'}, '고등어',inplace=True)
    df_essential.replace({'사과(부사)' , '사과(부사, 300g)' , '사과(부사),중급(대)'}, '사과',inplace=True)
    df_essential.replace({ '배(중품)' , '배(신고)' , '배(신고, 600g)', '배(신고),중급(대)'}, '배',inplace=True)
    df_essential.replace({'배추(중간)', '배추(2.5~3kg)', '배추(국산)'}, '배추',inplace=True)
    df_essential.replace({'무(세척무)', '무(1kg)'}, '무',inplace=True)
    df_essential.replace({'양파(1.5kg망)' , '양파(작은망)'}, '양파',inplace=True)
    df_essential.replace({'상추(100g)'}, '상추',inplace=True)
    df_essential.replace({'오이(다다기)'}, '오이',inplace=True)
    df_essential.replace({'호박(인큐베이터),중간' , '호박(인큐베이터)'}, '호박',inplace=True)
    df_essential.replace({'쇠고기(한우,불고기)', '쇠고기(한우1등급)' , '쇠고기(육우,불고기)' , '쇠고기(등심)' , '쇠고기(육우1등급)'}, '쇠고기',inplace=True)
    df_essential.replace({'돼지고기(생삼겹살)', '돼지고기(삼겹살)'}, '돼지고기',inplace=True)
    df_essential.replace({'닭고기(육계)', '닭고기(중간)', '닭고기(토종닭)'}, '닭고기',inplace=True)
    df_essential.replace({'달걀(10개)', '달걀(30개)', '달걀(왕란)', '달걀(15개)', '달걀(중란)'}, '달걀',inplace=True)
    df_essential.replace({'조기(생물,수입산)', '조기(국산,냉동)' , '조기(국산,생물)', '조기(냉동,수입산)' , '조기(생물,국산)', '조기(냉동,국산)', '냉동참조기(20cm,수입)'}, '조기',inplace=True)
    df_essential.replace({'명태(러시아,냉동)' , '명태(냉동,수입산)', '명태(생물,수입산)'  , '명태(냉동,국산)', '명태(45cm,수입산)', '명태(생물,국산)'}, '명태',inplace=True)
    df_essential.replace({'오징어(생물,국산)' ,'오징어(냉동,국산)' ,'오징어(생물,수입산)' ,'오징어(냉동,수입산)'}, '오징어',inplace=True)
    
    a= df_essential
    
    return a
    
    

def Recommend_Market(df_essential, distance):
    gredients = []    #리스트 선언
    groc = (input('원하는 재료를 모두 입력하시오: ').split())
    gredients.append(groc)
    New_list = []
    count = 0
    final_file=[]
    f=[]
    for index, value in enumerate(groc):
        df_filtered=df_essential[df_essential['품목 이름']==value]
        df_filtered=df_filtered.reset_index(drop=True)    #해당하는 재료를 새로운 표로 저장

        a = pd.DataFrame(df_filtered)   #완성된 딕셔너리를 가공하기   쉽게 데이터프레임 형태로 변환
        New_list.append(a)
        count += 1
        b = pd.merge(New_list[index], distance, how='inner', on=['시장/마트 이름'])
        b=b[b['가격(원)']!=0]
        b['가중치값'] = b['가격(원)'] + (b['거리(km)']*2000/8.3)
        #b = b.drop('Unnamed: 0',axis=1)
        final_file.append(b)
        
    user_input = int(input("원하는 추천 옵션을 선택하세요:(1:The cheapest, 2:The closest, 3:Resonable)"))
    match user_input:
        case 1:
            print("가장 저렴한 마트 3군데")
            for i in range(count):
                f.append(final_file[i].sort_values(by='가격(원)'))
                f[i] = f[i].drop_duplicates(subset='가격(원)', keep='first', inplace=False, ignore_index=False)
                f[i] = f[i].reset_index()
            print(f[i].loc[[0,1,2]])
            
        case 2:
            print("가장 가까운 마트 3군데")
            for i in range(count):
                f.append(final_file[i].sort_values(by='거리(km)'))
                f[i] = f[i].drop_duplicates(subset='시장/마트 이름',keep='first',inplace=False,ignore_index=False)
                f[i] = f[i].reset_index()
            print(f[i].loc[[0, 1, 2]])
            
        case 3:
            print("가장 합리적인 마트 3군데")
            for i in range(count):
                f.append(final_file[i].sort_values(by='가중치값'))
                f[i] = f[i].drop_duplicates(subset='가중치값', keep='first', inplace=False, ignore_index=False)
                f[i] = f[i].reset_index()
            print(f[i].loc[[0, 1, 2]])
            
    '''print("가장 저렴한 마트 3군데")
    for i in range(count):
        f.append(final_file[i].sort_values(by='가격(원)'))
        f[i] = f[i].drop_duplicates(subset='가격(원)', keep='first', inplace=False, ignore_index=False)
        f[i] = f[i].reset_index()
        print(f[i].loc[[0,1,2]])
    f=[]
    print("가장 가까운 마트 3군데")
    for i in range(count):
        f.append(final_file[i].sort_values(by='거리(km)'))
        f[i] = f[i].drop_duplicates(subset='시장/마트 이름',keep='first',inplace=False,ignore_index=False)
        f[i] = f[i].reset_index()
        print(f[i].loc[[0, 1, 2]])
    f=[]
    print("가장 합리적인 마트 3군데")
    for i in range(count):
        f.append(final_file[i].sort_values(by='가중치값'))
        f[i] = f[i].drop_duplicates(subset='가중치값', keep='first', inplace=False, ignore_index=False)
        f[i] = f[i].reset_index()
        print(f[i].loc[[0, 1, 2]])

    webbrowser.open('C:\\Python_VScode\\OpenSourceProject\\map.html')'''
    #csv파일에서 가져온 데이터 칸 밀리지 않게 깔끔하게 정리하기
