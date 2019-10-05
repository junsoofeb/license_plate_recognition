# license_plate_recognition
with OpenCV


## 1. 개요

카메라를 사용한 자동차 번호판 인식 프로그램

## 2. 구현 환경

1. window10 Home
2. Python 3.6
3. OpenCV-python library 4.1.0
4. Numpy 1.16
5. tesseract-3.05.01-vc14_10 및 pytesseract 0.3.0

## 3. 동작 과정

1. 이미지 크기 재조정 , 블러링 및 canny edge()을 거쳐 contour를 찾고, contour의 x, y좌표를 정렬하여 roi를 잡는다.
2. 추출한 roi에서 contour의 길이와 넓이가 적절한 것만 번호판으로 적당하다고 가정하고 최종 roi로 판단한다.
3. 최종 roi에서 contour의 개수가 조건에 해당하면 tesseract를 돌려본다.


## 4. 예시
<자동차 사진 1>
<img width="960" alt="1" src="https://user-images.githubusercontent.com/46870741/66252161-0a44ca80-e793-11e9-8f68-9fbefae4a74c.png">

<프로그램 결과 1>
<img width="960" alt="2" src="https://user-images.githubusercontent.com/46870741/66252165-13ce3280-e793-11e9-9c44-3a469269e159.png">

<자동차 사진 2>
<img width="960" alt="3" src="https://user-images.githubusercontent.com/46870741/66252180-2e081080-e793-11e9-9b26-ecf58fada6bb.png">

<프로그램 결과 2>
<img width="960" alt="4" src="https://user-images.githubusercontent.com/46870741/66252184-3eb88680-e793-11e9-974e-585919ff0a67.png">
