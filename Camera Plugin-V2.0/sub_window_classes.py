from libraries import *
from threads import *
from Image import *


# QWidget class for showing alerts
class AlertSubWindow(QWidget):
    def __init__(self):
        super(AlertSubWindow, self).__init__()

        # Loading ui file
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\UI files\\alert.ui", self)

        # Massage
        self.Massage = self.findChild(QLabel, "Massage")
        self.Massage.setText('Sub Window')
        self.Massage.setAlignment(Qt.AlignCenter)
        self.Massage.setStyleSheet('font-size:40px')

        # Sub Massage
        self.SubMassage = self.findChild(QLabel, "SubMassage")
        self.SubMassage.setAlignment(Qt.AlignCenter)
        self.SubMassage.setStyleSheet('font-size:20px')

    # set main massage text
    def set_text(self, msg):
        self.Massage.setText(msg)

    # set main massage text
    def set_sub_text(self, msg):
        self.SubMassage.setText(msg)

# Qwidget class for whole camera tools window
class CameraToolsSubWindow(QWidget):
    def __init__(self):
        super(CameraToolsSubWindow, self).__init__()

        self.camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder="captures\\", collection_name="Capture")
        self.alert_sub_window = AlertSubWindow()
        # Loading ui and css file
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\UI files\\Camera-Tools.ui", self)
        self.setStyleSheet(open('style\\camera_setting_style.css').read())

        # Finding objects from file and set to class attributes
        ## Setting objects
        self.ISOComboBox = self.findChild(QComboBox, "ISOComboBox")
        self.ApertureComboBox = self.findChild(QComboBox, "ApertureComboBox")
        self.ShutterComboBox = self.findChild(QComboBox, "ShutterComboBox")
        self.ExpoComboBox = self.findChild(QComboBox, "ExpoComboBox")
        self.UpdateValueButton = self.findChild(QPushButton, "UpdateValueButton")
        self.UpdateValueButton.setStyleSheet(open('style\\camera_setting_style.css').read())
        self.LoadLabel1 = self.findChild(QLabel, "LoadLabel1")
        self.LoadLabel2 = self.findChild(QLabel, "LoadLabel2")
        self.LoadLabel3 = self.findChild(QLabel, "LoadLabel3")
        self.LoadLabel4 = self.findChild(QLabel, "LoadLabel4")
        self.set_initial_gifs()
        ## Time Capturing Objects
        self.StartTime = self.findChild(QDateTimeEdit, "StartTime")
        dt = datetime.datetime.now()
        self.StartTime.setDateTime(dt)
        self.waitToStartProgressBar = self.findChild(QProgressBar, "waitToStartProgressBar")
        self.CapturingCycleSpinBox = self.findChild(QSpinBox, "CapturingCycleSpinBox")
        self.TotallCaptureNumber = self.findChild(QSpinBox, "TotallCaptureNumber")
        self.ApplyButton = self.findChild(QPushButton, "ApplyButton")
        self.ApplyButton.setStyleSheet(open('style\\camera_setting_style.css').read())
        self.LCDNumber = self.findChild(QLCDNumber, "LCDNumber")
        self.progressBar = self.findChild(QProgressBar, "progressBar")

        # Adding items to combo boxes
        for i in range(6):
            self.ISOComboBox.addItem("")
        for i in range(17):
            self.ApertureComboBox.addItem("")
        for i in range(51):
            self.ShutterComboBox.addItem("")
        for i in range(25):
            self.ExpoComboBox.addItem("")

        self.set_initial_values()

        # Connecting Buttons to related functions
        self.UpdateValueButton.clicked.connect(self.retreive_setting_data)
        self.ApplyButton.clicked.connect(self.startCapturing)

    # checking whether camera is connect or not
    def check_camera(self):
        self.camera.show_camera_info("connectivity_check_@.txt")
        try:
            f = open("connectivity_check_@.txt")
            f.close()
            os.remove("connectivity_check_@.txt")
            return 'yes'
        except IOError:
            self.alert_sub_window.set_text("Camera is not Connected!")
            self.alert_sub_window.show()
            return 'no'

    # derive input data from combo boxes for updating values
    def retreive_setting_data(self):
        camera_conectivity_state = self.check_camera()
        if (camera_conectivity_state=='yes'):
            iso = self.ISOComboBox.currentText()
            aperture = self.ApertureComboBox.currentText()
            exposure = self.ExpoComboBox.currentText()
            shutter = self.ShutterComboBox.currentText()
            speed = "1s"

            self.scalegif()
            self.LoadingThread = LoadingGifThread(iso, aperture, exposure, shutter, speed)
            self.LoadingThread.start()
            self.LoadingThread.gif1.connect(lambda: self.LoadingGif1.setScaledSize(QtCore.QSize(1, 1)))
            self.LoadingThread.gif2.connect(lambda: self.LoadingGif2.setScaledSize(QtCore.QSize(1, 1)))
            self.LoadingThread.gif3.connect(lambda: self.LoadingGif3.setScaledSize(QtCore.QSize(1, 1)))
            self.LoadingThread.gif4.connect(lambda: self.LoadingGif4.setScaledSize(QtCore.QSize(1, 1)))
            self.LoadingThread.alert.connect(self.show_updated_alert)

    # showing updated alert when updating is done
    def show_updated_alert(self):
        self.alert_sub_window.set_text("Camera Settings Updated !")
        self.alert_sub_window.set_sub_text("Complete info saved in records.")
        self.alert_sub_window.show()

    # set initial values for combo boxes
    def set_initial_values(self):
        self.ISOComboBox.setItemText(0, "100")
        self.ISOComboBox.setItemText(1, "200")
        self.ISOComboBox.setItemText(2, "400")
        self.ISOComboBox.setItemText(3, "800")
        self.ISOComboBox.setItemText(4, "1600")
        self.ISOComboBox.setItemText(5, "3200")

        self.ApertureComboBox.setItemText(0,  "4.0")
        self.ApertureComboBox.setItemText(1,  "4.5")
        self.ApertureComboBox.setItemText(2,  "5.0")
        self.ApertureComboBox.setItemText(3,  "5.6")
        self.ApertureComboBox.setItemText(4,  "6.3")
        self.ApertureComboBox.setItemText(5,  "7.1")
        self.ApertureComboBox.setItemText(6,  "8.0")
        self.ApertureComboBox.setItemText(7,  "9.0")
        self.ApertureComboBox.setItemText(8,  "10.0")
        self.ApertureComboBox.setItemText(9,  "11.0")
        self.ApertureComboBox.setItemText(10,  "13.0")
        self.ApertureComboBox.setItemText(11,  "14.0")
        self.ApertureComboBox.setItemText(12,  "16.0")
        self.ApertureComboBox.setItemText(13,  "18.0")
        self.ApertureComboBox.setItemText(14,  "20.0")
        self.ApertureComboBox.setItemText(15,  "22.0")
        self.ApertureComboBox.setItemText(16,  "25.0")

        self.ExpoComboBox.setCurrentText( "-1")
        self.ExpoComboBox.setItemText(0,  "-3")
        self.ExpoComboBox.setItemText(1,  "-3 2/3")
        self.ExpoComboBox.setItemText(2,  "-2.5")
        self.ExpoComboBox.setItemText(3,  "-2 1/3")
        self.ExpoComboBox.setItemText(4,  "-2")
        self.ExpoComboBox.setItemText(5,  "-1 2/3")
        self.ExpoComboBox.setItemText(6,  "-1.5")
        self.ExpoComboBox.setItemText(7,  "-1 1/3")
        self.ExpoComboBox.setItemText(8,  "-1")
        self.ExpoComboBox.setItemText(9,  "-2/3")
        self.ExpoComboBox.setItemText(10,  "-0.5")
        self.ExpoComboBox.setItemText(11,  "-1/3")
        self.ExpoComboBox.setItemText(12,  "0.0")
        self.ExpoComboBox.setItemText(13,  "+1/3")
        self.ExpoComboBox.setItemText(14,  "+0.5")
        self.ExpoComboBox.setItemText(15,  "+2/3")
        self.ExpoComboBox.setItemText(16,  "+1")
        self.ExpoComboBox.setItemText(17,  "+1 1/3")
        self.ExpoComboBox.setItemText(18,  "+1.5")
        self.ExpoComboBox.setItemText(19,  "+1 2/3")
        self.ExpoComboBox.setItemText(20,  "+2.0")
        self.ExpoComboBox.setItemText(21,  "+2 1/3")
        self.ExpoComboBox.setItemText(22,  "+2.5")
        self.ExpoComboBox.setItemText(23,  "+2 2/3")
        self.ExpoComboBox.setItemText(24,  "+3.0")

        self.ShutterComboBox.setItemText(0, "1/4000")
        self.ShutterComboBox.setItemText(1, "1/3200")
        self.ShutterComboBox.setItemText(2, "1/2500")
        self.ShutterComboBox.setItemText(3, "1/2000")
        self.ShutterComboBox.setItemText(4, "1/1600")
        self.ShutterComboBox.setItemText(5, "1/1250")
        self.ShutterComboBox.setItemText(6, "1/1000")
        self.ShutterComboBox.setItemText(7, "1/800")
        self.ShutterComboBox.setItemText(8, "1/640")
        self.ShutterComboBox.setItemText(9, "1/500")
        self.ShutterComboBox.setItemText(10, "1/400")
        self.ShutterComboBox.setItemText(11, "1/320")
        self.ShutterComboBox.setItemText(12, "1/250")
        self.ShutterComboBox.setItemText(13, "1/200")
        self.ShutterComboBox.setItemText(14, "1/160")
        self.ShutterComboBox.setItemText(15, "1/125")
        self.ShutterComboBox.setItemText(16, "1/100")
        self.ShutterComboBox.setItemText(17, "1/80")
        self.ShutterComboBox.setItemText(18, "1/60")
        self.ShutterComboBox.setItemText(19, "1/50")
        self.ShutterComboBox.setItemText(20, "1/40")
        self.ShutterComboBox.setItemText(21, "1/30")
        self.ShutterComboBox.setItemText(22, "1/25")
        self.ShutterComboBox.setItemText(23, "1/20")
        self.ShutterComboBox.setItemText(24, "1/15")
        self.ShutterComboBox.setItemText(25, "1/13")
        self.ShutterComboBox.setItemText(26, "1/10")
        self.ShutterComboBox.setItemText(27, "1/8")
        self.ShutterComboBox.setItemText(28, "1/5")
        self.ShutterComboBox.setItemText(29, "1/4")
        self.ShutterComboBox.setItemText(30, "0.3")
        self.ShutterComboBox.setItemText(31, "0.4")
        self.ShutterComboBox.setItemText(32, "0.5")
        self.ShutterComboBox.setItemText(33, "0.6")
        self.ShutterComboBox.setItemText(34, "0.8")
        self.ShutterComboBox.setItemText(35, "1")
        self.ShutterComboBox.setItemText(36, "1.3")
        self.ShutterComboBox.setItemText(37, "0.6")
        self.ShutterComboBox.setItemText(38, "2")
        self.ShutterComboBox.setItemText(39, "2.5")
        self.ShutterComboBox.setItemText(40, "3.2")
        self.ShutterComboBox.setItemText(41, "4")
        self.ShutterComboBox.setItemText(42, "5")
        self.ShutterComboBox.setItemText(43, "6")
        self.ShutterComboBox.setItemText(44, "8")
        self.ShutterComboBox.setItemText(45, "10")
        self.ShutterComboBox.setItemText(46, "13")
        self.ShutterComboBox.setItemText(47, "15")
        self.ShutterComboBox.setItemText(48, "20")
        self.ShutterComboBox.setItemText(49, "25")
        self.ShutterComboBox.setItemText(50, "30")

    # show loading gifs before updating values
    def scalegif(self):
        self.LoadingGif1.setScaledSize(QtCore.QSize(40, 40))
        self.LoadingGif2.setScaledSize(QtCore.QSize(40, 40))
        self.LoadingGif3.setScaledSize(QtCore.QSize(40, 40))
        self.LoadingGif4.setScaledSize(QtCore.QSize(40, 40))

    # making gifs
    def set_initial_gifs(self):
        self.LoadingGif1 = QMovie("images\\loader.gif")
        self.LoadingGif1.setScaledSize(QtCore.QSize(40, 40))
        self.LoadLabel1.setMovie(self.LoadingGif1)
        self.LoadingGif1.start()
        self.LoadingGif1.setScaledSize(QtCore.QSize(1, 1))

        self.LoadingGif2 = QMovie("images\\loader.gif")
        self.LoadingGif2.setScaledSize(QtCore.QSize(40, 40))
        self.LoadLabel2.setMovie(self.LoadingGif2)
        self.LoadingGif2.start()
        self.LoadingGif2.setScaledSize(QtCore.QSize(1, 1))

        self.LoadingGif3 = QMovie("images\\loader.gif")
        self.LoadingGif3.setScaledSize(QtCore.QSize(40, 40))
        self.LoadLabel3.setMovie(self.LoadingGif3)
        self.LoadingGif3.start()
        self.LoadingGif3.setScaledSize(QtCore.QSize(1, 1))

        self.LoadingGif4 = QMovie("images\\loader.gif")
        self.LoadingGif4.setScaledSize(QtCore.QSize(40, 40))
        self.LoadLabel4.setMovie(self.LoadingGif4)
        self.LoadingGif4.start()
        self.LoadingGif4.setScaledSize(QtCore.QSize(1, 1))

    # waiting until capturing cycle start time
    def startCapturing(self):
        self.multi_capture_number = 0
        t = datetime.datetime.now()
        start_time = self.StartTime.dateTime().toPyDateTime()
        wait_to_start = int((start_time - t).total_seconds())

        self.waitToStartThread = WaitingToStartThread(wait_to_start)
        self.waitToStartThread.update.connect(self.setWaitProgressValue)
        self.waitToStartThread.end.connect(self.capturing)
        self.waitToStartThread.start()

    # start the capturing cycle
    def capturing(self):
        camera_conectivity_state = self.check_camera()
        if (camera_conectivity_state == 'yes'):
            n = self.TotallCaptureNumber.value()
            k = n
            self.LCDNumber.display(k)
            self.LCDNumber.repaint()
            waiting = self.CapturingCycleSpinBox.value()
            self.waitAndCapture(waiting*10)

    # waiting for capturing each photo
    def waitAndCapture(self, t):
        self.waitToCaptureThread = WaitingToCaptureThread(t)
        self.waitToCaptureThread.update.connect(self.setWaitProgressValue2)
        self.waitToCaptureThread.end.connect(self.capture)
        self.waitToCaptureThread.start()

    # take picture command and update lcd number
    def capture(self, time):
        # taking picture
        self.camera.reset_image_index(self.multi_capture_number)
        t = datetime.datetime.now()
        current_time = str(t.strftime("%d")) + "." + str(t.strftime("%m")) + "." + str(t.strftime("%Y")) + "." + str(
            t.strftime("%H")) + "." + str(t.strftime("%M"))
        self.camera.set_save_folder(current_time + "\\")
        t = self.camera.capture_single_image(autofocus=True)
        self.multi_capture_number += 1

        #updating lcd number
        k = self.LCDNumber.value()
        self.LCDNumber.display(k-1)
        self.LCDNumber.repaint()
        if self.LCDNumber.value() > 0:
               self.waitAndCapture(time)
        else:
            self.clear()

    # reset inputs after time capturing
    def clear(self):
        self.TotallCaptureNumber.clear()
        self.CapturingCycleSpinBox.clear()
        self.StartTime.clear()
        self.progressBar.reset()
        self.waitToStartProgressBar.reset()

    # updating first progress bar
    def setWaitProgressValue(self, val):
        self.waitToStartProgressBar.setValue(int(val))

    # updating second progress bar
    def setWaitProgressValue2(self, val):
        self.progressBar.setValue( val )
