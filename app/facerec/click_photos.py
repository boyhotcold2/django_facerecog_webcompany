import cv2
import os


# hàm này nhấn spacebar để chụp lại ảnh
def click(dirName, dirID, cam):

    # tạo biến đếm để tăng số lần nhấn
    img_counter = 0
    
    DIR = f"app/facerec/dataset/{dirName}_{dirID}"

    # tạo thư mục lưu hình ảnh chứa khuôn mặt
    try:
        os.mkdir(DIR)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
        img_counter = len(os.listdir(DIR))

    while True:
        ret, frame = cam.read()
        cv2.imshow("Video", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        # nếu nhấn nút ESC thì thoát (thoát khỏi vòng lặp)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        # kí hiệu mã ascii của nút spacebar
        elif k%256 == 32:
            img_name = f"app/facerec/dataset/{dirName}_{dirID}/opencv_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()
