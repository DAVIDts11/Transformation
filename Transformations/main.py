# Submitted  by :
#                 Tsibulsky David  309444065
#                 Haham Omri       308428226
#                 Coral Rubilar    316392877

from tkinter import *
import numpy as np
import math
from copy import deepcopy
import os

# Global variables:
WIDTH = 1000
HEIGHT = 600
shapes_from_file = dict()
init_position = dict()
fileParams =""  #File Relative Path
first_point = True
first_point_x = 0
first_point_y = 0


def write_to_the_screen(my_canvas, my_text ,color):
    my_canvas.create_text(465, 15, fill=color, font="Times 20 italic bold",
                          text=my_text)

def clear(my_canvas):
    """
     To clear all the canvas
     """
    my_canvas.delete('all')


def create_circle(x, y, r, my_canvas):
    """
    Draw circle using create_oval tkinter function
    :param x , y :center coordinates
    :param r:  radius
    :param my_canvas: canvas
    """
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    my_canvas.create_oval(x0, y0, x1, y1, width=5, outline='blue')


def getImageParams():
    """
    This function is read parameters from a file, parsing it and returns
    three arrays with lines, circels and bezier curves.
    Uses global "fileParams" - File Relative Path
    :param fileParams: file with image params
    :return:shapes from file : dict that includes:
                1.Lines :  array of dicts with x1,y1,x2,y2
                2.Circles :  array of dicts with centerX,centerY ,Radius
                3.BezierCurves: array of dicts with x1,y1,x2,y2,x3,y3,x4,y4
    """
    try:
        Lines = []
        Circles = []
        BezierCurves = []
        shape = {"lines": False, "Circles": False, "BezierCurves": False}
        with open(fileParams, "r") as file:
            for line in file:
                if (line == "lines:\n"):
                    shape["lines"] = True
                    shape["Circles"] = False
                    shape["BezierCurves"] = False
                    continue
                elif (line == "Circles:\n"):
                    shape["lines"] = False
                    shape["Circles"] = True
                    shape["BezierCurves"] = False
                    continue
                elif (line == "BezierCurves:\n"):
                    shape["lines"] = False
                    shape["Circles"] = False
                    shape["BezierCurves"] = True
                    continue
                if (shape["lines"]):
                    lines_from_file = line.split(";")
                    for line_to_draw in lines_from_file:
                        if (line_to_draw is not "\n"):
                            line_params = line_to_draw.split(",", 4)
                            new_line = {"x1": float(line_params[0]), "y1": float(line_params[1]),
                                        "x2": float(line_params[2]), "y2": float(line_params[3])}
                            Lines.append(new_line)
                elif shape["Circles"]:
                    circles_from_file = line.split(";")
                    for circles_to_draw in circles_from_file:
                        if (circles_to_draw is not "\n"):
                            circles_params = circles_to_draw.split(",", 4)
                            new_circle = {"x1": float(circles_params[0]), "y1": float(circles_params[1]),
                                          "radius": float(circles_params[2])}
                            # new_circle = {"x1":float(circles_params[0]),"y1":float(circles_params[1]),"x2":float(circles_params[2]),"y2":float(circles_params[3])}
                            Circles.append(new_circle)
                elif shape["BezierCurves"]:
                    bezierCurves_from_file = line.split(";")
                    for bezierCurves_to_draw in bezierCurves_from_file:
                        if (bezierCurves_to_draw is not "\n"):
                            bezierCurves_params = bezierCurves_to_draw.split(",", 8)
                            new_bezierCurves = {"x1": float(bezierCurves_params[0]), "y1": float(bezierCurves_params[1]),
                                                "x2": float(bezierCurves_params[2]), "y2": float(bezierCurves_params[3]),
                                                "x3": float(bezierCurves_params[4]), "y3": float(bezierCurves_params[5]),
                                                "x4": float(bezierCurves_params[6]), "y4": float(bezierCurves_params[7])}
                            BezierCurves.append(new_bezierCurves)

        shapes_from_file = {"Lines": Lines, "Circles": Circles, "BezierCurves": BezierCurves}
        return shapes_from_file
    except Exception as e:
        write_to_the_screen(my_canvas,str(e) + "!!!", "red" )

