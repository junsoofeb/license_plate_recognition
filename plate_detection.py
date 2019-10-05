import cv2 as cv
import numpy as np
import operator
from PIL import Image
from pytesseract import *
#import subprocess
    


def show(frame):
    cv.imshow("", frame)
    cv.waitKey()
    cv.destroyAllWindows()
    
for f in range(1,12):  
    # 본인의 환경에 맞게, 자동차 사진의 경로를 설정
    frame = cv.imread(f'./car_img/{f}.jpg')
    #frame = cv.resize(frame, (640, 480))
    print("current frame >> ", f,".jpg", sep='')
    show(frame)
    
    copy = frame.copy()
    copy2 = frame.copy()
    for_roi = frame.copy()

    blur = cv.GaussianBlur(frame, (5,5), 0)
    #blur = cv.bilateralFilter(frame, 5, 75, 75)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 0, 10)
    #show(canny)
    cnts, _ = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    #copy_cnts = cnts.copy()
    #cv.drawContours(copy, cnts, -1, (0, 0, 255) )
    #show(copy)
    minAreaRect_x_list = []
    minAreaRect_y_list = []
    minAreaRect_i_list = []

    x_list = []
    y_list = []
    roi_position = []

    #print(len(cnts))
    for i in range(len(cnts)):
    #for i in range(40,41):

        cnt = cnts[i]
        rect = cv.minAreaRect(cnt)
        
        box = cv.boxPoints(rect)
        
        
        #print(box)
        #print(box[0][0])
        #print(box[0][1])
        #print(box[1][0])
        #print(box[1][1])
        '''
        box = [ [x y],
                [x y],
                [x y],
                [x y] ]
        '''
        for r, c in box:
            x_list.append(r)
            y_list.append(c)

        #print(x_list, y_list)

        x_list =sorted(x_list)
        y_list =sorted(y_list)
        #print(x_list, y_list)

        #print(i, x_list[-1] - x_list[0])
        #if x_list[-1] - x_list[0] > 100  and  x_list[-1] - x_list[0] < 400 and y_list[-1] - y_list[0] < 100 and x_list[-1] - x_list[0] > (y_list[-1] - y_list[0]) * 2.5:
        if x_list[-1] - x_list[0] > 100  and  x_list[-1] - x_list[0] < 400 and  y_list[-1] - y_list[0] > 10 and y_list[-1] - y_list[0] < 100 and x_list[-1] - x_list[0] > (y_list[-1] - y_list[0]) * 3:
            box = np.int0(box)
            if abs(rect[2]) < 3 or abs(rect[2]) > 87:
                #print(i, rect[2])
                cv.drawContours(copy2, [box], 0 , (0, 0, 255), 2)
                roi_position.append([x_list[0], x_list[-1], y_list[0], y_list[-1]])
            x_list = []
            y_list = []
        else:
            x_list = []
            y_list = []

    #show(copy2)


# roi 만 따오는 부분    
    roi_check = 0
    for i in range(len(roi_position)):
        min_x = roi_position[i][0]
        max_x = roi_position[i][1]
        min_y = roi_position[i][2]
        max_y = roi_position[i][3]
        
        min_x, max_x, min_y, max_y = int(min_x), int(max_x), int(min_y), int(max_y)
        
        roi = for_roi.copy()[min_y : max_y , min_x : max_x]
        temp_roi = roi.copy()

        #show(roi)
        blur = cv.GaussianBlur(roi, (9,9), 0)
        canny = cv.Canny(temp_roi, 0, 50)
        cnts, _ = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        #cv.drawContours(roi, cnts, -1, (0, 0, 255) )
        #show(roi)
        
        cnt_counter = 0
        # 각 roi 후보들 중에서 contour 길이와  넓이가 적절한 것만 번호판으로 인정
        for ii in range(len(cnts)):
            cnt = cnts[ii]
            area = cv.contourArea(cnt)
            lenth = cv.arcLength(cnt, True)
            
            if area > 20 and lenth > 40 and lenth < 160:
                #print("현재 인덱스",ii , " 현재 컨투어 넓이 :",area," 현재 컨투어 길이 :", lenth)
                #cv.drawContours(roi, [cnt], 0, (0, 0, 255) )
                cnt_counter += 1
                #rect = cv.minAreaRect(cnt)
                #box = cv.boxPoints(rect)
                #box = np.int0(box)
                #cv.drawContours(roi, [box], 0 , (0, 0, 255), 2)
        if cnt_counter > 7 and cnt_counter < 20 and roi_check == 0:
            #print("counter  : ",cnt_counter)
            cnt_counter = 0
            roi_check = 1
            try:
                save = f'./roi_img/{ii}.jpg'
                cv.imwrite(save, roi)
                img = cv.imread(r'./roi_img/%s.jpg' % ii)
                #print(image_to_string(f'{ii}.jpg', lang='eng', config='--psm 1 -c preserve_interword_spaces=1'))
                #print(subprocess.call("tesseract ./roi_img/%d.jpg -l" % ii))
                print(image_to_string(img, lang = 'kor', config='--psm 7 -c preserve_interword_spaces=2'))
                show(roi)
                
                break
            except:
                continue
        if  roi_check == 1:  
            break
            
            