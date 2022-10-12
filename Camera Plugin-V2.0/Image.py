from libraries import *

# Image class used to save and make changes to current image on the screen.
class Image:
    # Source image in order to make change over multiple windows
    img = np.array

    # Initiations
    def __init__(self, img):
        self.img = img
        self.backup = img

    # Auto Contrast Function
    def auto_contrast(self):
        clip_hist_percent = 20
        try:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        except:
            gray = self.img

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)
        accumulator = [float(hist[0])]
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum / 100.0)
        clip_hist_percent /= 2.0
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        self.img = cv2.convertScaleAbs(self.img, alpha=alpha, beta=beta)
        self.backup = self.img
    # Auto Sharpen Function
    def auto_sharpen(self):
        try:
            self.img = cv2.detailEnhance(self.img, sigma_s=10, sigma_r=0.3)
        except:
            tmp = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            self.img = cv2.detailEnhance(tmp, sigma_s=10, sigma_r=0.3)
        self.backup = self.img
    # Unused!
    def auto_cartoon(self, style=0):
        edges1 = cv2.bitwise_not(cv2.Canny(self.img, 100, 200))
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
        dst = cv2.edgePreservingFilter(self.img, flags=2, sigma_s=64, sigma_r=0.25)

        if not style:
            # less blurry
            self.img = cv2.bitwise_and(dst, dst, mask=edges1)
        else:
            # more blurry
            self.img = cv2.bitwise_and(dst, dst, mask=edges2)
    # Auto Invert Function
    def auto_invert(self):
        self.img = cv2.bitwise_not(self.img)
        self.backup = self.img
    # Black and White Function
    def blackAndWhite(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.backup = self.img

    # Channel Streching Functions
    def strech_red_channel(self, start=0, end=255):
        b, g, r = cv2.split(self.backup)
        r[r < start] = start
        r[r > end] = end
        self.img = cv2.merge([b, g, r])
    def strech_blue_channel(self, start=0, end=255):
        b, g, r = cv2.split(self.backup)
        b[b< start] = start
        b[b > end] = end
        self.img = cv2.merge([b, g, r])
    def strech_green_channel(self, start=0, end=255):
        b, g, r = cv2.split(self.backup)
        g[g< start] = start
        g[g > end] = end
        self.img = cv2.merge([b, g, r])
    def strech_bw_channel(self, start=0, end=255):
        b = self.backup.copy()
        b[b< start] = start
        b[b > end] = end
        self.img = b

    # Applying channel changes
    def apply_bw_channel(self):
        self.backup = self.img
        img = self.img

    # Gama Adjust Function
    def gama_adjust(self, gamma):
        if gamma==0:
            gamma+=0.1
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        self.img = cv2.LUT(self.backup, table)
        #self.backup = self.img

    # Rotation Functions
    def rotate_clockwise(self):
        self.img = cv2.rotate(self.img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    def rotate_unclockwise(self):
        self.img = cv2.rotate(self.img, cv2.cv2.ROTATE_90_CLOCKWISE)

    # Return image size
    def get_shape(self):
        return self.img.shape

    # Reload source image
    def reset(self, flip=None):
        if flip is None:
            flip = [False, False]
        self.img = deepcopy(self.img_copy)
        if flip[0]:
            self.img = cv2.flip(self.img, 0)
        if flip[1]:
            self.img = cv2.flip(self.img, 1)

    # Flip Functions
    def h_flip(self):
        self.img = cv2.flip(self.img, 1)
    def v_flip(self):
        self.img = cv2.flip(self.img, 0)

    # Return image
    def get_image(self):
        img = self.img
        return img