def find_image_location_params(initParams = False):
    """
    This function is finding the centre of the image, and the borders  -  min/max x , min\max y .
    Uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    Uses global param  init_position: dict with array of lines params list , circles params list and bezier curves params list;
    :param: initParams - bool if True the function uses init_position , else uses shapes_from_file
    :return: image_location_params : dict that contain center of the image params :(x,y) , and edges params: (xMin,xMax,yMin,yMax)
    """
    xMax = -1000000
    xMin = 1000000
    yMax = -1000000
    yMin = 1000000
    global shapes_from_file ,init_position

    if(initParams):
        params = init_position
    else:
        params = shapes_from_file

    for shape_type in params:
        for shape in params[shape_type]:
            for point_coordinate in shape:
                if "y" in str(point_coordinate):
                    to_comper = shape[point_coordinate] if shape_type is not "Circles" else shape[point_coordinate] + \
                                                                                            shape["radius"]
                    if to_comper > yMax:
                        yMax = to_comper
                    to_comper = shape[point_coordinate] if shape_type is not "Circles" else shape[point_coordinate] - \
                                                                                            shape["radius"]
                    if to_comper < yMin:
                        yMin = to_comper
                elif "x" in str(point_coordinate):
                    to_comper = shape[point_coordinate] if shape_type is not "Circles" else shape[point_coordinate] + \
                                                                                            shape["radius"]
                    if to_comper > xMax:
                        xMax = to_comper
                    to_comper = shape[point_coordinate] if shape_type is not "Circles" else shape[point_coordinate] - \
                                                                                            shape["radius"]
                    if to_comper < xMin:
                        xMin = to_comper
    x_centre = (xMax + xMin) / 2
    y_centre = (yMax + yMin) / 2
    image_edges_params = {"xMax":xMax,"xMin":xMin,"yMax":yMax,"yMin":yMin}
    centre = {"x_centre": x_centre, "y_centre": y_centre}
    image_location_params = {"centre":centre,"edges":image_edges_params}
    return image_location_params


def draw_the_shapes(shapes_from_file, my_canvas):
    """
    This function is geting dict with shapes params (lines , circles and bezier curves) , and draw
        them on the canvas  .
    :param shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas to draw all the shapes on .
    """
    for line in shapes_from_file["Lines"]:
        my_canvas.create_line(line["x1"], line["y1"], line["x2"], line["y2"], fill='blue', width=5)
    for circle in shapes_from_file["Circles"]:
        create_circle(circle["x1"], circle["y1"], circle["radius"], my_canvas)
        # my_canvas.create_oval(circle["x1"], circle["y1"], circle["x2"], circle["y2"], width=5, outline='blue')
    for curve in shapes_from_file["BezierCurves"]:
        my_canvas.create_line(curve["x1"], curve["y1"], curve["x2"], curve["y2"], curve["x3"], curve["y3"], curve["x4"],
                              curve["y4"], fill='blue', width=5, smooth=1)



def check_border_overflow(point_coordinate_key,point_coordinate_value, msg):
    """
    Checking if the point is out of border  , and if so - raise the exception
    :param point_coordinate_key: point coordinate key : x1,y1...
    :param point_coordinate_value: point coordinate value
    :param msg: messege to raise
    """
    messege = "Can't " + msg + " more -  Out of boarder"
    if "y" in str(point_coordinate_key):
        if point_coordinate_value > HEIGHT or point_coordinate_value < 0:
            raise Exception(messege)

    elif "x" in str(point_coordinate_key):
        if point_coordinate_value > WIDTH or point_coordinate_value < 0:
            raise Exception(messege)




