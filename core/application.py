# just something temporarily, for ease of projection

import sys
import image_warp as iw
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.initUI()

    def initUI(self):
        # Create a label that will hold the image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)  # Align the image in the center of QLabel
        self.setCentralWidget(self.label)
        self.updateImage()

        # Window settings
        self.setWindowTitle('Image Viewer')
        self.showMaximized()

        # Set the background to black
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.black)
        self.setPalette(palette)

    def updateImage(self):
        # Load the image
        pixmap = QPixmap(self.image_path)

        # Scale the pixmap to fit the current window size, maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # Update the image when the window is resized
        self.updateImage()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the path to your images
    image_1_path = 'core\image_assets\earthView1.png'
    image_2_path = 'core\image_assets\earthView2.png'
    
    # Warp the images - not sustainable method
    
    # just place holder variable names, i kinda don't know what they do
    stretchFactor = 8
    bge = stretchFactor/4
    bf = (bge*stretchFactor) / 100
    warped_image_1 = iw.warp_image(image_1_path, bulge_factor=-bf, bulge_exponent=bge, scale_down_factor=1.01)
    warp_path_1 = "core\image_assets\warped1.png"
    warped_image_1.save(warp_path_1)
    warped_image_2 = iw.warp_image(image_2_path, bulge_factor=-bf, bulge_exponent=bge, scale_down_factor=1.01)
    warp_path_2 = "core\image_assets\warped2.png"
    warped_image_2.save(warp_path_2)

    # Create windows for each image
    window1 = ImageWindow(warp_path_1)
    window2 = ImageWindow(warp_path_2)

    sys.exit(app.exec_())
