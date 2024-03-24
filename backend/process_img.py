import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt

def load_image(image_path):
    return cv2.imread(image_path)

# img = cv2.imread("backend/data/receipts/IMG_1885.png")

#https://stackoverflow.com/questions/28816046/displaying-different-images-with-actual-size-in-matplotlib-subplot
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width, depth  = im_data.shape
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

def get_skew_angle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotate_image(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def preprocess_for_ocr(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove shadows
    rgb_planes = cv2.split(gray)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    
    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    # Apply a threshold to separate the text from the background
    _, binary = cv2.threshold(result_norm, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply a morphological operation (opening) to separate the text characters
    kernel = np.ones((2,2), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return opening

# img_new = preprocess_for_ocr(img)

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

def deskew_image(image):
    # from PIL import Image
    # Coordinates of non-black pixels.
    non_zero_coords = np.column_stack(np.where(image > 0))

    # Angles are in radians, but cv2.getRotationMatrix2D needs degrees.
    # Here, compute the angle between each non-black pixel and the horizontal axis.
    angles = np.arctan2(non_zero_coords[:, 0], non_zero_coords[:, 1])
    print(angles)
    rotation_angle = np.median(angles)
    print(rotation_angle)

    # Convert the median angle from radians to degrees and negate it to correct the rotation
    rotation_angle_degrees = -np.rad2deg(rotation_angle)/100
    print(rotation_angle_degrees)

    # Rotate the image around its center
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, rotation_angle_degrees, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Convert to PIL Image format to display in the notebook
    # rotated_pil = Image.fromarray(rotated)

    # Save the deskewed image
    # deskewed_path = './temp/deskewed_receipt.png'
    # rotated_pil.save(deskewed_path)

    return rotated

def save_image(name, img):
    return cv2.imwrite(name, img)

# cv2.imwrite('preprocessed_img.png', img_new)

def get_text_from_image(img):
    # Use Tesseract to convert the image to text
    text = pytesseract.image_to_string(img, lang='nor', config='--oem 1 --psm 6')
    return text

def save_raw_text(text, name):
    with open("backend/data/raw_text/" + name, "w") as file:
        file.write(text)