import folium
import googlemaps
import json
import pandas as pd

#구글맵 key
gmaps = googlemaps.Client(key="AIzaSyCK0gxxUUobQQ5tPKbVE8F16SApviPvVhs")

#json file 호출
geo_path = 'data/02. skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))

#csv file 가져오기
service_seoul = pd.read_csv('data/parcel_service.csv')
map = folium.Map(location = [37.5103, 126.98], zoom_start = 11)

#경도 위도 columns 저장
matrix1 = []
matrix1 = pd.DataFrame(service_seoul[["location2"]])
matrix2 = []
matrix2 = pd.DataFrame(service_seoul[["location1"]])

#지도 maker 출력
for row in range(3, 200):
    folium.Marker((matrix1['location2'][row], matrix2['location1'][row]), popup = '안심택배', icon=folium.Icon(color='red')).add_to(map)
 
#결과값 저장   
map.save('Desktop/data/map.html')
