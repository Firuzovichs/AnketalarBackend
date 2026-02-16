from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from models.relationship import Relationship, RelationStatus

@transaction.atomic
def like_user(*, actor, target, comment: str = "") -> dict:
    if actor.id == target.id:
        raise ValidationError("Self-like mumkin emas")

    # A -> B
    rel, _ = Relationship.objects.select_for_update().get_or_create(
        from_user=actor, to_user=target,
        defaults={"status": RelationStatus.LIKED, "comment": comment or ""}
    )

    # agar oldin SKIPPED/REJECTED bo'lgan bo'lsa, endi LIKE ga qaytarish
    rel.status = RelationStatus.LIKED
    if comment is not None:
        rel.comment = comment  # bo'sh bo'lsa ham yangilayveramiz
    rel.save(update_fields=["status", "comment", "updated_at"])

    # B -> A bor-yo'qligini tekshiramiz (qarshi like)
    reverse = Relationship.objects.select_for_update().filter(
        from_user=target, to_user=actor, status=RelationStatus.LIKED
    ).first()

    matched = False
    if reverse:
        # Ikkalasini ham MATCHED qilamiz
        Relationship.objects.filter(id__in=[rel.id, reverse.id]).update(status=RelationStatus.MATCHED)
        matched = True

    return {"matched": matched, "relation_status": RelationStatus.MATCHED if matched else RelationStatus.LIKED}


@transaction.atomic
def accept_incoming_like(*, actor, liker) -> dict:
    """
    actor = men (qabul qiluvchi)
    liker = menga like bosgan user
    Qabul qilish: actor -> liker LIKE bo'ladi va agar liker->actor LIKE bo'lsa MATCH bo'ladi.
    """
    # liker -> actor LIKE bo'lishi kerak
    incoming = Relationship.objects.select_for_update().filter(
        from_user=liker, to_user=actor, status=RelationStatus.LIKED
    ).first()
    if not incoming:
        raise ValidationError("Incoming like topilmadi")

    # actor -> liker LIKE
    return like_user(actor=actor, target=liker, comment="")  # comment optional


@transaction.atomic
def reject_incoming_like(*, actor, liker) -> None:
    # liker -> actor ni REJECTED qilamiz (yoki delete)
    incoming = Relationship.objects.select_for_update().filter(from_user=liker, to_user=actor).first()
    if not incoming:
        return
    incoming.status = RelationStatus.REJECTED
    incoming.save(update_fields=["status", "updated_at"])


@transaction.atomic
def comment_like(*, actor, liker) -> None:
    """
    actor = men (qabul qiluvchi)
    liker = menga like bosgan user
    actor comment_like bosganda incoming row'da comment_liked_at belgilanadi
    """
    rel = Relationship.objects.select_for_update().filter(from_user=liker, to_user=actor).first()
    if not rel:
        raise ValidationError("Relation topilmadi")
    rel.comment_liked_at = timezone.now()
    rel.save(update_fields=["comment_liked_at", "updated_at"])
