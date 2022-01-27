"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
# Based on this:
# https://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-
# out-under-mouse-position-using-mouse-wheel

from PyQt5.QtWidgets import QGraphicsView


class GraphicsView(QGraphicsView):
    """
    :class: Subclass of QGraphicsView. Enables mouse wheel zoom.

    A more detailed description of the basics can be found here:
    https://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-
    out-under-mouse-position-using-mouse-wheel
    """
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

    def wheelEvent(self, event):
        """
        :method: Here in all the zoom magic happens
        """
        # Zoom Factor
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        old_pos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

        # Get the new position
        new_pos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