def scale(my_canvas, mult_by, nkudat_ihus=False):
    """
     This function is scaling up and down all the points of the shapes of the image
        and draw it on the canvas
    uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas to draw all the shapes on .
    :param mult_by: the number to mulifly all the coordinats of the points by ,
                        for scale up :  mult_by should be > 1
                        for scale down :  mult_by should be < 1
    :param nkudat_ihus : if nkudat_ihus is True - the function doe's not draw thw image , and there is no checking for "out of boarder"
    """
    global shapes_from_file
    try:
        copy_shapes_from_file = deepcopy(shapes_from_file)
        for shape_type in copy_shapes_from_file:
            for shape in copy_shapes_from_file[shape_type]:
                for point_coordinate in shape:
                    shape[point_coordinate] = shape[point_coordinate] * mult_by

                    if not nkudat_ihus:
                        # checking if the point is out of boarder or to small :
                        check_border_overflow(point_coordinate, shape[point_coordinate], "scale")

                        #checking if the shape is to small :
                        if shape[point_coordinate] < 1  and shape[point_coordinate] >= 0 :
                            raise Exception("Can't scale  -  To small")

        shapes_from_file = deepcopy(copy_shapes_from_file)
        if not nkudat_ihus:
            clear(my_canvas)
            draw_the_shapes(shapes_from_file, my_canvas)
    except Exception as e:
        write_to_the_screen(my_canvas,str(e) + "!!!", "red" )



def translation(my_canvas, Tx=0, Ty=0, nkudat_ihus=False ,complex_transformation = False):
    """
    translate the image according the TX / Ty parameters  ,and draw the translate image on the canvas.
            all x in the all point become x+Tx
            all y in the all point become x+Ty
    uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas
    :param Tx: how many to add to x
    :param Ty: how many to add to y
    :param nkudat_ihus : if nkudat_ihus is True - the function doe's not draw thw image , and there is no checking for "out of boarder"
    """
    global shapes_from_file
    try:
        copy_shapes_from_file = deepcopy(shapes_from_file)
        for shape_type in copy_shapes_from_file:
            for shape in copy_shapes_from_file[shape_type]:
                for point_coordinate in shape:
                    if "y" in str(point_coordinate):
                        shape[point_coordinate] = shape[point_coordinate] + Ty
                    elif "x" in str(point_coordinate):
                        shape[point_coordinate] = shape[point_coordinate] + Tx
                    if not nkudat_ihus:
                        # checking if the point is out of border or to small :
                        check_border_overflow(point_coordinate,shape[point_coordinate],"translate")

        shapes_from_file = deepcopy(copy_shapes_from_file)
        if not nkudat_ihus:
            clear(my_canvas)
            draw_the_shapes(shapes_from_file, my_canvas)
    except Exception as e:
        if(complex_transformation):
            raise Exception(str(e))
        else :
            write_to_the_screen(my_canvas,str(e) + "!!!", "red" )


def rotation(my_canvas, angle, nkudat_ihus=False):
    """
    This function is rotating all the points of the shapes of the image
        and draw it on the canvas
    uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas to draw all the shapes on .
    :param angle: angle in radian
    :param nkudat_ihus : if nkudat_ihus is True - the function doe's not draw thw image , and there is no checking for "out of boarder"
    """
    matrixB = np.array([[math.cos(angle), math.sin(angle)], [(-math.sin(angle)), math.cos(angle)]])
    global shapes_from_file
    try:
        copy_shapes_from_file = deepcopy(shapes_from_file)
        for shape_type in copy_shapes_from_file:
            for shape in copy_shapes_from_file[shape_type]:
                shape["x1"], shape["y1"] = np.dot(np.array([shape["x1"], shape["y1"]]), matrixB)
                if shape_type == "Lines" or shape_type == "BezierCurves":
                    shape["x2"], shape["y2"] = np.dot(np.array([shape["x2"], shape["y2"]]), matrixB)
                if shape_type == "BezierCurves":
                    shape["x3"], shape["y3"] = np.dot(np.array([shape["x3"], shape["y3"]]), matrixB)
                    shape["x4"], shape["y4"] = np.dot(np.array([shape["x4"], shape["y4"]]), matrixB)

                if not nkudat_ihus:
                    # checking if the point is out of boarder :
                    for point_coordinate in shape:
                        check_border_overflow(point_coordinate, shape[point_coordinate],"rotate")

        shapes_from_file = deepcopy(copy_shapes_from_file)

        if not nkudat_ihus:
            clear(my_canvas)
            draw_the_shapes(shapes_from_file, my_canvas)
    except Exception as e:
        write_to_the_screen(my_canvas,str(e) + "!!!", "red" )



