import cv2
import numpy as np
import yaml
import os
from Pre_processing.Enter_GeoCoordinates import Tk_GeoPoint

refPt = []
cap_img = []
geoPt = []

'''
# Control point를 선정하는 GUI 기반 프로그램 코드
 - 왼쪽 마우스 : 클릭한 좌표를 Control point로 선정
 - 키보드 'r'  : 선택된 포인트를 차례로 삭제
 - 키보드 's'  : 선택된 포인트 저장
 - 키보드 'q'  : 저장하지 않고 GUI 프로그램 종료
'''
def create_control_point(img_path, control_point_file, control_point_img):

    print()
    print('The function selecting control points ')
    print('- left mouse button : Select control points')
    print('- keyboard "r" : remove selected points')
    print('- keyboard "s" : save selected points ')
    print('- keyboard "q" : exit without saving the selected points')
    print()

    def click_and_select(event, x, y, flags, param):
        global refPt, cap_img, geoPt

        if event == cv2.EVENT_FLAG_LBUTTON:
            if len(refPt) == 0:
                refPt = [(x,y)]
            else:
                refPt.append((x,y))
            
            # Control point 선정 및 표출
            cv2.circle(image, (x, y), 9, (0, 0, 255), -1)
            cv2.putText(image, 'point.{}'.format(len(refPt)), (x+15, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, [0,0,0], 3)
            clone = image.copy()
            cap_img.append(clone)
            cv2.imshow('draw', cap_img[-1])
                            
            # Geo point 입력창 표출 및 입력
            app = Tk_GeoPoint(None)
            app.title('Enter GeoCoordinates')
            app.geometry('310x80')
            app.mainloop()
            if len(geoPt) == 0:
                geoPt = [app.pointList]
            else:
                geoPt.append(app.pointList)

        elif event == cv2.EVENT_MOUSEWHEEL:pass

    image = cv2.imread(img_path)
    clone = image.copy()
    cap_img.append(clone)
    cv2.namedWindow('draw', cv2.WINDOW_NORMAL)
    cv2.imshow("draw", image)
    cv2.setMouseCallback("draw", click_and_select, cap_img[-1])
    cv2.waitKey(0)


    while True:
        cv2.imshow('draw', image)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('r'):
            if len(refPt) == 0:
                print("There's no selected image. Please create image using left mouse click.")
            elif len(refPt) == 1:
                del refPt[-1], cap_img[-1], geoPt[-1]
                image = clone.copy()
            else:
                del refPt[-1], cap_img[-1], geoPt[-1]
                image = cap_img[-1].copy()
        elif key == ord('s'):
            pointsFile = {'frm_point': {i: x for i, x in enumerate(refPt)}}
            pointsFile['geo_point'] = {i: x for i, x in enumerate(geoPt)}
            with open(control_point_file, 'w') as file:
                yaml.dump(pointsFile, file, sort_keys=False)
            cv2.imwrite(control_point_img, image)
            break
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

def get_control_point(test_Video):
    control_point_file = 'data/data_setting/control_point/' + test_Video + '/' + test_Video + '_point.yaml'
    control_point_img = 'data/data_setting/control_point/'+ test_Video + '/' + test_Video + '_point.jpg'
    first_frm = 'data/data_setting/source_img/' + test_Video + '/' + test_Video +'.jpg'
    
    if os.path.exists(control_point_file):
        print()
        create_new_srcimg = input('If you wanna set new control point, Write yes : ')
        if create_new_srcimg =='yes':
            create_control_point(first_frm, control_point_file, control_point_img)
        else:
            pass
    else:
        os.makedirs('data/data_setting/control_point/' + test_Video + '/')
        create_control_point(first_frm, control_point_file, control_point_img)