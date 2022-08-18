from .models import Employee, Detected
import cv2
import pickle
import face_recognition
import datetime
from cachetools import TTLCache
from django.utils import timezone


cache = TTLCache(maxsize=20, ttl=10)


# Hàm ghi ảnh đã nhận dạng đúng vào trong thư mục detected
def identify1(frame, name, buf, buf_length, known_conf):

    if name in cache:
        return
    count = 0
    for ele in buf:
        count += ele.count(name)
    
    if count >= known_conf:
        timestamp = datetime.datetime.now(tz=timezone.utc)
        print(name, timestamp)
        cache[name] = 'detected'
        path = 'app/facerec/detected/{}_{}.jpg'.format(name, timestamp)
        cv2.imwrite(path, frame)
        try:
            emp = Employee.objects.get(name=name)
            emp.detected_set.create(time_stamp=timestamp)
        except:
            pass                


def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.9):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Tải lên bộ phân loại KNN đã lưu
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Tải hình ảnh lên và xác định vị trí khuôn mặt
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)

    # Nếu không tìm thấy khuôn mặt, trả về một mảng rỗng
    if len(X_face_locations) == 0:
        return []

    # Trích xuất đặc trưng ảnh test
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)

    # Sử dụng mô hình KNN để tìm khuôn mặt tốt nhất cho khuôn mặt test
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=5)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Dự đoán lớp và bỏ đi các lớp mà có giá trị dưới ngưỡng
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def identify_faces(video_capture):

    buf_length = 10
    known_conf = 5
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Lấy từng khung hình của video
        ret, frame = video_capture.read()

        # Thay đổi kích thước khung hình thành 1/4 để quá trình nhận diện được nhanh hơn
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Do đang sử dụng thư viện face_recognition nên phải chuyển ảnh màu BGR -> RGB
        rgb_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="app/facerec/models/trained_model.clf")

        process_this_frame = not process_this_frame

        face_names = []

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Vẽ một khung hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Gán nhãn bên dưới khuôn mặt
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)

        buf[i] = face_names
        i = (i + 1) % buf_length

        # Hiển thị kết quả
        cv2.imshow('Video', frame)

        # Nhấn q để tắt màn hình
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()