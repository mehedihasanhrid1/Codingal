import cv2
import numpy as np

def apply_filter(image, ftype):
    img = image.copy()
    if ftype == "red_tint":
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == "green_tint":
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == "blue_tint":
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sob = cv2.bitwise_or(sx.astype("uint8"), sy.astype("uint8"))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, 100, 200)
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)
    elif ftype == "sketch":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        blend = cv2.divide(gray, 255 - blur, scale=256)
        img = cv2.cvtColor(blend, cv2.COLOR_GRAY2BGR)
    elif ftype == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img = cv2.transform(image, kernel)
        img = np.clip(img, 0, 255).astype(np.uint8)
    elif ftype == "hdr":
        img = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return img

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    ftype = "original"
    print("Keys: r=Red, g=Green, b=Blue, s=Sobel, c=Canny, t=Cartoon, k=Sketch, h=HDR, p=Sepia, q=Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break

        out = apply_filter(frame, ftype)
        cv2.imshow("Live Filters", out)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'): ftype = "red_tint"
        elif key == ord('g'): ftype = "green_tint"
        elif key == ord('b'): ftype = "blue_tint"
        elif key == ord('s'): ftype = "sobel"
        elif key == ord('c'): ftype = "canny"
        elif key == ord('t'): ftype = "cartoon"
        elif key == ord('k'): ftype = "sketch"
        elif key == ord('h'): ftype = "hdr"
        elif key == ord('p'): ftype = "sepia"
        elif key == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
