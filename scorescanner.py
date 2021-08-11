import cv2 as cv
import gradio as gr
import numpy as np

GRADIO_COLOR_ORANGE = (231, 162, 59)
def main():
    iface = gr.Interface(analyze_image, gr.inputs.Image(), "image",
            examples=[["scores.png"]], server_port=8080, server_name="0.0.0.0")
    iface.launch()
    # show(analyze_image("scores.png"))

def analyze_image(img):
    # Load image
    # img = cv.imread("scores.png")

    gray = to_gray(img)

    processed = invert(adaptive_threshold(gray))

    contours, _hierachy = find_contours(processed)
    scoreboard_contour = find_largest_contour(contours)

    mask = np.zeros(processed.shape, np.uint8)
    draw_solid_contour_on_image(mask, scoreboard_contour)
    scoreboard = mask_image(processed, mask)

    contours, _hierachy = find_contours(scoreboard)
    cell_contours = find_cells(contours)
    contours_by_columns = separate_contours_in_columns(cell_contours)

    # for c, _centroid in contours_by_columns[2]:
    #     draw_contour_on_image(img, c)
    # show(img)

    lowest_centroid = max(column[-1][1][1] for column in contours_by_columns)
    y_pos = lowest_centroid + 100
    for col_nr, column in enumerate(contours_by_columns):
        predictions = []
        for row_nr, (contour, centroid) in enumerate(column):
            cell = extract_contour(scoreboard, contour)
            prediction = classify(cell)
            predictions.append(prediction)
            cv.imwrite(f"cells/{col_nr}_{row_nr}.jpg", cell)
            put_text(img, str(prediction), centroid, color=(0, 0, 0))
        column_sum = sum(predictions)
        bottom_centroid = column[-1][1]
        # second_bottom_centroid = column[-2][1]
        # y_distance = bottom_centroid[1] - second_bottom_centroid[1]
        # y_pos = bottom_centroid[1] + y_distance
        x_pos = bottom_centroid[0]
        put_text(img, str(column_sum), (x_pos, y_pos), color=GRADIO_COLOR_ORANGE)

    return img

    # show(img)

    # edges = cv.Canny(scoreboard, 100, 200)
    # lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    # for line in lines:
    #     x1,y1,x2,y2 = line[0]
    #     cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # show(img)

    # cv.destroyAllWindows()

def to_gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def morph_open(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

def adaptive_threshold(img):
    return cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY, 11, 2)

def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv.dilate(img, kernel)

def invert(img):
    return cv.bitwise_not(img, 0)

def blur(img):
    return cv.GaussianBlur(img, (5, 5), 0)

def find_contours(img):
    return cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

def find_largest_contour(contours):
    areas = [cv.contourArea(c) for c in contours]
    largest_contour_index = np.argmax(areas)
    return contours[largest_contour_index]

def find_cells(contours):
    area_limit = 3500
    return [c for c in contours if cv.contourArea(c) > area_limit]

def draw_solid_contour_on_image(img, contour):
    cv.drawContours(img, [contour], 0, 255, -1)

def draw_contour_on_image(img, contour):
    cv.drawContours(img, [contour], 0, (0, 255, 0), 2)

def mask_image(img, mask):
    return cv.bitwise_and(img, img, mask=mask)

def show(img, text='img'):
    cv.imshow(text, img)
    cv.waitKey(0)

def extract_contour(img, contour):
    x, y, w, h = cv.boundingRect(contour)
    return img[y:y+h, x:x+w]

def separate_contours_in_columns(contours):
    centroids = [get_centroid(c) for c in contours]
    threshold = 30
    columns = []
    for contour, centroid in zip(contours, centroids):
        for column in columns:
            if any(abs(centroid[0] - member[1][0]) <= threshold for member in column):
                column.append((contour, centroid))
                break
        else:
            columns.append([(contour, centroid)])
    sorted_columns = [sorted(column, key=lambda member: member[1][1]) for
            column in columns]
    return sorted(sorted_columns, key=lambda column: column[0][1][0])
    # return [[member[0] for member in column] for column in sorted_columns]

def get_centroid(contour):
    moments = cv.moments(contour)
    centroid_x = int(moments["m10"]/moments["m00"])
    centroid_y = int(moments["m01"]/moments["m00"])
    return centroid_x, centroid_y

def classify(img):
    return 5

def put_text(img, text, bottom_left_position, color=(255, 0, 0)):
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, text, bottom_left_position, font, 1, color, 2)

if __name__ == "__main__":
    main()
