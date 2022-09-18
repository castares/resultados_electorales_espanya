from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from pandas import DataFrame


class Area(str, Enum):
    CCAA = "Comunidad Autónoma"
    PROVINCIA = "Provincia"
    MUNICIPIO = "Municipio"


class AreaProcessor:
    _areas: dict[Area, str] = {
        Area.CCAA: "Nombre de Comunidad",
        Area.PROVINCIA: "Nombre de Provincia",
        Area.MUNICIPIO: "Nombre de Municipio",
    }

    def data_by_area(self, data: DataFrame, area: Area):
        area_field: Optional[str] = self._areas.get(area)
        if not area_field:
            raise NameError("area is not valid. Please select valid area.")
        data_by_area = data.groupby(by=[area_field]).sum()
        return data_by_area
