import shutil
from pathlib import Path


class LocalController:


    @staticmethod
    def ClearResultDirectory(displayName):
        path = LocalController.GetResultDirectory(displayName)
        shutil.rmtree(path)


    @staticmethod
    def GetZipPath(displayName):
        return f"./data/{displayName}/charts_{displayName}.zip"


    @staticmethod
    def GetResultDirectory(displayName):
        return f"./data/{displayName}/result/"


    @staticmethod
    def GetPGCRDirectory(displayName):
        return f"./data/{displayName}/pgcr/"


    @staticmethod
    def GetAllPgcrFilename(displayName):
        return f"./data/{displayName}/pgcr.json"
    
    
    @staticmethod
    def CreateDirectoriesForUser(displayName):
        Path(LocalController.GetResultDirectory(displayName)).mkdir(parents=True, exist_ok=True)
        Path(LocalController.GetPGCRDirectory(displayName)).mkdir(parents=True, exist_ok=True)
