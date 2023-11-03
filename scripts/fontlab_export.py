from pathlib import Path

from fontlab import ExportControl, flItems, flPreferences, flWorkspace
from PythonQt.QtCore import QTimer, qDebug
from PythonQt.QtGui import QAction, QGuiApplication


def pprint(msg):
    qDebug(str(msg))


class FontLabFontExport:
    def __init__(self):
        self.qApp = QGuiApplication.instance()
        #self.script_folder = Path(__file__).resolve().parent
        self.args = self.qApp.arguments()
        self.fl_workspace = flWorkspace.instance()
        self.fl_main = self.fl_workspace.mainWindow
        self.fl_items = flItems.instance()

    def runQAction(self, code):
        for action in self.fl_main.findChildren(QAction):
            if code in action.statusTip:
                action.trigger()

    def openFont(self, input_path):
        self.input_path = Path(input_path).resolve()
        self.font_base_name = self.input_path.stem
        #self.fl_items.notifyWorkspaceInitialized(self.fl_workspace)
        #self.fl_items.init()
        self.fl_main.loadFont(str(self.input_path))
        self.fl_package = self.fl_workspace.currentPackage
        self.fl_workspace.addPackage(self.fl_package)
        pprint(f">> Opened: {self.input_path}")

    def setBoolPref(self, pref_key, val):
        fl_prefs = flPreferences()
        fl_prefd = fl_prefs.save()
        pref_val = fl_prefd[pref_key]
        if isinstance(pref_val, str):
            fl_prefd[pref_key] = "true" if val else "false"
        else:
            fl_prefd[pref_key] = val
        fl_prefs.load(fl_prefd)

    def exportFont(self, output_folder, profile_name="OpenType TT"):
        fl_prefs = flPreferences()
        self.setBoolPref("export.show_confirmation", False)
        self.setBoolPref("general.welcome", False)
        self.output_folder = Path(output_folder).resolve()
        if not self.output_folder.is_dir():
            self.output_folder.mkdir(parents=True)
        fl_export = ExportControl()
        fl_export.profileName = profile_name
        fl_export.destinationMode = fl_prefs.DestinationFolder
        fl_export.conflictMode = fl_prefs.ConflictOverwrite
        fl_export.contentMode = fl_prefs.ContentMasters
        fl_export.destinationFolder = str(self.output_folder)
        fl_export.groupProfiles = False
        fl_export.groupFamily = False

        self.fl_workspace.exportFont(self.fl_package, fl_export)
        pprint(f">> Exported: {self.output_folder}")

    def closeAll(self):
        packages = list(self.fl_workspace.packages())
        pprint(f">> Closing {len(packages)} fonts")
        for packobj in packages:
            self.fl_workspace.currentPackage.close(False)

    def convert(self, input_path, output_folder, profile_name="OpenType TT"):
        pprint(f">> Converting {input_path} to {output_folder} as {profile_name}")
        self.openFont(input_path)
        self.exportFont(output_folder, profile_name)

    def quit(self):
        pprint(f">> Quitting FontLab")
        self.runQAction("mainwindow.actionExit")

    def finish(self):
        QTimer.singleShot(100, self.closeAll)
        self.qApp.processEvents()
        QTimer.singleShot(100, self.quit)
        

def convert(input_path, output_folder, profile_name="OpenType TT"):
    fl_font_export = FontLabFontExport()
    fl_font_export.convert(input_path, output_folder, profile_name)
    fl_font_export.finish()

if __name__ == "__main__":
    fl_main()
