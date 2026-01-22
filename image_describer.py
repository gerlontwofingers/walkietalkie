from dataclasses import dataclass
from pathlib import Path

from captioning import Captionator, GetImage
from yolo_detector import YOLOConfidenceDetector
from utils import MetaExtractor

@dataclass(frozen=True)
class ImageDescription:
    caption: str
    detected: str
    meta: MetaExtractor

class ImageDescriber:
    def __init__(self):
        self._captionator = Captionator()
        self._captionator.initialize()
        self._detection = YOLOConfidenceDetector()
        self.last_image: None | GetImage = None
    
    # def register_image(self, path: str | Path) -> None:
    #     self.image = GetImage(path=path)
    
    def get_descriptions(self, path: str | Path, min_conf: float = 0.55) -> ImageDescription:
        self.last_image = GetImage(path=path)
        return ImageDescription(
            caption=self._captionator.get_caption(image=self.last_image.image),
            detected=self._detection.confidence_dict_to_sentence(image=self.last_image.image, confidence_threshold=min_conf),
            meta=MetaExtractor(path=path)
        )

    def make_journal_entry(self, path: str | Path, min_conf: float = 0.55) -> str:
        print(f"\n>>>> Image analysis for {path}: \n")
        description = self.get_descriptions(
            path=path,
            min_conf=min_conf
        )
        if description.meta.creation_date == description.meta.default_date:
            img_date_statement = (
                f"Creation date did not exist in EXIF. No date available, "
                f"so dates set to default {description.meta.default_date}."
            )
        else:
            img_date_statement = (
                "This image was taken "
                rf"{description.meta.creation_date.strftime("%b %d, %Y")}, "
                rf"in the {description.meta.creation_season}."
            )
        return (
            f"{img_date_statement}\n"
            f"In this image, we can see {description.caption}.\n"
            f"{description.detected}"
        )
