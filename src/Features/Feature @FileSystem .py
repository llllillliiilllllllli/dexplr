from typing import List
import os 

class LocalRepository:

    def GetEntryPaths() -> None:
        i_fol = input("Enter input folder: ").replace("\"", "").strip()

        with os.scandir(i_fol) as entries:
            for entry in entries:
                print(entry.path)


    def GetFilePaths() -> None:
        i_fol = input("Enter input folder: ").replace("\"", "").strip()

        fils = []
        with os.scandir(i_fol) as entries:
            for entry in entries:
                if entry.is_file():
                    fils.append(entry.path)

        for fil in fils: print(fil)

    def GetFolderPaths() -> None:
        i_fol = input("Enter input folder: ").replace("\"", "").strip()

        fols = []
        with os.scandir(i_fol) as entries:
            for entry in entries:
                if entry.is_dir():
                    fols.append(entry.path)

        for fol in fols: print(fol)


    def ExportEntryPaths() -> None:
        pass 

    def ExportFilePaths() -> None: 
        pass 

    def ExportFolderPaths() -> None: 
        pass 