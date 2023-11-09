import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
import matplotlib.pyplot as plt
from keras.preprocessing import image
import tensorflow as tf

class MainWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(580, 650)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.Camera = QtWidgets.QLabel(Dialog)
        self.Camera.setGeometry(QtCore.QRect(50, 50, 480, 480))

        self.Predict = QtWidgets.QPushButton(parent=Dialog)
        self.Predict.setGeometry(QtCore.QRect(50, 550, 101, 41))
        self.Predict.setText("Predict")
        self.Predict.clicked.connect(self.capture_image)

        # self.Clear = QtWidgets.QPushButton(parent=Dialog)
        # self.Clear.setGeometry(QtCore.QRect(160, 550, 101, 41))
        # self.Clear.setText("Clear")

        self.Label = QtWidgets.QLabel(Dialog)
        self.Label.setGeometry(QtCore.QRect(160, 550, 500, 41))
        self.Label.setFont(font)
        self.Label.setText("Predicted: Nan")

        self.CaptureVideo = cv2.VideoCapture(0)
        self.timer_object = QtCore.QObject()
        self.timer = QTimer(self.timer_object)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        ret, frame = self.CaptureVideo.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, 480, 480, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.Camera.setPixmap(pixmap)

    def capture_image(self):
        # Chụp ảnh từ QLabel và lưu lại
        pixmap = self.Camera.pixmap()
        if pixmap:
            img = pixmap.toImage().save("a.jpg")
            result_value = result()
            if result_value == 1:
                result_text = "Có khẩu trang"
            else:
                result_text = "Không khẩu trang"
            self.Label.setText("Predicted Class: " + result_text)
        
def result():
    color_image = cv2.imread('a.jpg')
    resized_image = cv2.resize(color_image, (128, 128))
    img = image.img_to_array(resized_image)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    model = tf.keras.models.load_model(r"Mask.h5")
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)
    return predicted_class[0]

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())