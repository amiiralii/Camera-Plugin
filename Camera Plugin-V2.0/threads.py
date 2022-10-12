from libraries import *

# QThread class for handling gif icons whenever update button pressed
class LoadingGifThread(QThread):
    # One signal per Each gif
    gif1 = pyqtSignal()
    gif2 = pyqtSignal()
    gif3 = pyqtSignal()
    gif4 = pyqtSignal()
    alert = pyqtSignal()

    def __init__(self, iso, aperture, exposure, shutter, speed) -> None:
        super(LoadingGifThread, self).__init__()
        self.camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder="captures\\", collection_name="Capture")
        self.i = iso
        self.a = aperture
        self.o = exposure
        self.s = shutter
        self.p = speed

    def run(self):
        # Turn down each gifs after it commands
        self.camera.set_iso_number(self.i)
        self.gif1.emit()
        self.camera.set_aperture_number(self.a)
        self.gif2.emit()
        self.camera.set_exposure_comp_number(self.o)
        self.gif3.emit()
        self.camera.set_shutter_speed_number(self.s, self.p)

        # Saving Camera setting details each time settings change
        t = datetime.datetime.now()
        current_time = str(t.strftime("%d")) + "." + str(t.strftime("%m")) + "." + str(t.strftime("%Y")) + "." + str(
            t.strftime("%H")) + "." + str(t.strftime("%M"))
        try:
            os.mkdir(os.path.join(os.curdir, "Camera-setting-records"))
        except OSError as error:
            pass
        record_name = "Camera-setting-records\\" + current_time + ".txt"
        self.camera.show_camera_info(record_name)
        self.gif4.emit()
        self.alert.emit()

# QThread class for handling Waiting time between pressing apply button and start capturing
class WaitingToStartThread(QThread):
    update = pyqtSignal(int)
    end = pyqtSignal()
    def __init__(self, waiting_len) -> None:
        super(WaitingToStartThread, self).__init__()
        self.duration = waiting_len

    def run(self):
        for i in range(self.duration):
            time.sleep(1)
            val = ((i + 1) / self.duration) * 100
            self.update.emit(val)
        self.end.emit()

# QThread class for handling Waiting time between each capture
class WaitingToCaptureThread(QThread):
    end = pyqtSignal(int)
    update = pyqtSignal(int)

    def __init__(self, waiting_len) -> None:
        super(WaitingToCaptureThread, self).__init__()
        self.duration = waiting_len

    def run(self):
        for i in range(self.duration):
            time.sleep(0.1)
            val = ((i + 1) / self.duration) * 100
            self.update.emit(val)
        self.end.emit(self.duration)
