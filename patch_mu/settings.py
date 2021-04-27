#replace in C:\Users\benoit\AppData\Local\Programs\Mu Editor\Python\Lib\site-packages\mu
#run "C:\Users\benoit\AppData\Local\Programs\Mu Editor\Python\python.exe" -m mu

from tkinter import filedialog
from tkinter import *
class UserSettings(SettingsBase):

    
    autosave = False
    filestem = "settings"
    
    def __init__(self, **kwargs):
        SettingsBase.__init__(self, **kwargs)
        root = Tk()
        root.withdraw()
        self.DEFAULTS["workspace"] = filedialog.askdirectory(initialdir=os.path.join(config.HOME_DIRECTORY, config.WORKSPACE_NAME))
        print (self.DEFAULTS["workspace"])