import logging

import pymel.core as pmc
from pymel.core.system import Path
import re

log = logging.getLogger(__name__)


class SceneFile(object):

    def __init__(self, path=None):
        self.folder_path = Path()
        self.descriptor = 'main'
        self.task = None
        self.ver = 1
        self.ext = '.ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.warning("Unable to initialize SceneFile object from"
                        "a new scene. Please specify a path.")
            return
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
        self.descriptor, self.task, ver = re.findall(
            '([^_]+)+', path.name.stripext())
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except:
            log.warning(
                "Missing directory in specified path. Creating directory")
            self.folder_path.mkdir_p()
            return pmc.system.saveAs(self.path)

    def next_avail_ver(self):
        """Returns the next available version number in a folder."""
        # pattern = f"{descriptor}_{task}_v*{ext}"  R.I.P. Maya Python still on Python 2
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        # How do I get auto complete here? Is it because latest_scene is dynamic?
        latest_scenefile = latest_scenefile.name.stripext()
        latest_ver_num = int(latest_scenefile.split("_v")[-1])
        return latest_ver_num + 1

    def increment_save(self):
        """Increments the version and saves the scene

        If the exisiting version of a file already exists, it should increment
        from the largest version number available in the folder.

        Returns:
            Path: The path to the scene file if successful
        """
        self.ver = self.next_avail_ver()
        self.save()
