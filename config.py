from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Seasonator:
    leap_year: int = 2000 # dummy leap year to allow input X-02-29 (leap day)
    seasons = [
        ('winter', (date(leap_year,  1,  1),  date(leap_year,  3, 20))),
        ('spring', (date(leap_year,  3, 21),  date(leap_year,  6, 20))),
        ('summer', (date(leap_year,  6, 21),  date(leap_year,  9, 22))),
        ('fall', (date(leap_year,  9, 23),  date(leap_year, 12, 20))),
        ('winter', (date(leap_year, 12, 21),  date(leap_year, 12, 31)))
    ]