def rotate_nekudat_ihus(x_ihus, y_ihus, angle, my_canvas):
    """
    Complex transformations that perform sequence of  transformations to ratate the image
    relativly to  point of reference .
    Uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param x_ihus ,y_ihus: point of reference params
    :param angle: angle of rotation in radians
    :param my_canvas: canvas
    """
    global shapes_from_file
    copy_shapes_from_file = deepcopy(shapes_from_file)
    try:
        image_location_params = find_image_location_params()
        Tx = x_ihus - image_location_params["centre"]["x_centre"]
        Ty = y_ihus - image_location_params["centre"]["y_centre"]
        translation(my_canvas, Tx, Ty, True)
        rotation(my_canvas, angle, True)
        translation(my_canvas, (-Tx), (-Ty) ,False,True)
    except Exception as e:
        msg = str(e).replace("translate", "rotate")
        write_to_the_screen(my_canvas,msg + "!!!", "red" )
        print(msg + "5")
        shapes_from_file = deepcopy(copy_shapes_from_file)


def scale_nekudat_ihus(x_ihus, y_ihus, mult_by, my_canvas):
    """
    Complex transformations that perform sequence of  transformations to scale the image
    relativly to  point of reference .
    Uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param x_ihus ,y_ihus: point of reference params
    :param mult: scale by
    :param my_canvas: canvas
    """
    global shapes_from_file
    copy_shapes_from_file = deepcopy(shapes_from_file)
    try:
        image_location_params = find_image_location_params()
        Tx = x_ihus - image_location_params["centre"]["x_centre"]
        Ty = y_ihus - image_location_params["centre"]["y_centre"]
        translation(my_canvas, Tx, Ty, True)
        scale(my_canvas, mult_by, True)
        translation(my_canvas, (-Tx), (-Ty) ,False, True)
    except Exception as e:
        msg = str(e).replace("translate","scale")
        write_to_the_screen(my_canvas,msg + "!!!", "red" )
        print(msg + "6")
        shapes_from_file = deepcopy(copy_shapes_from_file)





def mirror(mirror_type, my_canvas):
    """
    :param mirror_type: type "X" ,"Y" ,"0"
    :param my_canvas: canvas
    :return:
    """
    global shapes_from_file
    try:
        copy_shapes_from_file = deepcopy(shapes_from_file)
        for shape_type in copy_shapes_from_file:
            for shape in copy_shapes_from_file[shape_type]:
                for point_coordinate in shape:
                    if "y" in str(point_coordinate):
                        if mirror_type == "Y" or mirror_type == "0":
                            shape[point_coordinate] = HEIGHT - shape[point_coordinate]
                    elif "x" in str(point_coordinate):
                        if mirror_type == "X" or mirror_type == "0":
                            shape[point_coordinate] = WIDTH - shape[point_coordinate]

                        # checking if the point is out of boarder or to small :
                        check_border_overflow(point_coordinate, shape[point_coordinate], "mirror")
        shapes_from_file = deepcopy(copy_shapes_from_file)
        clear(my_canvas)
        draw_the_shapes(shapes_from_file, my_canvas)
    except Exception as e:
        write_to_the_screen(my_canvas,str(e) + "!!!", "red" )



def point_in_image_border(point_x,point_y):
    """
    Check if the point is in the image boarder
    :param point_x: X of point
    :param point_y: Y of point
    :return: boolian  -if thr point inside return true else false.
    """
    image_location_params = find_image_location_params()
    print("imageparams : ", 'xMin = ',  image_location_params["edges"]["xMin"] ,' xMax = ',image_location_params["edges"]["xMax"] ,\
          " yMin = ",image_location_params["edges"]["yMin"] ," yMax = ", image_location_params["edges"]["yMax"])
    if point_x >= image_location_params["edges"]["xMin"]  and point_x <= image_location_params["edges"]["xMax"]:
        if point_y >= image_location_params["edges"]["yMin"] and point_y <= image_location_params["edges"]["yMax"]:
            return True
    return False

