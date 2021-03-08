import logging

import pymel.core as pmc
from pymel.core.system import Path
import re

log = logging.getLogger(__name__)

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
        
    def save(self):
        """Saves the scene file.
        
        Returns:
            Path: The path to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except:
            log.warning("Missing directory in specified path. Creating directory")
            self.folder_path.mkdir_p()
            return pmc.system.saveAs(self.path)
