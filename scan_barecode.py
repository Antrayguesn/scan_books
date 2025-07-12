import cv2 as cv
import time


def detect_barecode(frame, show_frame=False, debug=False, filtre_barecode=('EAN_13'), exclude_barecodes=()):
    bc = cv.barcode.BarcodeDetector()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    ret, barecodes, barecodes_type, points = bc.detectAndDecodeWithType(gray)

    if debug and ret:
        frame = cv.polylines(gray, points.astype(int), True, (0, 255, 0), 3)
        for s, p in zip(barecodes, points):
            if s:
                frame = cv.putText(frame, s, p[1].astype(int),
                                   cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA)

    if debug:
        cv.imshow('frame', gray)

    if ret:
        if barecodes_type[0] in filtre_barecode:
            return barecodes[0]
    else:
        return None


def read_from_video_capture(dev_video=0, debug=False, show_frame=False):
    cap = cv.VideoCapture(dev_video)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    old_time = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Impossible de lire la capture")
            break

        if time.time() != old_time:
            yield frame
            old_time == time.time()

        if debug and cv.waitKey(1) == ord('q'):
            break