def translate_with_mouse( my_canvas ,my_window):
    """
    Translate the image according the  mouse drag parameters  .
     draw the translate image on the canvas.
    uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas
    :param my_window: window - to bind tho nouse drag on
    """
    global first_point , shapes_from_file
    write_to_the_screen(my_canvas, "To move - Drag the image with the mouse" + "!!!", "black")

    def drag_with_mouse(event ,my_canvas):
        global first_point, first_point_x, first_point_y ,init_position ,shapes_from_file
        if (first_point):
            try:
                first_point_x, first_point_y = event.x, event.y
                if (point_in_image_border(first_point_x, first_point_y)):
                    first_point = False
                    init_position =  deepcopy(shapes_from_file)
            except Exception as e:
                write_to_the_screen(my_canvas,str(e) + "!!!", "red" )


        else:
            x, y = event.x, event.y
            deltaX = x - first_point_x
            deltaY = y - first_point_y
            try:
                # shapes_from_file = getImageParams()
                copy_shapes_from_file = deepcopy(init_position)
                for shape_type in copy_shapes_from_file:
                    for shape in copy_shapes_from_file[shape_type]:
                        for point_coordinate in shape:

                            if "y" in str(point_coordinate):
                                shape[point_coordinate] = shape[point_coordinate] + deltaY
                            if "x" in str(point_coordinate):
                                shape[point_coordinate] = shape[point_coordinate] + deltaX

                            # checking if the point is out of border or to small :
                            check_border_overflow(point_coordinate, shape[point_coordinate], "move")

                shapes_from_file = deepcopy(copy_shapes_from_file)
                clear(my_canvas)
                draw_the_shapes(shapes_from_file, my_canvas)
            except Exception as e:
                write_to_the_screen(my_canvas,str(e) + "!!!", "red" )

    my_window.bind("<B1-Motion>", lambda event: drag_with_mouse(event ,my_canvas))


def mouseButtonReleesed(event):
    global first_point
    print("mouseButtonReleesed = ",event)
    first_point = True

