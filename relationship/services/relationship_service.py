from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from relationship.models import Relationship, RelationStatus

@transaction.atomic
def like_or_comment(*, actor, target, comment: str | None = None) -> dict:
    if actor.id == target.id:
        raise ValidationError("Self-like mumkin emas")

    # A -> B row
    rel, _ = Relationship.objects.select_for_update().get_or_create(
        from_user=actor,
        to_user=target,
        defaults={
            "status": RelationStatus.LIKED,
            "comment": (comment or "").strip(),
        },
    )

    # Update
    rel.status = RelationStatus.LIKED
    if comment is not None:
        rel.comment = (comment or "").strip()
    rel.save(update_fields=["status", "comment", "updated_at"])

    # Reverse LIKE bormi?
    reverse = Relationship.objects.select_for_update().filter(
        from_user=target,
        to_user=actor,
        status=RelationStatus.LIKED,
    ).first()

    matched = False
    if reverse:
        Relationship.objects.filter(id__in=[rel.id, reverse.id]).update(status=RelationStatus.MATCHED)
        matched = True

    return {
        "matched": matched,
        "status": RelationStatus.MATCHED if matched else RelationStatus.LIKED,
    }


@transaction.atomic
def like_only(*, actor, target) -> dict:
    # comment berilmaydi, agar oldin comment bo'lsa ham o'chirmaymiz
    return like_or_comment(actor=actor, target=target, comment=None)


@transaction.atomic
def comment_only(*, actor, target, comment: str) -> dict:
    # comment majburiy (bo'sh bo'lmasin)
    c = (comment or "").strip()
    if not c:
        raise ValidationError("Comment bo'sh bo'lmasin")
    return like_or_comment(actor=actor, target=target, comment=c)


@transaction.atomic
def comment_like(*, actor, liker) -> None:
    """
    actor = men
    liker = menga like/comment yozgan user (incoming)
    """
    rel = Relationship.objects.select_for_update().filter(from_user=liker, to_user=actor).first()
    if not rel:
        raise ValidationError("Relationship topilmadi")
    rel.comment_liked_at = timezone.now()
    rel.save(update_fields=["comment_liked_at", "updated_at"])
