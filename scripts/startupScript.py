from PythonQt.QtCore import QTimer, QEvent
from PythonQt.QtGui import QGuiApplication
from PythonQt.private import QObject


class DialogCloser(QObject):
    def eventFilter(self, obj, event):
        if (
            event.type() == QEvent.Show
            and obj.isVisible()
            and obj.className() in ("DlgInitialize", "DlgRegister")
        ):
            QTimer.singleShot(
                100, lambda: obj.reject()
            ) 
            return True
        return False


qapp = QGuiApplication.instance()

dialog_closer = DialogCloser()
qapp.installEventFilter(dialog_closer)
