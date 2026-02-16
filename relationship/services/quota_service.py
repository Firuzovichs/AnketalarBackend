from dataclasses import dataclass
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from relationship.models import DailyQuota

DAILY_LIMIT_DEFAULT = 50

ACTION_COST = {
    "like": 1,
    "skip": 1,
    "comment_like": 1,
}

@dataclass
class QuotaState:
    limit: int
    used: int
    remaining: int

def get_daily_limit_for_user(user) -> int:
    return DAILY_LIMIT_DEFAULT

@transaction.atomic
def consume_quota(user, action: str) -> QuotaState:
    # 1) profil to'liq bo'lmasa umuman ruxsat bermaslik ham mumkin:
    profile = getattr(user, "profile", None)
    if not profile or not getattr(profile, "is_profile_complete", False):
        raise PermissionDenied("Profile to'liq emas. Avval profilni to'ldiring.")

    cost = ACTION_COST.get(action)
    if cost is None:
        raise PermissionDenied("Unknown action for quota")

    limit = get_daily_limit_for_user(user)

    today = timezone.localdate()
    quota, _ = DailyQuota.objects.select_for_update().get_or_create(
        user=user, date=today, defaults={"used": 0}
    )

    if quota.used + cost > limit:
        # Siz xohlasangiz 429 qaytarish ham mumkin (quyida ko'rsataman)
        raise PermissionDenied(f"Kunlik limit tugadi. Limit={limit}, Used={quota.used}")

    quota.used += cost
    quota.save(update_fields=["used"])

    return QuotaState(limit=limit, used=quota.used, remaining=limit - quota.used)
