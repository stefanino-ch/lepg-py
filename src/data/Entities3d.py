"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import math
from PyQt6.QtCore import QRectF

def min_bounding_rect(rect_list):
    """
    :function: calculates the 2d bounding rect needed to display all items
    :param rect_list: a list of all items for which the bounding rect must be
                      calculated
    """
    if not rect_list:
        return None

    min_x = rect_list[0].left()
    min_y = rect_list[0].top()
    max_x = rect_list[0].right()
    max_y = rect_list[0].bottom()

    for k in range(1, len(rect_list)):
        min_x = min(min_x, rect_list[k].left())
        min_y = min(min_y, rect_list[k].top())
        max_x = max(max_x, rect_list[k].right())
        max_y = max(max_y, rect_list[k].bottom())

    return QRectF(min_x,
                  min_y,
                  max_x - min_x,
                  max_y - min_y)


class Color:
    """
    :class: Represents a color in r, g, b
    """
    r = 0
    g = 0
    b = 0

    def __init__(self,
                 r: int = 0,
                 g: int = 0,
                 b: int = 0):
        """
        :method: Class initialization
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        self.set_color(r, g, b)

    def set_color(self, r, g, b):
        """
        :method: Set the color values. If white (255, 255, 255) black will be
                 used, as all drawing backgrounds are white
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        if r == 255 and g == 255 and b == 255:
            self.r = 0
            self.g = 0
            self.b = 0
        else:
            self.r = r
            self.g = g
            self.b = b


class Point3D:
    """
    :class: Holds the coordinates of a point in 3D space. Provides all
            methods for the transformation of the point in space and the
            projection on a 2D surface.

            Two ways of working are possible:
            1. Create the point. Make sure it gets informed about every
            transformation, use .x3d, .y3d, .z3d, .x2d, y2d to find the
            position

            2. Create the point. Use x2d(), y2d() to find the 2d coordinates
            for the given parameters.

            ATTENTION: if you call x2d() and y2d() also .x3d, .y3d, .z3d, .x2d,
                       y2d will be updated.

    """
    curr_x_ang = 0  # type: int
    curr_y_ang = 0  # type: int
    curr_z_ang = 0  # type: int
    curr_view_width = 0  # type: int
    curr_view_height = 0  # type: int
    curr_fov = 0  # type: int
    curr_view_dist = 0  # type: int

    rotPoint = None
    projPoint = None

    x3d = 0  # type: float
    y3d = 0  # type: float
    z3d = 0  # type: float

    x2d = 0  # type: float
    y2d = 0  # type: float

    def __init__(self,
                 x3d: float = 0.0,
                 y3d: float = 0.0,
                 z3d: float = 0.0):
        """
        :method: Creates a new point 3D object with the given coordinates
        :param x3d: x coordinate of the point
        :param y3d: x coordinate of the point
        :param z3d: x coordinate of the point
        """
        # Remember original coordinates of the Point
        self.x3d, self.y3d, self.z3d = x3d, y3d, z3d

    def rotate_x(self, angle):
        """
        :method: Rotates this point around the X axis the given number
                 of degrees
        :param angle: The current rotation angle
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y3d = self.y3d * cosa - self.z3d * sina
        z3d = self.y3d * sina + self.z3d * cosa
        return Point3D(self.x3d, y3d, z3d)

    def rotate_y(self, angle):
        """
        :method: Rotates this point around the Y axis the given number
                 of degrees
        :param angle: The current rotation angle
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z3d = self.z3d * cosa - self.x3d * sina
        x3d = self.z3d * sina + self.x3d * cosa
        return Point3D(x3d, self.y3d, z3d)

    def rotate_z(self, angle):
        """
        :method: Rotates this point around the Z axis the given number
                 of degrees
        :param angle: The current rotation angle
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x3d = self.x3d * cosa - self.y3d * sina
        y3d = self.x3d * sina + self.y3d * cosa
        return Point3D(x3d, y3d, self.z3d)

    def project(self, win_width, win_height, fov, viewer_distance):
        """
        :method: Transforms this 3D point to 2D using a perspective projection
        :returns: New Point 3D Object fitted into the given parameters
        """
        factor = fov / (viewer_distance + self.z3d)
        x3d = self.x3d * factor + win_width / 2
        y3d = -self.y3d * factor + win_height / 2

        return Point3D(x3d, y3d, self.z3d)

    def transform(self, x_ang, y_ang, z_ang,
                  view_width, view_height, fov, view_dist):
        """
        :method: Checks what angles have been changed and calculates the new
                 2D coordinates where needed
        :param x_ang: x angle in 0..360 degrees
        :param y_ang: y angle in 0..360 degrees
        :param z_ang: z angle in 0..360 degrees
        :param view_width: Width of the view displaying the data
        :param view_height: Height of the view displaying the data
        :param fov: Field of view
        :param view_dist: Viewer distance
        """

        if ((x_ang != self.curr_x_ang)
                or (y_ang != self.curr_y_ang)
                or (z_ang != self.curr_z_ang)
                or (view_width != self.curr_view_width)
                or (view_height != self.curr_view_height)
                or (fov != self.curr_fov)
                or (view_dist != self.curr_view_dist)):
            self.rotPoint = self.rotate_x(x_ang) \
                .rotate_y(y_ang) \
                .rotate_z(z_ang)
            self.curr_x_ang = x_ang
            self.curr_y_ang = y_ang
            self.curr_z_ang = z_ang

            self.projPoint = self.rotPoint.project(view_width,
                                                   view_height,
                                                   fov,
                                                   view_dist)
            self.curr_view_width = view_width
            self.curr_view_height = view_height
            self.curr_fov = fov
            self.curr_view_dist = view_dist

            self.x2d = self.projPoint.x3d
            self.y2d = self.projPoint.y3d

    def get_x2d(self, x_ang, y_ang, z_ang,
                view_width, view_height, fov, view_dist):
        """
        :method: Checks what angles have been changed and calculates the new
                 2D coordinates where needed
        :param x_ang: x angle in 0..360 degrees
        :param y_ang: y angle in 0..360 degrees
        :param z_ang: z angle in 0..360 degrees
        :param view_width: Width of the view displaying the data
        :param view_height: Height of the view displaying the data
        :param fov: Field of view
        :param view_dist: Viewer distance
        :returns: x value of the point in the 2D projection
        """
        self.transform(x_ang, y_ang, z_ang,
                       view_width, view_height, fov, view_dist)
        return self.x2d

    def get_y2d(self, x_ang, y_ang, z_ang,
                view_width, view_height, fov, view_dist):
        """
        :method: Checks what angles have been changed and calculates the new
                 2D coordinates where needed
        :param x_ang: x angle in 0..360 degrees
        :param y_ang: y angle in 0..360 degrees
        :param z_ang: z angle in 0..360 degrees
        :param view_width: Width of the view displaying the data
        :param view_height: Height of the view displaying the data
        :param fov: Field of view
        :param view_dist: Viewer distance
        :returns: y value of the point in the 2D projection
        """
        self.transform(x_ang, y_ang, z_ang,
                       view_width, view_height, fov, view_dist)
        return self.y2d


class Line3D:
    """
    :class: Represents a line in 3D space
    """
    start = None
    end = None
    color = None

    def __init__(self,
                 start_x, start_y, start_z,
                 end_x, end_y, end_z,
                 r=0, g=0, b=0):
        """
        :method: Creates a new line object
        :param start_x: x coordinate of start point
        :param start_y: y coordinate of start point
        :param start_z: z coordinate of start point
        :param end_x: x coordinate of end point
        :param end_y: y coordinate of end point
        :param end_z: z coordinate of end point
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        self.start = Point3D(start_x, start_y, start_z)
        self.end = Point3D(end_x, end_y, end_z)
        self.color = Color(r, g, b)


