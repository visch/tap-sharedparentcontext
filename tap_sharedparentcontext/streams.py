"""Stream type classes for tap-sharedparentcontext."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_sharedparentcontext.client import SharedParentContextStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class UsersStream(SharedParentContextStream):
    """Define custom stream."""

    name = "users"
    path = "/users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property(
            "id",
            th.StringType,
            description="The user's system ID",
        ),
        th.Property(
            "age",
            th.IntegerType,
            description="The user's age in years",
        ),
        th.Property(
            "email",
            th.StringType,
            description="The user's email address",
        ),
        th.Property("street", th.StringType),
        th.Property("city", th.StringType),
        th.Property(
            "state",
            th.StringType,
            description="State name in ISO 3166-2 format",
        ),
        th.Property("zip", th.StringType),
    ).to_dict()

    def get_records(self, context: dict) -> t.Generator[dict, None, None]:
        """Return a generator of record-type dictionary objects."""
        return [
            {
                "id": "1",
                "name": "John Doe",
                "age": 30,
            }
        ]
    
    def get_child_context(
        self,
        record,
        context,
    ) -> dict | None:
        return { "id": record["id"] }


class UsersChildOneStream(SharedParentContextStream):
    """Define custom stream."""

    name = "users_child_one"
    path = "/users_child_one"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "modified"
    parent_stream_type = UsersStream
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()

    def get_records(self, context: dict) -> t.Generator[dict, None, None]:
        """Return a generator of record-type dictionary objects."""
        context["url_parameter_for_user_child_one"] = "1"
        self.logger.info(f"Context User Child One: {context}")
        return [
            {
                "id": "1",
                "name": "John Doe",
                "modified": "2021-01-01T00:00:00Z",
            }
        ]

class UsersChildTwoStream(SharedParentContextStream):
    """Define custom stream."""

    name = "users_child_two"
    path = "/users_child_two"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "modified"
    parent_stream_type = UsersStream
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()

    def get_records(self, context: dict) -> t.Generator[dict, None, None]:
        """Return a generator of record-type dictionary objects."""
        record = {
                "id": "1",
                "name": "John Doe",
                "modified": "2021-01-01T00:00:00Z",
            }
        self.logger.info(f"Context User Child Two: {context}")
        return [record]