def Shearing(shearing_type, my_canvas ,my_window ,nkudat_ihus=False ) :
    """
    Shearing the image according the shearing_type ("X" or "Y") and mouse drag parameters  .
     draw the translate image on the canvas.
    uses global param  shapes_from_file: dict with array of lines params list , circles params list and bezier curves params list;
    :param my_canvas: canvas
    :param shearing_type: type of shiring "X" or "Y"
    :param my_window: window - to bind tho nouse drag on
    """
    global first_point ,shapes_from_file
    write_to_the_screen(my_canvas, "To shear - Drag the image with the mouse" + "!!!", "black")

    def shear(event,shearing_type,my_canvas):
        print(shearing_type)
        global first_point, first_point_x, first_point_y ,init_position ,shapes_from_file
        if(first_point):
            first_point_x, first_point_y = event.x, event.y
            # print('first_point : {}, {}'.format(first_point_x, first_point_y))
            if(point_in_image_border(first_point_x,first_point_y)):
                first_point = False
                init_position = deepcopy(shapes_from_file)
        else:
            x,y =  event.x, event.y
            print('first_point : {}, {}'.format(first_point_x, first_point_y))
            print('x,y : {}, {}'.format(x, y))
            deltaX =  x - first_point_x
            deltaY =  y - first_point_y
            print("deltaX : {} ,deltaY : {}  ".format(deltaX,deltaY))
            try:

                image_location_params = find_image_location_params(True)

                copy_shapes_from_file = deepcopy(init_position)

                for shape_type in copy_shapes_from_file:
                    for shape in copy_shapes_from_file[shape_type]:

                        if shearing_type == "X":
                            delta_Y  =  image_location_params["edges"]["yMax"] - y
                            a = deltaX/delta_Y
                            shape["x1"] =  shape["x1"]  + a* abs(shape["y1"] -image_location_params["edges"]["yMax"] )
                            if shape_type == "Lines" or shape_type == "BezierCurves":
                                shape["x2"]  = shape["x2"]  + a* abs(shape["y2"] -image_location_params["edges"]["yMax"] )
                            if shape_type == "BezierCurves":
                                shape["x3"] =shape["x3"]  + a* abs(shape["y3"] -image_location_params["edges"]["yMax"] )
                                shape["x4"] = shape["x4"] + a* abs(shape["y4"] -image_location_params["edges"]["yMax"] )

                        elif shearing_type == "Y":
                            Xmax = image_location_params["edges"]["xMax"]
                            delta_X = image_location_params["edges"]["xMax"] - x
                            a = deltaY / delta_X
                            shape["y1"] = shape["y1"] + a * abs(shape["x1"] - Xmax)
                            if shape_type == "Lines" or shape_type == "BezierCurves":
                                shape["y2"] = shape["y2"] + a * abs(shape["x2"] - Xmax)
                            if shape_type == "BezierCurves":
                                shape["y3"] = shape["y3"] + a * abs(shape["x3"] - Xmax)
                                shape["y4"] = shape["y4"] + a * abs(shape["x4"] - Xmax)

                        # checking if the point is out of border or to small :
                        for point_coordinate in shape:
                            check_border_overflow(point_coordinate,shape[point_coordinate],"shear")

                shapes_from_file = deepcopy(copy_shapes_from_file)
                clear(my_canvas)
                draw_the_shapes(shapes_from_file, my_canvas)
            except Exception as e:
                print(e)
                write_to_the_screen(my_canvas, str(e) + "!!!", "black")

    my_window.bind("<B1-Motion>", lambda event: shear(event,shearing_type ,my_canvas))


def reset_canvas(canvas):
    """
    Reopen and redraw the image on canvas
    :param canvas: canvas
    """
    global  shapes_from_file
    clear(canvas)
    shapes_from_file  = getImageParams()
    draw_the_shapes(shapes_from_file, canvas)
    fit_car_to_screen(canvas)


# #print slider value
# def print_slider_value(slider):
#     print (slider.get())

#return slider value
def get_slider_values(slider):
    return slider.get()


def get_mouse_pos_on_click(event):
    return event.x, event.y

def get_angle(num):
    return num * 2 * math.pi / 360.0

def set_all_sliders(all_sliders):
    """
    Set all sliders  to tho midle of the bar .
    :param all_sliders: list with all sliders
    """
    for slider in all_sliders:
        slider_fefault_value = float( ( slider["to"] + slider["from"] ) /2 )
        slider.set(float(slider_fefault_value))

def change_file_name(my_canvas, text_box):
    # car_param = find_image_location_params()
    global fileParams
    file_temp=fileParams
    fileParams = text_box.get(1.0, END+"-1c")
    if fileParams == "":
        return

    fileParams = os.path.join("Params/", fileParams)
    if not os.path.isfile(fileParams):
        fileParams = file_temp
        write_to_the_screen(my_canvas,"invalid file name!!", "red")
    else:
        text_box.delete("1.0", "end")
        reset_canvas(my_canvas)


