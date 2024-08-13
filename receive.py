import requests
from PIL import Image
from io import BytesIO

# API URL
url = 'http://127.0.0.1:8000/plot/?dna1=ATGACATAGAGAT&dna2=TACTGGAGAGATAGATA'

# API 요청
response = requests.get(url)

# 응답 확인
if response.status_code == 200:
    # 이미지 데이터가 바이너리 형태로 응답됨
    img_data = response.content
    
    # 이미지 파일을 열기
    image = Image.open(BytesIO(img_data))
    
    # 이미지 저장
    image.save('output_image.png')
    print("이미지가 성공적으로 저장되었습니다.")
else:
    print(f"API 요청 실패: 상태 코드 {response.status_code}")

