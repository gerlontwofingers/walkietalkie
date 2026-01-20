import os
from pathlib import Path
import datetime
import shutil
import subprocess
from PIL import Image
from datetime import date, datetime
# import datetime
import exifread
from dataclasses import dataclass

from config import Seasonator

class Seasons:
    def __init__(self) -> None:
        self._seasonator = Seasonator()

    def get_season(self, now) -> str:
        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=self._seasonator.leap_year)
        return next(season for season, (start, end) in self._seasonator.seasons
                    if start <= now <= end)

class MetaExtractor:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.extension = self.path.suffix.lower()
        self.default_date = datetime.strptime("1000:01:01 00:00:00", "%Y:%m:%d %H:%M:%S")
        # print(self.extension)
        self.file_name = self.path.name
        self.creation_date = self._get_creation_date()
        # print(self.creation_date)
        # print(type(self.creation_date))
        self.creation_yyyymmdd = self.creation_date.strftime(format="%Y%m%d")
        self.creation_year = self.creation_date.strftime(format="%Y")
        self.creation_season = self._get_season()
    
    def _get_season(self):
        seasons = Seasons()
        return seasons.get_season(now=self.creation_date)

    def _img_extract_via_pil(self):
        print('Attempting to extract metadata using PIL...')
        if exif := Image.open(self.path)._getexif():
            print('Looking for date in EXIF...')
            if 36867 in exif.keys():
                print('...found!')
                return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')
            else:
                print('...failed. Defaulting to default date.')
                return self.default_date
            # return self.default_date
            # return exif[36867]
        else:
            Exception('Method pil: Image {0} does not have EXIF data.'.format(self.path))
            print('...failed. Defaulting to default date.')
            return self.default_date
    
    def _img_extract_via_exifread(self):
        with open(self.path, "rb") as file_handle:
            tags = exifread.process_file(file_handle)
        # print(tags)
        return datetime.strptime(tags["EXIF DateTimeOriginal"].values, "%Y:%m:%d %H:%M:%S")

    def _vid_extract_via_exifread(self):
        print("Attempting to extract video metadata...")
        EXIFTOOL_DATE_TAG_VIDEOS = "Create Date"
        EXIF_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        EXIF_DATE_FORMATS = [
            "%Y-%m-%d %H:%M:%S",
            "%Y:%m:%d %H:%M:%S",
        ]
        # absolute_path = os.path.join( os.getcwd(), path )
        absolute_path = self.path

        process = subprocess.Popen(["exiftool", absolute_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        lines = out.decode("utf-8").split("\n")
        creation_dates = []
        creation_date = None
        for l in lines:
            if EXIFTOOL_DATE_TAG_VIDEOS in str(l):
                datetime_str = str(l.split(" : ")[1].strip())
                for date_format in EXIF_DATE_FORMATS:
                    try:
                        print(f'Reading vido metadata. Attempting to parse using format {date_format}...')
                        creation_date = datetime.strptime(datetime_str, date_format)
                        creation_dates += [creation_date]
                        print(f"parsed: {creation_date}")
                        print('...success!')
                    except Exception:
                        print(f"Date format {date_format} was rejected. Trying new format.")
        if not creation_date:
            raise ValueError('Could not resolve date.')
        else:
            return min(creation_dates)
    def _extract_via_file_properties(self):
        dates = [
            datetime.datetime.fromtimestamp(self.path.stat().st_mtime, tz=datetime.timezone.utc),
            datetime.datetime.fromtimestamp(self.path.stat().ct_mtime, tz=datetime.timezone.utc),
        ]
        return min(dates)

    def _get_creation_date(self):
        print(f"Pulling for extension {self.extension}")
        if self.extension in ['.mp4']:
            return self._vid_extract_via_exifread()
        elif self.extension in ['.jpg', '.png']:
            return self._img_extract_via_pil()
        elif self.extension in ['.cr2']:
            return self._img_extract_via_exifread()
        else:
            print("Unable to resolve exif data. Attempting file metadata...")
            return self._extract_via_file_properties()

        

# class DateTools:
#     def __init__(self):
#         pass

#     def get_date_taken_pil(self, path: Path, as_datetime: bool = True):
#         if exif := Image.open(path)._getexif():
#             return (
#                 datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')
#                 if as_datetime
#                 else exif[36867]
#             )
#         else:
#             raise LookupError('Image {0} does not have EXIF data.'.format(path))
    
#     def get_date_taken_exifread(self, path: Path, as_datetime: bool = True):
#         with open(path, "rb") as file_handle:
#             tags = exifread.process_file(file_handle)
#         print(tags)
#         exif_date = tags["EXIF DateTimeOriginal"].values
#         if as_datetime:
#             return datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
#         else:
#             return exif_date
    
#     def get_date_taken(self, path: Path, as_datetime: bool = True):
#         try:
#             # print("Trying pil...")
#             return self.get_date_taken_pil(path=path, as_datetime=as_datetime)
#         except Exception:
#             # print("")
#             return self.get_date_taken_exifread(path=path, as_datetime=as_datetime)



# # Open image file for reading (must be in binary mode)





# class PhotoMeta:
#     def __init__(self, path: str | Path):
#         self.path = Path(path)
#         metadata = MetaExtractor(path=self.path)
#         self.date = metadata.creation_date
#         self.date_yymmdd = self.date.strftime(format="%Y%m%d")
#         self.year = self.date.strftime(format="%Y")
#         self.season = self._seasons.get_season(self.date)
#         self.file_name = metadata.file_name
#         self.extension = metadata.extension

#         # self._base_metadata = MetaExtractor(path=self.path)
#         # # self._date_tools = DateTools()
#         # # self._seasons = Seasons()
#         # # self.path = Path(path)
#         # self.date = self._date_tools.get_date_taken(path = self.path)
#         # print(self.date)
#         # print(type(self.date))
#         # self.yyyymmdd = self.date.strftime(format="%Y%m%d")
#         # self.year = self.date.strftime(format="%Y")
#         # self.season = self._seasons.get_season(self.date)
#         # self.name = self.path.name
    
#     def _extract_date(self, path: Path) -> datetime:
#         with open(path, "rb") as file_handle:
#             tags = exifread.process_file(file_handle)
#         return datetime.strptime(tags["EXIF DateTimeOriginal"].values, "%Y:%m:%d %H:%M:%S")

class PhotoBro:
    def __init__(self, root_path: str, out_root: str):
        self.root_path = Path(root_path)
        self.out_path = Path(out_root)
        # self.metadata = MetaExtractor(path=self.root_path)
        # self.seasons = Seasons()
        # self.date_tools = DateTools()
        # self.root_path = Path(root_path)
        self.file_paths = list(self.root_path.glob('**/*'))
        
    def get_file_date(self, file_path: Path, as_str: bool = True, format: str = "%Y%m%d"):
        # file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
        file_date = self.date_tools.get_date_taken(path=file_path)
        return file_date.strftime(format=format) if as_str else file_date

    # def t1.strftime(format="%Y%m%d")
    def make_folder(self, path: Path, as_str: bool = True, format = "%Y%m%d") -> None:
        path.mkdir(parents=True, exist_ok=True)
    
    def do_the_thing(self) -> None:
        for file_path in self.file_paths:
            print(f"Processing file: {file_path}")
            if file_path.is_file():
                self.step_file = file_path
                # photo_meta = PhotoMeta(path=file_path)
                photo_meta = MetaExtractor(path=file_path)
                
                # file_date = self.get_file_date(file_path)
                # file_year = self.get_file_date(file_path, format="%Y")
                # file_season = self.seasons.get_season(self.get_file_date(file_path, as_str=False))
                
                self.make_folder(Path(self.out_path, photo_meta.creation_year, photo_meta.creation_season, photo_meta.creation_yyyymmdd))
                print(file_path)
                print(file_path.name)
                new_file_path = Path(self.out_path, photo_meta.creation_year, photo_meta.creation_season, photo_meta.creation_yyyymmdd, photo_meta.file_name)
                print(f"Attempting to copy\n\tfrom: {file_path}\n\tto: {new_file_path}")
                self.test = new_file_path
                if not new_file_path.exists():
                    print("Creating file")
                    shutil.copy(file_path, new_file_path)
                    file_path.unlink()
        print("\nRoutine complete!")


            

    
