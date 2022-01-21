
from Point3d import Point3D


class Line3D:

    start = None
    end = None
    color = 0  # type: int

    def __init__(self,
                 start_x, start_y, start_z,
                 end_x, end_y, end_z,
                 color=1):
        self.start = Point3D(start_x, start_y, start_z)
        self.end = Point3D(end_x, end_y, end_z)
        self.color = color

