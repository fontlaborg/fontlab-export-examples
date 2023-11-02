from PythonQt.QtCore import QTimer, QEvent, qDebug
from PythonQt.QtGui import QGuiApplication
from PythonQt.private import QObject
from fontlab import flWorkspace, ExportControl, flPreferences, flItems

def pprint(msg):
    qDebug(str(msg))

class DialogCloser(QObject):
    def eventFilter(self, obj, event):
        if (
            event.type() == QEvent.Show
            and obj.isVisible()
            and obj.className() in ("DlgInitialize", "DlgRegister")
        ):
            QTimer.singleShot(
                300, lambda: obj.reject()
            ) 
            pprint(f">> Closing {obj.className()}")
            return True
        return False


qapp = QGuiApplication.instance()

dialog_closer = DialogCloser()
qapp.installEventFilter(dialog_closer)
pprint(f">> FontLab run event filter installed")
