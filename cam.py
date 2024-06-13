import sys
import cv2
import torch
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
from cam_ui import Ui_Maincam

class Maincam(QMainWindow):
    def __init__(self):
        super(Maincam, self).__init__()
        self.ui = Ui_Maincam()
        self.ui.setupUi(self)
        self.setWindowTitle("Custom Model을 이용한 YOLO 웹캠")

        # 클래스 이름을 정의합니다.
        self.cls_names = ['big bus', 'big truck', 'bus-l-', 'bus-s-', 'car', 'mid truck', 'small bus', 'small truck', 'truck-l-', 'truck-m-', 'truck-s-', 'truck-xl-']

        # GPU가 있는 경우 GPU를 사용하고, 그렇지 않은 경우 CPU를 사용합니다.
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 사용자가 만든(학습시킨) 모델을 로드합니다.
        self.model = torch.hub.load('./yolov5', 'custom', path='./yolov5s.pt', source='local')
        self.model.to(self.device)

        # 프레임을 읽어오는 타이머를 설정합니다.
        self.timer = QTimer()
        self.timer.setInterval(500)  # 0.5초마다 프레임을 읽어옵니다.
        self.timer.timeout.connect(self.video_pred)  # 타이머에 video_pred 함수를 연결합니다.
        self.timer.start()  # 타이머를 시작합니다.

        # 웹캠을 엽니다.
        self.video = cv2.VideoCapture(0)

        # 버튼 클릭 이벤트 연결
        self.ui.pushButton.clicked.connect(self.load_image)
        self.ui.pushButton_2.clicked.connect(self.switch_to_camera)

        self.loaded_image = None  # 불러온 이미지를 저장할 변수

    # OpenCV 배열을 QImage로 변환합니다.
    def convert2QImage(self, img):
        height, width, channel = img.shape
        bytes_per_line = width * channel
        return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

    # 웹캠에서 프레임을 읽어와서 YOLO 모델로 객체 탐지를 수행합니다.
    def video_pred(self):
        if self.loaded_image is None:
            ret, frame = self.video.read()
            if not ret:  # 프레임을 읽지 못한 경우
                self.timer.stop()  # 타이머를 중지합니다.
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV의 BGR 형식을 RGB 형식으로 변환합니다.
        else:
            frame = self.loaded_image.copy()

        # 이미지 크기 조정
        frame = cv2.resize(frame, (self.ui.input.width(), self.ui.input.height()), interpolation=cv2.INTER_AREA)

        self.ui.input.setPixmap(QPixmap.fromImage(self.convert2QImage(frame)))  # 입력 이미지를 표시합니다.
        start = time.perf_counter()  # 객체 탐지 시작 시간을 기록합니다.
        results = self.model(frame)  # YOLO 모델로 객체를 탐지합니다.
        detections = results.xyxy[0].cpu().numpy()  # 탐지 결과를 NumPy 배열로 변환합니다.

        if len(detections) > 0:  # 탐지된 객체가 있는 경우
            for det in detections:
                cls_idx = int(det[5])  # 클래스 인덱스는 det[5]에 있음
                if cls_idx < len(self.cls_names):
                    class_name = self.cls_names[cls_idx]
                    print(f"감지된 객체(Class) : {class_name}")  # 감지된 클래스 이름을 출력합니다.

        # end = time.perf_counter()  # 객체 탐지 종료 시간을 기록합니다.
        # self.ui.label_1.setText(f'판독시간: {round((end - start) * 1000, 4)} ms')  # 객체 탐지 시간을 표시합니다.

        image = results.render()[0]  # 객체를 이미지로 렌더링합니다.
        self.ui.output.setPixmap(QPixmap.fromImage(self.convert2QImage(image)))  # 출력 이미지를 표시합니다.

    # 이미지 파일을 불러와서 모델을 사용하여 처리하는 함수
    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if fileName:
            # 이미지를 읽어서 QLabel에 표시
            image = cv2.imread(fileName)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.loaded_image = image_rgb  # 이미지를 로드하여 loaded_image 변수에 저장합니다.

    # 캠 화면으로 전환하는 함수
    def switch_to_camera(self):
        self.loaded_image = None  # 로드된 이미지를 초기화하여 캠 화면으로 전환합니다.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Maincam()
    window.show()
    sys.exit(app.exec_())
