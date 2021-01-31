"""Haapi Games RawG Genre."""
import dataclasses
from typing import Optional

import desert
import marshmallow


@dataclasses.dataclass
class Genre:
    """RawG Genre."""

    id: int
    name: str
    slug: str
    games_count: Optional[int]
    image_background: Optional[str] = dataclasses.field(
        default=None,
        metadata=desert.metadata(field=marshmallow.fields.Url(allow_none=True)),
    )
