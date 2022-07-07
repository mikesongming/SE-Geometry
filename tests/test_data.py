from dataclasses import fields

from fseg import Observatory
from fseg.impl import Algorithm


class TestDataSchemaConsistency:
    def test_observatory(self):
        assert Algorithm.OBS_FIELDS == [fld.name for fld in fields(Observatory)]