def fit_car_to_screen(canvas):
    global shapes_from_file
    #find the middel of the screen
    window_mid_x = WIDTH/2
    window_mid_y = HEIGHT/2
    #get current car params
    car_param = find_image_location_params()
    car_center_x = car_param["centre"]["x_centre"]
    car_center_y = car_param["centre"]["y_centre"]
    #move car to the middel
    print(shapes_from_file)
    try:
        translation(canvas,(window_mid_x - car_center_x),False,True)
        translation(canvas,0, (window_mid_y - car_center_y),False,True)
        # get current car params
        car_param = find_image_location_params()
        # get len of the car
        car_len_x = car_param['edges']['xMax'] - car_param['edges']['xMin']
        car_len_y = car_param['edges']['yMax'] - car_param['edges']['yMin']
        ratio_x = math.floor((WIDTH) / car_len_x)
        ratio_y = math.floor((WIDTH) / car_len_y)
        # scale for perfection ;)
        if ratio_y > ratio_x:
            scale_nekudat_ihus(0, 0, math.floor((WIDTH) / car_len_x), canvas)
        else:
            scale_nekudat_ihus(0, 0, math.floor(HEIGHT / car_len_y), canvas)
    except Exception as e:
        write_to_the_screen(my_canvas, "Can't fit the image to the screen " + "!!!", "red")
        shapes_from_file = {'Lines':[],'Circles':[],'BezierCurves':[]}



