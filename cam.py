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

        self.cls_names = ['big bus', 'big truck', 'bus-l-', 'bus-s-', 'car', 'mid truck', 'small bus', 'small truck', 'truck-l-', 'truck-m-', 'truck-s-', 'truck-xl-']

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = torch.hub.load('./yolov5', 'custom', path='./yolov5s.pt', source='local')
        self.model.to(self.device)

        self.timer = QTimer()
        self.timer.setInterval(500)  
        self.timer.timeout.connect(self.video_pred)  
        self.timer.start()

        self.video = cv2.VideoCapture(0)

        self.ui.pushButton.clicked.connect(self.load_image)
        self.ui.pushButton_2.clicked.connect(self.switch_to_camera)

        self.loaded_image = None 

    def convert2QImage(self, img):
        height, width, channel = img.shape
        bytes_per_line = width * channel
        return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

    def video_pred(self):
        if self.loaded_image is None:
            ret, frame = self.video.read()
            if not ret: 
                self.timer.stop()
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            frame = self.loaded_image.copy()

        frame = cv2.resize(frame, (self.ui.input.width(), self.ui.input.height()), interpolation=cv2.INTER_AREA)

        self.ui.input.setPixmap(QPixmap.fromImage(self.convert2QImage(frame)))
        start = time.perf_counter()
        results = self.model(frame)
        detections = results.xyxy[0].cpu().numpy()

        if len(detections) > 0:
            for det in detections:
                cls_idx = int(det[5])
                if cls_idx < len(self.cls_names):
                    class_name = self.cls_names[cls_idx]
                    print(f"감지된 객체(Class) : {class_name}")

        image = results.render()[0]
        self.ui.output.setPixmap(QPixmap.fromImage(self.convert2QImage(image)))

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if fileName:
            image = cv2.imread(fileName)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.loaded_image = image_rgb

    def switch_to_camera(self):
        self.loaded_image = None 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Maincam()
    window.show()
    sys.exit(app.exec_())
