"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QSizePolicy, QGraphicsScene, QPushButton, QGraphicsLineItem

from data.Point3d import Point3D
from data.PreProcOutfileReader import PreProcOutfileReader

from gui.elements.GraphicsView import GraphicsView
from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from Singleton.Singleton import Singleton


class Rib:
    """
    :class: Does collect all data to describe the 3D coordinates of a rib.
    """

    le = None
    te = None

    def __init__(self,
                 le_x, le_y, le_z,
                 te_x, te_y, te_z):
        """
        :method: Constructor
        :param le_x: x-Coordinate of the le-position
        :param le_y: y-Coordinate of the le-position
        :param le_z: z-Coordinate of the le-position
        :param te_x: x-Coordinate of the te-position
        :param te_y: y-Coordinate of the te-position
        :param te_z: z-Coordinate of the te-position
        """

        self.le = Point3D(le_x, le_y, le_z)
        self.te = Point3D(te_x, te_y, te_z)


class PreProcWingOutline(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display the wing outline calculated by the
            PreProcessor.
    """

    __className = 'PreProcWingOutline'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()
        self.view = None
        self.scene = None
        self.proj_params = None
        logging.debug(self.__className + '.__init__')

        self.__open_pre_proc_file = False  # type: bool
        self.button_bar = None
        self.help_bar = None
        self.window_ly = None
        self.window = None

        self.wing = []
        self.edges = []
        self.ini_angle_x = 100
        self.ini_angle_y = 210
        self.ini_angle_z = 0

        self.ini_fov = 1500
        self.ini_distance = 6000

        self.angle_x = self.ini_angle_x
        self.angle_y = self.ini_angle_y
        self.angle_z = self.ini_angle_z

        self.ini_scene_width = 400
        self.ini_scene_height = 200

        self.build_window()

    def build_window(self):
        """
        :method: Creates the window including all GUI elements.

        Structure::

            window
                window_ly

                    ---------------------------
                                help_bar | btn_bar
        """
        logging.debug(self.__className + '.build_window')

        self.setWindowIcon(QIcon('gui/elements/appIcon.ico'))
        self.window = QWidget()
        self.setWidget(self.window)
        self.window.setMinimumSize(900, 400)

        self.window_ly = QVBoxLayout()

        self.help_bar = WindowHelpBar()

        #############################
        # Add window specifics here
        self.setWindowTitle(_("Wing outline"))

        btn_ly = QVBoxLayout()
        btn_ly.addStretch()
        x_min_btn = QPushButton(_("Pitch -"))
        x_min_btn.clicked.connect(self.x_min)
        x_plu_btn = QPushButton(_("Pitch +"))
        x_plu_btn.clicked.connect(self.x_plu)
        x_hbox = QHBoxLayout()
        x_hbox.addWidget(x_min_btn)
        x_hbox.addWidget(x_plu_btn)
        btn_ly.addLayout(x_hbox)

        y_min_btn = QPushButton(_("Yaw BB"))
        y_min_btn.clicked.connect(self.y_min)
        y_plu_btn = QPushButton(_("Yaw StB"))
        y_plu_btn.clicked.connect(self.y_plu)
        y_hbox = QHBoxLayout()
        y_hbox.addWidget(y_min_btn)
        y_hbox.addWidget(y_plu_btn)
        btn_ly.addLayout(y_hbox)

        z_min_btn = QPushButton(_("Roll StB"))
        z_min_btn.clicked.connect(self.z_min)
        z_plu_btn = QPushButton(_("Roll BB"))
        z_plu_btn.clicked.connect(self.z_plu)
        z_hbox = QHBoxLayout()
        z_hbox.addWidget(z_plu_btn)
        z_hbox.addWidget(z_min_btn)
        btn_ly.addLayout(z_hbox)

        top_btn = QPushButton(_("Top"))
        top_btn.clicked.connect(self.top)
        btn_ly.addWidget(top_btn)

        side_stb_btn = QPushButton(_("StB"))
        side_stb_btn.clicked.connect(self.side_stb)
        side_bb_btn = QPushButton(_("BB"))
        side_bb_btn.clicked.connect(self.side_bb)
        side_hbox = QHBoxLayout()
        side_hbox.addWidget(side_bb_btn)
        side_hbox.addWidget(side_stb_btn)
        btn_ly.addLayout(side_hbox)

        rear_btn = QPushButton(_("Rear"))
        rear_btn.clicked.connect(self.rear)
        btn_ly.addWidget(rear_btn)

        zoom_in_btn = QPushButton("Zoom +")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn = QPushButton("Zoom -")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_hbox = QHBoxLayout()
        zoom_hbox.addWidget(zoom_out_btn)
        zoom_hbox.addWidget(zoom_in_btn)
        btn_ly.addLayout(zoom_hbox)

        fit_btn = QPushButton("Fit")
        fit_btn.clicked.connect(self.fit_scene)
        btn_ly.addWidget(fit_btn)

        res_btn = QPushButton("Reset")
        res_btn.clicked.connect(self.reset_scene)
        btn_ly.addWidget(res_btn)

        btn_ly.addStretch()

        self.scene = QGraphicsScene(0, 0,
                                    self.ini_scene_width,
                                    self.ini_scene_height)
        self.view = GraphicsView(self.scene)
        self.view.setDragMode(GraphicsView.ScrollHandDrag)
        self.view.setRenderHint(QPainter.Antialiasing)

        hbox_ly = QHBoxLayout()
        hbox_ly.addLayout(btn_ly)
        hbox_ly.addWidget(self.view)

        self.window_ly.addLayout(hbox_ly)

        pre_proc_file_btn = QPushButton(_("Pre-Proc file"))
        pre_proc_file_btn.clicked.connect(self.open_pre_proc_file)
        own_file_btn = QPushButton(_("Own file"))
        own_file_btn.clicked.connect(self.open_file)

        #############################
        # Commons for all windows
        self.button_bar = WindowBtnBar(0b0101)
        self.button_bar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                  QSizePolicy.Fixed))
        self.button_bar.my_signal.connect(self.button_press)
        self.button_bar.setHelpPage('preproc/wing_outline.html')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(pre_proc_file_btn)
        bottom_layout.addWidget(own_file_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_bar)
        bottom_layout.addWidget(self.button_bar)
        self.window_ly.addLayout(bottom_layout)

        self.window.setLayout(self.window_ly)

    def open_pre_proc_file(self):
        """
        :method: Opens the data file from the pre-proc directory and updates
                 the window
        """
        pre_proc_reader = PreProcOutfileReader()
        data, num_cells = pre_proc_reader.open_read_file(True)

        if len(data) > 0 and num_cells != 0:
            self.prepare_wing_data(data, num_cells)
            self.update_scene()
            self.update_scene()
            self.reset_scene()

    def open_file(self):
        """
        :method: Opens a user specific data file and updates the window
        """
        pre_proc_reader = PreProcOutfileReader()
        data, num_cells = pre_proc_reader.open_read_file(False)

        if len(data) > 0 and num_cells != 0:
            self.prepare_wing_data(data, num_cells)
            # self.update_scene()
            self.reset_scene()

    def prepare_wing_data(self, data, num_cells):
        """
        :method: Builds with the one-sided data read from the data file all
                 edges tho be displayed.
        :param data: Data read from the data file
        :param num_cells: Number of cells read from the data file
        """

        # We will move the turn point of the wing to half wing deep
        delta_y = float(data[0][3]) * 0.5

        # Empty wing list
        del self.wing[:]
        self.scene.clear()

        if int(num_cells) % 2 == 0:
            # num_cells even/ gerade Anzahl
            # we have one rib exactly in the middle

            for rib_it in range(len(data)-1, -1, -1):
                self.wing.append(Rib(float(data[rib_it][1]) * -1,
                                     float(data[rib_it][2]) - delta_y,
                                     float(data[rib_it][5]),
                                     float(data[rib_it][1]) * - 1,
                                     float(data[rib_it][3]) - delta_y,
                                     float(data[rib_it][5])))
            # middle rib has already been written
            for rib_it in range(1, len(data)):
                self.wing.append(Rib(float(data[rib_it][1]),
                                     float(data[rib_it][2]) - delta_y,
                                     float(data[rib_it][5]),
                                     float(data[rib_it][1]),
                                     float(data[rib_it][3]) - delta_y,
                                     float(data[rib_it][5])))

        else:
            # num_cells odd/ ungerade
            for rib_it in range(len(data)-1, -1, -1):
                self.wing.append(Rib(float(data[rib_it][1]) * -1,
                                     float(data[rib_it][2]) - delta_y,
                                     float(data[rib_it][5]),
                                     float(data[rib_it][1]) * - 1,
                                     float(data[rib_it][3]) - delta_y,
                                     float(data[rib_it][5])))
            # middle rib will be written twice
            for rib_it in range(0, len(data)):
                self.wing.append(Rib(float(data[rib_it][1]),
                                     float(data[rib_it][2]) - delta_y,
                                     float(data[rib_it][5]),
                                     float(data[rib_it][1]),
                                     float(data[rib_it][3]) - delta_y,
                                     float(data[rib_it][5])))

        # delete old edges
        for edge_it in range(len(self.edges)-1, -1, -1):
            self.scene.removeItem(self.edges[edge_it][2])
        # empty edge list
        del self.edges[:]

        # create edges
        # lines for the ribs
        for rib_it in range(0, len(self.wing)):

            line_item = QGraphicsLineItem()

            border = divmod(len(self.wing), 2)

            if rib_it < border[0]:
                pen = QPen(Qt.darkGreen)
            elif rib_it >= border[0]+border[1]:
                pen = QPen(Qt.red)
            else:
                pen = QPen(Qt.black)

            pen.setCosmetic(True)
            line_item.setPen(pen)

            edge = (self.wing[rib_it].le,
                    self.wing[rib_it].te,
                    line_item)
            self.edges.append(edge)

        # leading edge
        black_pen = QPen(Qt.black)
        black_pen.setCosmetic(True)

        for rib_it in range(0, len(self.wing)-1):
            line_item = QGraphicsLineItem()
            line_item.setPen(black_pen)

            edge = (self.wing[rib_it].le,
                    self.wing[rib_it+1].le,
                    line_item)
            self.edges.append(edge)

        # trailing edge
        for rib_it in range(0, len(self.wing)-1):
            line_item = QGraphicsLineItem()
            line_item.setPen(black_pen)

            edge = (self.wing[rib_it].te,
                    self.wing[rib_it+1].te,
                    line_item)
            self.edges.append(edge)

        for edge in self.edges:
            self.scene.addItem(edge[2])

    def update_scene(self):
        self.proj_params = [self.angle_x, self.angle_y, self.angle_z,
                            self.view.width(), self.view.height(),
                            self.ini_fov, self.ini_distance]

        for edge in self.edges:
            edge[2].setLine(edge[0].get_x2d(*self.proj_params),
                            edge[0].get_y2d(*self.proj_params),
                            edge[1].get_x2d(*self.proj_params),
                            edge[1].get_y2d(*self.proj_params))

    def x_min(self):
        self.angle_x -= 10
        self.update_scene()

    def x_plu(self):
        self.angle_x += 10
        self.update_scene()

    def y_min(self):
        self.angle_y -= 10
        self.update_scene()

    def y_plu(self):
        self.angle_y += 10
        self.update_scene()

    def z_min(self):
        self.angle_z -= 10
        self.update_scene()

    def z_plu(self):
        self.angle_z += 10
        self.update_scene()

    def top(self):
        self.angle_x = 180
        self.angle_y = 180
        self.angle_z = 0
        self.update_scene()

    def rear(self):
        self.angle_x = 90
        self.angle_y = 180
        self.angle_z = 0
        self.update_scene()

    def side_stb(self):
        self.angle_x = 90
        self.angle_y = 270
        self.angle_z = 0
        self.update_scene()

    def side_bb(self):
        self.angle_x = 90
        self.angle_y = 90
        self.angle_z = 0
        self.update_scene()

    def zoom_in(self):
        self.view.scale(1.1, 1.1)

    def zoom_out(self):
        self.view.scale(.9, .9)

    def min_bounding_rect(self, rect_list):
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

    def reset_scene(self):
        self.angle_x = self.ini_angle_x
        self.angle_y = self.ini_angle_y
        self.angle_z = self.ini_angle_z
        self.update_scene()
        self.fit_scene()

    def fit_scene(self):
        # make sure scene covers all items
        items = self.scene.items()
        rects = [item.mapToScene(item.boundingRect()).boundingRect() for item in items]
        rect = self.min_bounding_rect(rects)
        self.scene.setSceneRect(rect)

        # fit view to scene
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def button_press(self, q):
        """
        :method: Handling of all pressed buttons.
        """
        logging.debug(self.__className+'.btn_press')
        if q == 'Apply':
            pass

        elif q == 'Ok':
            self.close()

        elif q == 'Cancel':
            self.close()
        else:
            logging.error(self.__className
                          + '.btn_press unrecognized button press '
                          + q)

    def closeEvent(self, event):
        """
        :method: Called at the time the user closes the window.
        """
        logging.debug(self.__className+'.closeEvent')
