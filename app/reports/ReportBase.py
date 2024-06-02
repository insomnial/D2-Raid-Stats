from app.LocalController import LocalController
import abc

from app.ManifestController import DestinyManifest


class Report:

    def __init__(self, membershipType, membershipId, displayName, manifest: DestinyManifest) -> None:
        super().__init__()
        self.membershipType = membershipType
        self.membershipId = membershipId
        self.displayName = displayName
        self.manifest = manifest
        self.fig = None

    @abc.abstractmethod
    def generate(self, data):
        pass

    @abc.abstractmethod
    def getName(self) -> str:
        return "unnamed"

    def save(self):
        print("Report> Saving %s" % self.getName())
        assert self.fig is not None
        filename = '%s/%s.html' % (LocalController.GetResultDirectory(self.displayName), self.getName())
        with open(filename, "w") as f:
            f.write(self.fig.to_html(full_html=False, include_plotlyjs='cdn'))