if __name__ == "__main__":
    # get shapes from file :
    fileName = "car_params.txt"
    fileParams = os.path.join("Params/",fileName)
    shapes_from_file = getImageParams()
    image_location_params = find_image_location_params()

    # Windows and canvas definitions  :
    my_window = Tk()
    my_window.maxsize(WIDTH+300,HEIGHT)
    my_window.minsize(WIDTH +300,HEIGHT)
    my_window.title("Targil 2 - Transformations")
    my_canvas = Canvas(my_window, width=WIDTH, height=HEIGHT, background='white')
    my_canvas.grid(row=0, column=0, columnspan=4)
    fit_car_to_screen(my_canvas)
    draw_the_shapes(shapes_from_file, my_canvas)


    #scale slider
    slider_scale = Scale(my_window, from_=1, to=2, tickinterval=1,resolution =0.1 ,orient=HORIZONTAL,troughcolor='green')
    # slider_scale.set(1.1)
    slider_scale.place(x=1160, y=10)

    #rotate slider
    slider_rotate = Scale(my_window, from_=0, to=45, tickinterval=45,orient=HORIZONTAL,troughcolor='coral')
    # slider_rotate.set(22)
    slider_rotate.place(x=1160, y=80)

    # translate slider
    slider_translate = Scale(my_window, from_=0, to=100, tickinterval=100, orient=HORIZONTAL, troughcolor='yellow')
    slider_translate.set(25)
    slider_translate.place(x=1160, y=180)

    # rotate on point slider
    slider_scale_point = Scale(my_window, from_=1, to=2, tickinterval=1,resolution =0.1, orient=HORIZONTAL, troughcolor='red')
    # slider_scale_point.set(1.1)
    slider_scale_point.place(x=1160, y=290)

    # scale on point slider
    slider_rotate_point = Scale(my_window, from_=0, to=45, tickinterval=45, orient=HORIZONTAL, troughcolor='purple1')
    # slider_rotate_point.set(22.5)
    slider_rotate_point.place(x=1160, y=360)

    all_sliders = [slider_scale,slider_rotate ,slider_translate,slider_scale_point ,slider_rotate_point]
    set_all_sliders(all_sliders)

    #buttons
    button1 = Button(my_window, text="Scale Up", width=20, bg="green", fg="white",
                     command=lambda: scale(my_canvas, get_slider_values(slider_scale)))
    button2 = Button(my_window, text="Scale Down", width=20, bg="green", fg="white",
                     command=lambda: scale(my_canvas, 1/get_slider_values(slider_scale)))
    button3 = Button(my_window, text="ClockWise Rotation", width=20, bg="coral", fg="white",
                     command=lambda: rotation(my_canvas, get_angle(get_slider_values(slider_rotate))))
    button4 = Button(my_window, text="antiClockWise Rotation", width=20, bg="coral", fg="white",
                     command=lambda: rotation(my_canvas, -(get_angle(get_slider_values(slider_rotate)))))
    button5 = Button(my_window, text="Translate Left", width=20, bg="yellow", fg="black",
                     command=lambda: translation(my_canvas, -(get_slider_values(slider_translate))))
    button6 = Button(my_window, text="Translate Up", width=20, bg="yellow", fg="black",
                     command=lambda: translation(my_canvas, 0, -(get_slider_values(slider_translate))))
    button7 = Button(my_window, text="Translate Down", width=20, bg="yellow", fg="black",
                     command=lambda: translation(my_canvas, 0, get_slider_values(slider_translate)))
    button8 = Button(my_window, text="Translate Right", width=20, bg="yellow", fg="black",
                     command=lambda: translation(my_canvas, get_slider_values(slider_translate)))

    button9 = Button(my_window, text="Scale-Up on place", width=20, bg="red", fg="white",
                     command=lambda: scale_nekudat_ihus(0,0, get_slider_values(slider_scale_point), my_canvas))
    button10 = Button(my_window, text="Scale-Down on place", width=20, bg="red", fg="white",
                      command=lambda: scale_nekudat_ihus(0,0, 1/get_slider_values(slider_scale_point), my_canvas))
    button11 = Button(my_window, text="Rotate on place CW", width=20, bg="purple1", fg="white",
                      command=lambda: rotate_nekudat_ihus( 0, 0,get_angle(get_slider_values(slider_rotate_point)), my_canvas))
    button12 = Button(my_window, text="Rotate on place aCW", width=20, bg="purple1", fg="white",
                      command=lambda: rotate_nekudat_ihus( 0, 0, -(get_angle(get_slider_values(slider_rotate_point))), my_canvas))

    button13 = Button(my_window, text="Mirror Y-axis", width=20, bg="thistle3", fg="white", command=lambda: mirror("Y", my_canvas))
    button14 = Button(my_window, text="Mirror X-axis", width=20, bg="thistle3", fg="white",command=lambda: mirror("X", my_canvas))
    button15 = Button(my_window, text="Mirror 0-axis", width=20, bg="thistle3", fg="white",command=lambda: mirror("0", my_canvas))
    button16 = Button(my_window, text="Shearing X-axis", width=20, bg="blue", fg="white",command=lambda: Shearing("X", my_canvas ,my_window))
    button17 = Button(my_window, text="Shearing Y-axis", width=20, bg="blue", fg="white",command=lambda: Shearing("Y", my_canvas ,my_window))
    button18 = Button(my_window, text="Move with mouse", width=20, bg="pink", fg="white",command=lambda: translate_with_mouse( my_canvas ,my_window))
    button_reset = Button(my_window, text="Reset image", width=20, bg="gray", fg="white",command=lambda: reset_canvas(my_canvas))
    button_reset_sliders = Button(my_window, text="Reset sliders", width=20, bg="gray", fg="white",
                          command=lambda: set_all_sliders(all_sliders))

    # textbox
    input_file_name = Text(my_window, height=1, width=16)
    input_file_name.place(x=1160, y=540)
    button_file_name = Button(my_window, text="Change File", width=15, bg="black", fg="white",
                              command=lambda: change_file_name(my_canvas, input_file_name))
    button_file_name.place(x=1170, y=565)


    # button1.grid(row=0, column=3)#
    button1.place(x=1005, y=10)
    button2.place(x=1005, y=45)
    button3.place(x=1005, y=80)
    button4.place(x=1005, y=115)
    button5.place(x=1005, y=150)
    button6.place(x=1005, y=185)
    button7.place(x=1005, y=220)
    button8.place(x=1005, y=255)

    button9.place(x=1005, y=290)
    button10.place(x=1005, y=325)
    button11.place(x=1005, y=360)
    button12.place(x=1005, y=395)

    button13.place(x=1005, y=430)
    button14.place(x=1005, y=465)
    button15.place(x=1005, y=500)
    button16.place(x=1005, y=535)
    button17.place(x=1005, y=570)
    button_reset.place(x=850, y=10)
    button_reset_sliders.place(x=850, y=45)
    button18.place(x=850, y=80)

    # my_window.bind('<Motion>', motion)
    my_window.bind('<ButtonRelease-1>', mouseButtonReleesed)
    # my_window.bind('<Button>', get_mouse_pos_on_click)
    # start running the interface window :
    my_window.mainloop()