class Text3D:
    """
    :class: Represents a text in 3D space
    """
    position = None
    text = None
    height = None
    color = None
    rotation = None

    def __init__(self,
                 x, y, z,
                 text,
                 height,
                 r, g, b,
                 rotation):
        """
        :method: Creates a new text object
        :param x: x coordinate of text
        :param y: y coordinate of text
        :param z: z coordinate of text
        :param text: the text as string
        :height: text height
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        :param rotation: Rotation angle of the text
        """
        self.position = Point3D(x, y, z)
        self.text = text
        self.height = height
        self.color = Color(r, g, b)
        self.rotation = rotation

    def set_color(self, r, g, b):
        """
        :method: Set the color values. If white (255, 255, 255) black will be
                 used, as all drawing backgrounds are white
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        self.color.set_color(r, g, b)


class Circle3D:
    """
    :class: Represents a circle in 3D space
    """
    center = None
    radius = None

    cornerOne = None
    cornerTwo = None
    color = None

    def __init__(self,
                 center_x, center_y, center_z,
                 radius,
                 r=0, g=0, b=0):
        """
        :method: Creates a new circle object
        :param center_x: x coordinate of the center
        :param center_y: y coordinate of the center
        :param center_z: z coordinate of the center
        :param radius: circle radius
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        self.center = Point3D(center_x, center_y, center_z)
        self.radius = radius
        self.cornerOne = Point3D(center_x - radius,
                                 center_y - radius,
                                 0)
        self.cornerTwo = Point3D(center_x + radius,
                                 center_y + radius,
                                 0)
        self.color = Color(r, g, b)

    def set_color(self, r, g, b):
        """
        :method: Set the color values. If white (255, 255, 255) black will be
                 used, as all drawing backgrounds are white
        :param r: red part of the color
        :param g: green part of the color
        :param b: blue part of the color
        """
        self.color.set_color(r, g, b)

    def get_width(self, x_ang, y_ang, z_ang,
                  view_width, view_height, fov, view_dist):
        """
        :method: As all object will be scaled in the view, we cannot use the
                 radius given in the dxf file for drawing. Instead, we calculate
                 the width of the circle with the help of the two opposite
                 corners of the bounding rect.
        :returns: width of the bounding rect
        """
        return self.cornerOne.get_x2d(
                    x_ang, y_ang, z_ang,
                    view_width, view_height, fov, view_dist) \
            - self.cornerTwo.get_x2d(
                    x_ang, y_ang, z_ang,
                    view_width, view_height, fov, view_dist)

    def get_height(self, x_ang, y_ang, z_ang,
                   view_width, view_height, fov, view_dist):
        """
        :method: As all object will be scaled in the view, we cannot use the
                 radius given in the dxf file for drawing. Instead, we calculate
                 the height of the circle with the help of the two opposite
                 corners of the bounding rect.
        :returns: height of the bounding rect
        """
        return self.cornerOne.get_y2d(
                x_ang, y_ang, z_ang,
                view_width, view_height, fov, view_dist) \
            - self.cornerTwo.get_y2d(
                x_ang, y_ang, z_ang,
                view_width, view_height, fov, view_dist)
