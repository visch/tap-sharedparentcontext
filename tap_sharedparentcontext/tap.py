"""SharedParentContext tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_sharedparentcontext import streams


class TapSharedParentContext(Tap):
    """SharedParentContext tap class."""

    name = "tap-sharedparentcontext"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
    ).to_dict()

    def discover_streams(self) -> list[streams.SharedParentContextStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
            streams.UsersChildOneStream(self),
            streams.UsersChildTwoStream(self),
        ]


if __name__ == "__main__":
    TapSharedParentContext.cli()
