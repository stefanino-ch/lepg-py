"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import math


class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self,
                 r: int = 0,
                 g: int = 0,
                 b: int = 0):
        self.set_color(r, g, b)

    def set_color(self, r, g, b):
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
        :constructor: Creates a new point 3D object with the given coordinates
        :param x3d: x coordinate of the point
        :param y3d: x coordinate of the point
        :param z3d: x coordinate of the point
        """
        # Remember original coordinates of the Point
        self.x3d, self.y3d, self.z3d = x3d, y3d, z3d

    def rotate_x(self, angle):
        """
        Rotates this point around the X axis the given number of degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y3d = self.y3d * cosa - self.z3d * sina
        z3d = self.y3d * sina + self.z3d * cosa
        return Point3D(self.x3d, y3d, z3d)

    def rotate_y(self, angle):
        """
        Rotates this point around the Y axis the given number of degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z3d = self.z3d * cosa - self.x3d * sina
        x3d = self.z3d * sina + self.x3d * cosa
        return Point3D(x3d, self.y3d, z3d)

    def rotate_z(self, angle):
        """
        Rotates this point around the Z axis the given number of degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x3d = self.x3d * cosa - self.y3d * sina
        y3d = self.x3d * sina + self.y3d * cosa
        return Point3D(x3d, y3d, self.z3d)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
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
    start = None
    end = None
    color = None

    def __init__(self,
                 start_x, start_y, start_z,
                 end_x, end_y, end_z,
                 r=0, g=0, b=0):
        self.start = Point3D(start_x, start_y, start_z)
        self.end = Point3D(end_x, end_y, end_z)
        self.color = Color(r, g, b)


class Text3D:
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
        self.position = Point3D(x, y, z)
        self.text = text
        self.height = height
        self.color = Color(r, g, b)
        self.rotation = rotation

    def set_color(self, r, g, b):
        self.color.set_color(r, g, b)


class Circle3D:
    center = None
    radius = None
    color = None

    def __init__(self,
                 start_x, start_y, start_z,
                 end_x, end_y, end_z,
                 r=0, g=0, b=0):
        self.start = Point3D(start_x, start_y, start_z)
        self.end = Point3D(end_x, end_y, end_z)
        self.color = Color(r, g, b)

    def set_color(self, r, g, b):
        self.color.set_color(r, g, b)
