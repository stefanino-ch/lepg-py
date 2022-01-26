"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import logging
import os

from PyQt5.QtCore import Qt, QRectF

from PyQt5.QtGui import QIcon, QPainter, QPen, QColor
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QSizePolicy, QGraphicsScene, QPushButton, QGraphicsView, QGraphicsLineItem, QMessageBox, QFileDialog

from ConfigReader.ConfigReader import ConfigReader
from data.DxfReader import DxfReader

from gui.elements.WindowHelpBar import WindowHelpBar
from gui.elements.WindowBtnBar import WindowBtnBar
from Singleton.Singleton import Singleton

# TODO: Mouse wheel zoom
# https://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel


class PreProcWingOutlineDxf(QMdiSubWindow, metaclass=Singleton):
    """
    :class: Window to display the wing outline calculated by the
            PreProcessor.
    """
    __className = 'PreProcWingOutlineDxf'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :method: Constructor
        """
        super().__init__()
        self.__file_path_name = None
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
        self.ini_angle_x = 0
        self.ini_angle_y = 0
        self.ini_angle_z = 0

        self.ini_fov = 1500
        self.ini_distance = 6000

        self.angle_x = self.ini_angle_x
        self.angle_y = self.ini_angle_y
        self.angle_z = self.ini_angle_z

        self.ini_scene_width = 200
        self.ini_scene_height = 200

        self.config_reader = ConfigReader()

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
        self.setWindowTitle(_("Wing outline DXF"))

        btn_ly = QVBoxLayout()

        zoom_in_btn = QPushButton("Zoom +")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn = QPushButton("Zoom -")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_hbox = QHBoxLayout()
        zoom_hbox.addWidget(zoom_out_btn)
        zoom_hbox.addWidget(zoom_in_btn)
        btn_ly.addLayout(zoom_hbox)

        res_btn = QPushButton("Fit")
        res_btn.clicked.connect(self.fit_scene)
        btn_ly.addWidget(res_btn)

        self.scene = QGraphicsScene(0, 0,
                                    self.ini_scene_width,
                                    self.ini_scene_height)
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
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
        dxf_data = self.open_read_file(True)
        if dxf_data:
            self.prepare_data(dxf_data)
            self.update_scene()
            self.fit_scene()

    def open_file(self):
        """
        :method: Opens a user specific data file and updates the window
        """
        dxf_data = self.open_read_file()
        if dxf_data:
            self.prepare_data(dxf_data)
            self.update_scene()
            self.fit_scene()

    def open_read_file(self, read_from_pre_proc_dir=False):
        """
        :method: File Open dialog handling.
                 Checks if the file header specifies a valid file
        :param read_from_pre_proc_dir: Set this to True if the file in the
                 configured pre-proc dir shall be read.

        :returns: Data read from the file
                  None if file could not be read
        """
        logging.debug(self.__className + '.open_read_file')

        if read_from_pre_proc_dir is True:
            self.__file_path_name = \
                os.path.join(self.config_reader.get_pre_proc_directory(),
                             'geometry.dxf')
            if not os.path.isfile(self.__file_path_name):
                msg_box = QMessageBox()
                msg_box.setWindowTitle(_('Ups!'))
                msg_box.setText(_('Either the file does not exist,\n'
                                  'or the pre-processor location\n'
                                  'is not setup.\n'
                                  '(Setup->Both Processors)'))
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
                return None
        else:
            file_name = QFileDialog.getOpenFileName(
                            None,
                            _('Open Pre-proc dxf file'),
                            "",
                            "Pre-Proc Files (*.dxf);;All Files (*)")

            if file_name != ('', ''):
                # User has really selected a file, if it had aborted
                # the dialog an empty tuple is returned
                self.__file_path_name = file_name[0]

        if self.__file_path_name != '':
            dxf_reader = DxfReader()
            if dxf_reader.open_doc(self.__file_path_name):
                return dxf_reader.read_layers_entities()
            else:
                return None

    def prepare_data(self, dxf_data):
        """
        :method: Builds with the dxf data all edges tho be displayed
        :param dxf_data: Data read from the dxf file
        """
        # Data structure of dxf_data
        # Dict key = layer
        #      values = list with all entities found in layer

        # In the pre-proc dxf the only layer is 'default'

        # empty edge list
        del self.edges[:]

        # create edges
        entities = dxf_data.get('default')

        # lines for the ribs
        for entity in entities:
            line_item = QGraphicsLineItem()

            pen = QPen(QColor(entity.color.r, entity.color.g, entity.color.b))
            line_item.setPen(pen)

            edge = (entity,
                    line_item)
            self.edges.append(edge)

        # add all edges to the scene
        for edge in self.edges:
            self.scene.addItem(edge[1])

    def update_scene(self):
        self.proj_params = [self.angle_x, self.angle_y, self.angle_z,
                            self.scene.width(), self.scene.height(),
                            self.ini_fov, self.ini_distance]
        max_x = 0
        max_y = 0

        for edge in self.edges:

            max_x = max(max_x,
                        edge[0].start.get_x2d(*self.proj_params),
                        edge[0].end.get_x2d(*self.proj_params))
            max_y = max(max_y,
                        edge[0].start.get_y2d(*self.proj_params),
                        edge[0].end.get_y2d(*self.proj_params))

            edge[1].setLine(edge[0].start.get_x2d(*self.proj_params),
                            edge[0].start.get_y2d(*self.proj_params),
                            edge[0].end.get_x2d(*self.proj_params),
                            edge[0].end.get_y2d(*self.proj_params))

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

    # TODO: check if same trick works also in WingOutlineViewer
    def fit_scene(self):
        self.angle_x = self.ini_angle_x
        self.angle_y = self.ini_angle_y
        self.angle_z = self.ini_angle_z
        self.update_scene()

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
