from enum import Enum
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
    area_field_value: str

    def data_by_area(self, data: DataFrame, area: Area):
        area_field: Optional[str] = self._areas.get(area)
        # TODO: Refactor to avoid side-effects
        self.area_field_value = area_field
        if not area_field:
            raise NameError("Area is not valid. Please select valid area.")
        data_by_area = data.groupby(by=[area_field]).sum(numeric_only=True)
        return data_by_area
