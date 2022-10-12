from Image import *
from libraries import *
from sub_window_classes import *

# QWidget class for main window
class main_window(QWidget):
    def __init__(self):
        super().__init__()
        # camera initials
        self.camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder="captures\\", collection_name="Capture")
        self.picture_index = 0
        self.camera.reset_image_index(self.picture_index)

        # initial variables and files
        self.alert_sub_window = AlertSubWindow()
        self.camera_setting_window = CameraToolsSubWindow()
        self.channel_edit_window = ChannelEditSubWindow()
        self.image = Image(cv2.imread("images\\base.png", 1))
        self.backup = cv2.imread("images\\base.png", 1)

        # loading ui file
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\UI files\\main.ui", self)
        self.move(150, 0)
        # loading icon image
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.png"))
        self.setStyleSheet(open('style\\style.css').read())

        # deriving elements from main window
        self.browseButton = self.findChild(QPushButton, "browseButton")
        self.TakePictureButton = self.findChild(QPushButton, "TakePictureButton")
        self.CheckCameraButton = self.findChild(QPushButton, "CheckCameraButton")
        self.cameraSettingButton = self.findChild(QPushButton, "cameraSettingButton")
        self.saveButton = self.findChild(QPushButton, "saveButton")
        self.resetButton = self.findChild(QPushButton, "resetButton")
        self.invertButton = self.findChild(QPushButton, "invertButton")
        self.ACButton = self.findChild(QPushButton, "ACButton")
        self.ASButton = self.findChild(QPushButton, "ASButton")
        self.BWButton = self.findChild(QPushButton, "BWButton")
        self.imageArea = self.findChild(QGraphicsView, "imageArea")
        self.hflipButton = self.findChild(QPushButton, "hflip")
        self.vflipButton = self.findChild(QPushButton, "vflip")
        self.UCRotateButton = self.findChild(QPushButton, "rotateUnClockWise")
        self.CRotateButton = self.findChild(QPushButton, "rotateClockWise")
        self.zoomIn = self.findChild(QPushButton, "zoomIn")
        self.zoomOut = self.findChild(QPushButton, "zoomOut")
        self.rstZoom = self.findChild(QPushButton, "rstZoom")
        self.channelEditButton = self.findChild(QPushButton, "channelEditButton")
        self.gamaSlider = self.findChild(QSlider, "gamaSlider")

        # zoom parameters for scaling image
        self.zoom_scale = 1
        self.zoom_parameter = 0.2
        self.scene = QGraphicsScene()

        # connecting buttons to their functions
        self.invertButton.clicked.connect(self.invert)
        self.ACButton.clicked.connect(self.auto_contrast)
        self.ASButton.clicked.connect(self.auto_sharpen)
        self.BWButton.clicked.connect(self.black_and_white)
        self.browseButton.clicked.connect(self.on_click)
        self.resetButton.clicked.connect(self.reset)
        self.saveButton.clicked.connect(self.save)
        self.vflipButton.clicked.connect(self.vertical_flip)
        self.hflipButton.clicked.connect(self.horizontal_flip)
        self.UCRotateButton.clicked.connect(self.clockwise_rotate)
        self.CRotateButton.clicked.connect(self.unclockwise_rotate)
        self.TakePictureButton.clicked.connect(self.take_picture)
        self.CheckCameraButton.clicked.connect(self.check_camera)
        self.cameraSettingButton.clicked.connect(self.camera_setting)
        self.zoomIn.clicked.connect(self.zooming_in)
        self.zoomOut.clicked.connect(self.zooming_out)
        self.rstZoom.clicked.connect(self.zooming_rst)
        self.channelEditButton.clicked.connect(self.channel_edit)
        self.gamaSlider.valueChanged.connect(self.gama_slider_value_change)

        # Histograms
        self.red_channel_plot = self.findChild(PlotWidget, "histogram1")
        self.red_channel_hist()

        self.green_channel_plot = self.findChild(PlotWidget, "histogram2")
        self.green_channel_hist()

        self.blue_channel_plot = self.findChild(PlotWidget, "histogram3")
        self.blue_channel_hist()

    # opening channel edit window
    def channel_edit(self):
        self.channel_edit_window.set_image(self.image)
        self.channel_edit_window.show()

    # Handling changes in gama value
    def gama_slider_value_change(self):
        t = self.gamaSlider.value() / 10
        self.image.gama_adjust(t)
        self.update_image()

    # Updating Histograms Values
    def red_channel_hist(self):
        self.red_channel_plot.clear()
        red_channel = cv2.calcHist([self.image.get_image()],[2],None,[256],[0,256])
        rc = []
        for i in red_channel:
            rc.append(i[0]//1000)
        self.red_channel_plot.setBackground((141,9,37))
        self.red_channel_plot.plot(rc,pen='w')
        self.red_channel_plot.setLabel('bottom', 'Red Channel')
    def green_channel_hist(self):
        self.green_channel_plot.clear()
        green_channel = cv2.calcHist([self.image.get_image()], [1], None, [256], [0, 256])
        gc = []
        for i in green_channel:
            gc.append(i[0] // 1000)
        self.green_channel_plot.setBackground((2, 66, 5))
        self.green_channel_plot.plot(gc, pen='w')
        self.green_channel_plot.setLabel('bottom', 'Green Channel')
    def blue_channel_hist(self):
        self.blue_channel_plot.clear()
        blue_channel = cv2.calcHist([self.image.get_image()], [0], None, [256], [0, 256])
        bc = []
        for i in blue_channel:
            bc.append(i[0] // 1000)
        self.blue_channel_plot.setBackground((0, 43, 100))
        self.blue_channel_plot.plot(bc, pen='w')
        self.blue_channel_plot.setLabel('bottom', 'Blue Channel')
    def update_histograms(self):
        self.blue_channel_hist()
        self.green_channel_hist()
        self.red_channel_hist()

    # handling wheel zoom
    def wheelEvent(self, event):
        a = event.angleDelta().y()
        self.zooming_in() if a>0 else self.zooming_out()

    # zooming functions
    def zooming_in(self):
        self.current_image = QPixmap(
            qimage2ndarray.array2qimage(cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2RGB)))
        self.scene = QGraphicsScene()
        h = 864 * self.zoom_scale * (1+self.zoom_parameter)
        self.zoom_scale = self.zoom_scale * (1+self.zoom_parameter)
        self.current_image = self.current_image.scaledToHeight(int(h))
        self.scene_img = self.scene.addPixmap(self.current_image)
        self.imageArea.setScene(self.scene)
        self.update_histograms()
    def zooming_out(self):
        self.current_image = QPixmap(
            qimage2ndarray.array2qimage(cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2RGB)))
        self.scene = QGraphicsScene()
        h = 864 * self.zoom_scale * (1-self.zoom_parameter)
        self.zoom_scale = self.zoom_scale * (1 - self.zoom_parameter)
        self.current_image = self.current_image.scaledToHeight(int(h))
        self.scene_img = self.scene.addPixmap(self.current_image)
        self.imageArea.setScene(self.scene)
        self.update_histograms()
    def zooming_rst(self):
        self.current_image = QPixmap(
            qimage2ndarray.array2qimage(cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2RGB)))
        self.scene = QGraphicsScene()
        h = 864
        self.zoom_scale = 1
        self.current_image = self.current_image.scaledToHeight(h)
        self.scene_img = self.scene.addPixmap(self.current_image)
        self.imageArea.setScene(self.scene)
        self.update_histograms()

    # Browsing files
    def on_click(self):
        pic, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png *.jpeg *.ico);;All Files (*)")
        if pic:
            self.pictureName = pic[0].split('/')[-1][:-4]
            self.image = Image(cv2.imread(pic[0], 1) )
            self.channel_edit_window.set_image(self.image)
            self.backup = cv2.imread(pic[0], 1)
            self.update_image()

    # camera setting window
    def camera_setting(self):
        self.camera_setting_window.show()

    # checking camera connectivity
    def check_camera(self):
        self.camera.show_camera_info("connectivity_check_@.txt")
        try:
            f = open("connectivity_check_@.txt")
            f.close()
            os.remove("connectivity_check_@.txt")
            self.alert_sub_window.set_text("Camera is Available!")
            self.alert_sub_window.show()
        except IOError:
            self.alert_sub_window.set_text("Camera is not Connected!")
            self.alert_sub_window.show()

    # take picture command
    def take_picture(self):
        self.check_camera()
        # set the name of the picture
        self.picture_index = self.camera.capture_single_image(autofocus=True)
        self.pictureName = "Capture_"+str(self.picture_index)+".jpg"
        address = "captures\\Capture_"+str(self.picture_index)+".jpg"
        # save image and its backup
        self.image = Image(cv2.imread(address, 1))
        self.backup = cv2.imread(address, 1)
        self.update_image()

    # updating the screen
    def update_image(self):
        self.current_image = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2RGB)))
        self.scene = QGraphicsScene()
        self.current_image = self.current_image.scaledToHeight(864)
        self.scene_img = self.scene.addPixmap(self.current_image)
        self.imageArea.setScene(self.scene)
        self.update_histograms()

    # connecting buttons to Image class
    # Flips buttons function
    def vertical_flip(self):
        self.image.v_flip()
        self.update_image()
    def horizontal_flip(self):
        self.image.h_flip()
        self.update_image()

    # Rotating buttons function
    def clockwise_rotate(self):
        self.image.rotate_clockwise()
        self.update_image()
    def unclockwise_rotate(self):
        self.image.rotate_unclockwise()
        self.update_image()

    # Invert button function
    def invert(self):
        self.image.auto_invert()
        self.update_image()
    # Auto Contrast button function
    def auto_contrast(self):
        self.image.auto_contrast()
        self.update_image()
    # Auto Sharpen button function
    def auto_sharpen(self):
        self.image.auto_sharpen()
        self.update_image()
    # Black and White button function
    def black_and_white(self):
        self.image.blackAndWhite()
        self.update_image()

    # re-loading backup photo
    def reset(self):
        self.gamaSlider.setValue(10)
        self.image = Image(self.backup)
        self.update_image()

    # saving current photo into the file
    def save(self):
        try:
            os.mkdir(os.path.join(os.curdir, "Edit-Captures"))
        except OSError as error:
            pass
        name = "Edit-Captures\\" + self.pictureName + "(Edit).JPG"
        cv2.imwrite(name, self.image.get_image())

def main():
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
