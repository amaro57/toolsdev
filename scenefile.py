from pymel.core.system import Path
import re

class SceneFile(object):

    def __init__(self, path):
        self.folder_path = Path()
        self.descriptor = 'main'
        self.task = None
        self.ver = 1
        self.ext = '.ma'
        self._init_from_path(path)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task, ver=self.ver, ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename
    
    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = re.findall('([^_]+)+', path.name.stripext())
        self.ver = int(ver.split("v")[-1])


scene_file = SceneFile("F:/tank_model_v1.ma")
print(scene_file.path)
