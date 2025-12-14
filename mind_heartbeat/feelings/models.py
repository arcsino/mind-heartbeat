from datetime import datetime
from uuid import uuid4

from accounts.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Stamp(models.Model):
    """Stamp model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("スタンプ名"),
        max_length=100,
        unique=True,
        help_text=_("スタンプ名は必須です。固有の名前を指定してください。"),
    )
    color = models.CharField(
        verbose_name=_("スタンプ色"),
        max_length=16,
        choices=[
            ("textcolor-red", "赤"),
            ("textcolor-orange", "橙"),
            ("textcolor-yellow", "黄"),
            ("textcolor-lime", "黄緑"),
            ("textcolor-green", "緑"),
            ("textcolor-cyan", "水色"),
            ("textcolor-blue", "青"),
            ("textcolor-purple", "紫"),
        ],
        default="textcolor-blue",
        help_text=_("感情の色を選択してください。"),
    )
    score = models.IntegerField(
        verbose_name=_("スコア"),
        default=0,
        help_text=_("スタンプのスコアを整数で指定してください。"),
    )
    image = models.ImageField(
        verbose_name=_("スタンプ画像"),
        upload_to="stamps/",
        blank=True,
        null=True,
        help_text=_("スタンプの画像ファイルをアップロードしてください。"),
    )
    created_at = models.DateTimeField(verbose_name=_("作成日時"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("更新日時"), auto_now=True)

    class Meta:
        verbose_name = _("スタンプ")
        verbose_name_plural = _("スタンプ一覧")

    def __str__(self):
        return self.name


class Feeling(models.Model):
    """Feeling model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    stamp = models.ForeignKey(
        Stamp,
        verbose_name=_("スタンプ"),
        on_delete=models.CASCADE,
        related_name="feelings",
    )
    comment = models.TextField(
        verbose_name=_("コメント"),
        max_length=500,
        blank=True,
        help_text=_("気持ちに関するコメントを入力してください。"),
    )
    felt_at = models.DateTimeField(
        verbose_name=_("感じた日時"),
        default=datetime.now(),
        help_text=_("気持ちを感じた日時を指定してください。"),
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("作成者"),
        on_delete=models.CASCADE,
        related_name="feelings",
    )
    created_at = models.DateTimeField(verbose_name=_("作成日時"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("更新日時"), auto_now=True)

    class Meta:
        verbose_name = _("気持ち")
        verbose_name_plural = _("気持ち一覧")

    def __str__(self):
        return f"{self.created_by.username}の気持ち - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
