from PyQt5.QtWidgets import QSizePolicy
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MyVTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super(MyVTKWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCameraClippingRange()
        self.GetRenderWindow().Render()

    def resizeEvent(self, event):
        # Call the base class resizeEvent to allow normal Qt resizing behavior
        super(MyVTKWidget, self).resizeEvent(event)
        
        # Update the VTK view with the new viewport size
        self.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCameraClippingRange()
        self.GetRenderWindow().Render()