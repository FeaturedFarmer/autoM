import cv2


#Mouse event
def mouse(event, x, y, flags, param):
    global flag, horizontal, vertical, flag_hor, flag_ver, dx, dy, sx, sy, dst, x1, y1, x2, y2, x3, y3, f1, f2
    global zoom, scroll_har, scroll_var, img_w, img_h, img, dst1, win_w, win_h, show_w, show_h
    if event == cv2.EVENT_LBUTTONDOWN: # Left click
        if flag == 0:
            if horizontal and 0 <x <win_w and win_h-scroll_w <y <win_h:
                flag_hor = 1 # The mouse is on the horizontal scroll bar
            elif vertical and win_w-scroll_w <x <win_w and 0 <y <win_h:
                flag_ver = 1 # The mouse is on the vertical scroll bar
            if flag_hor or flag_ver:
                flag = 1 # Make the scroll bar vertical
                x1, y1, x2, y2, x3, y3 = x, y, dx, dy, sx, sy # Make the mouse move distance relative to the initial scroll bar click position, not relative to the previous position
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON): # Hold down the left button and drag
        if flag == 1:
            if flag_hor:
                w = (x-x1)/2 # Moving width
                dx = x2 + w * f1 # original image x
                if dx <0: # position correction
                    dx = 0
                elif dx> img_w-show_w:
                    dx = img_w-show_w
                sx = x3 + w # scroll bar x
                if sx <0: # position correction
                    sx = 0
                elif sx> win_w-scroll_har:
                    sx = win_w-scroll_har
            if flag_ver:
                h = y-y1 # moving height
                dy = y2 + h * f2 # original image y
                if dy <0: # position correction
                    dy = 0
                elif dy> img_h-show_h:
                    dy = img_h-show_h
                sy = y3 + h # scroll bar y
                if sy <0: # position correction
                    sy = 0
                elif sy> win_h-scroll_var:
                    sy = win_h-scroll_var
            dx, dy = int(dx), int(dy)
            img1 = img[dy:dy + show_h, dx:dx + show_w] # Take a screenshot for display
            print(dy, dy + show_h, dx, dx + show_w)
            dst = img1.copy()
    elif event == cv2.EVENT_LBUTTONUP: # Left key release
        flag, flag_hor, flag_ver = 0, 0, 0
        x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0
    elif event == cv2.EVENT_MOUSEWHEEL: # scroll wheel
        if flags> 0: # scroll wheel up
            zoom += wheel_step
            if zoom> 1 + wheel_step * 20: # zoom factor adjustment
                zoom = 1 + wheel_step * 20
        else: # scroll wheel down
            zoom -= wheel_step
            if zoom <wheel_step: # zoom factor adjustment
                zoom = wheel_step
        zoom = round(zoom, 2) # Take 2 significant digits
        img_w, img_h = int(img_original_w * zoom), int(img_original_h * zoom) # zooming is relative to the original image, not iteration
        img_zoom = cv2.resize(img_original, (img_w, img_h), interpolation=cv2.INTER_AREA)
        horizontal, vertical = 0, 0
        if img_h <= win_h and img_w <= win_w:
            dst1 = img_zoom
            cv2.resizeWindow("img", img_w, img_h)
            scroll_har, scroll_var = 0, 0
            f1, f2 = 0, 0
        else:
            if img_w> win_w and img_h> win_h:
                horizontal, vertical = 1, 1
                scroll_har, scroll_var = win_w * show_w/img_w, win_h * show_h/img_h
                f1, f2 = (img_w-show_w)/(win_w-scroll_har), (img_h-show_h)/(win_h-scroll_var)
            elif img_w> win_w and img_h <= win_h:
                show_h = img_h
                win_h = show_h + scroll_w
                scroll_har, scroll_var = win_w * show_w/img_w, 0
                f1, f2 = (img_w-show_w)/(win_w-scroll_har), 0
            elif img_w <= win_w and img_h> win_h:
                show_w = img_w
                win_w = show_w + scroll_w
                scroll_har, scroll_var = 0, win_h * show_h/img_h
                f1, f2 = 0, (img_h-show_h)/(win_h-scroll_var)
            dx, dy = dx * zoom, dy * zoom # After zooming, display the coordinates of the relative zoomed image
            sx, sy = dx/img_w * (win_w-scroll_har), dy/img_h * (win_h-scroll_var)
            img = img_zoom.copy() # Make the zoomed picture the original picture
            dx, dy = int(dx), int(dy)
            img1 = img[dy:dy + show_h, dx:dx + show_w]
            dst = img1.copy()

    if horizontal and vertical:
        sx, sy = int(sx), int(sy)
        # Draw a picture on dst1 instead of dst to avoid continuous refreshing of mouse events so that the displayed picture is constantly filled
        dst1 = cv2.copyMakeBorder(dst, 0, scroll_w, 0, scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (sx, show_h), (int(sx + scroll_har), win_h), (181, 181, 181), -1) # draw horizontal scroll bar
        cv2.rectangle(dst1, (show_w, sy), (win_w, int(sy + scroll_var)), (181, 181, 181), -1) # draw vertical scroll bar
    elif horizontal == 0 and vertical:
        sx, sy = int(sx), int(sy)
        dst1 = cv2.copyMakeBorder(dst, 0, 0, 0, scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (show_w, sy), (win_w, int(sy + scroll_var)), (181, 181, 181), -1) # draw vertical scroll bar
    elif horizontal and vertical == 0:
        sx, sy = int(sx), int(sy)
        dst1 = cv2.copyMakeBorder(dst, 0, scroll_w, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (sx, show_h), (int(sx + scroll_har), win_h), (181, 181, 181), -1) # draw horizontal scroll bar
    cv2.imshow("img", dst1)
    cv2.waitKey(1)


img_original = cv2.imread("test.jpg") # here needs to be replaced with an image larger than img_w * img_h
img_original_h, img_original_w = img_original.shape[0:2] # original image width and height
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.moveWindow("img", 300, 100)
img = img_original.copy()
img_h, img_w = img.shape[0:2] # original image width and height
show_h, show_w = 600, 800 # Display picture width and height
horizontal, vertical = 0, 0 # Whether the original image exceeds the displayed image
dx, dy = 0, 0 # Display the coordinates of the picture relative to the original picture
scroll_w = 16 # scroll bar width
sx, sy = 0, 0 # The coordinates of the scroll block relative to the scroll bar
flag, flag_hor, flag_ver = 0, 0, 0 # Mouse operation type, whether the mouse is on the horizontal scroll bar, and whether the mouse is on the vertical scroll bar
x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0 # intermediate variables
win_w, win_h = show_w + scroll_w, show_h + scroll_w # window width and height
scroll_har, scroll_var = win_w * show_w/img_w, win_h * show_h/img_h # scroll bar horizontal and vertical length
wheel_step, zoom = 0.05, 1 # zoom factor, zoom value
zoom_w, zoom_h = img_w, img_h # zoom image width and height
f1, f2 = (img_w-show_w)/(win_w-scroll_har), (img_h-show_h)/(win_h-scroll_var) # The proportion of the movable part of the original image to the movable part of the scroll bar

if img_h <= show_h and img_w <= show_w:
    cv2.imshow("img", img)
else:
    if img_w> show_w:
        horizontal = 1
    if img_h> show_h:
        vertical = 1
    i = img[dy:dy + show_h, dx:dx + show_w]
    dst = i.copy()
cv2.resizeWindow("img", win_w, win_h)
cv2.setMouseCallback('img', mouse)

cv2.waitKey()
cv2.destroyAllWindows()
