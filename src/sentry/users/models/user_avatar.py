from __future__ import annotations

import contextlib
from collections.abc import Generator
from enum import IntEnum
from typing import Any, ClassVar, Self

from django.db import models, router, transaction

from sentry.db.models import FlexibleForeignKey, control_silo_model
from sentry.db.models.manager.base import BaseManager
from sentry.hybridcloud.models.outbox import ControlOutboxBase
from sentry.hybridcloud.outbox.category import OutboxCategory
from sentry.models.avatars import ControlAvatarBase
from sentry.types.region import find_regions_for_user


class UserAvatarType(IntEnum):
    LETTER_AVATAR = 0
    UPLOAD = 1
    GRAVATAR = 2

    def api_name(self) -> str:
        return self.name.lower()

    @classmethod
    def as_choices(cls) -> tuple[tuple[int, str], ...]:
        return (
            (cls.LETTER_AVATAR, cls.LETTER_AVATAR.api_name()),
            (cls.UPLOAD, cls.UPLOAD.api_name()),
            (cls.GRAVATAR, cls.GRAVATAR.api_name()),
        )


@control_silo_model
class UserAvatar(ControlAvatarBase):
    """
    A UserAvatar associates a User with their avatar photo File
    and contains their preferences for avatar type.
    """

    AVATAR_TYPES = UserAvatarType.as_choices()

    FILE_TYPE = "avatar.file"

    user = FlexibleForeignKey("sentry.User", unique=True, related_name="avatar")
    avatar_type = models.PositiveSmallIntegerField(default=0, choices=UserAvatarType.as_choices())

    objects: ClassVar[BaseManager[Self]] = BaseManager(cache_fields=["user"])

    class Meta:
        app_label = "sentry"
        db_table = "sentry_useravatar"

    url_path = "avatar"

    def outboxes_for_update(self, shard_identifier: int | None = None) -> list[ControlOutboxBase]:
        regions = find_regions_for_user(self.user_id)
        return OutboxCategory.USER_UPDATE.as_control_outboxes(
            region_names=regions,
            shard_identifier=self.user_id,
            object_identifier=self.user_id,
        )

    @contextlib.contextmanager
    def _maybe_prepare_outboxes(self, *, outbox_before_super: bool) -> Generator[None]:
        from sentry.hybridcloud.models.outbox import outbox_context

        with outbox_context(
            transaction.atomic(router.db_for_write(type(self))),
        ):
            if not outbox_before_super:
                yield
            for outbox in self.outboxes_for_update():
                outbox.save()
            if outbox_before_super:
                yield

    def save(self, *args: Any, **kwds: Any) -> None:
        with self._maybe_prepare_outboxes(outbox_before_super=False):
            super().save(*args, **kwds)

    def update(self, *args: Any, **kwds: Any) -> int:
        with self._maybe_prepare_outboxes(outbox_before_super=False):
            return super().update(*args, **kwds)

    def delete(self, *args: Any, **kwds: Any) -> tuple[int, dict[str, Any]]:
        with self._maybe_prepare_outboxes(outbox_before_super=True):
            return super().delete(*args, **kwds)

    def get_cache_key(self, size: int) -> str:
        return f"avatar:{self.user_id}:{size}"
