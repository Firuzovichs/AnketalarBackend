from celery import shared_task
from django.db import transaction
from accounts.models import User, VerificationSelfie, FaceStatus
from accounts.services.face_service_opencv import detect_face_opencv


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def verify_selfie_task(self, user_id: int) -> dict:
    """
    Selfie tekshiruv (background).
    - yuz topilsa: APPROVED (MVP)
    - topilmasa: REJECTED
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {"ok": False, "reason": "user_not_found"}

    try:
        selfie = VerificationSelfie.objects.get(user=user)
    except VerificationSelfie.DoesNotExist:
        return {"ok": False, "reason": "selfie_not_found"}

    # Fayl system path
    try:
        image_path = selfie.image.path
    except Exception as e:
        return {"ok": False, "reason": f"image_path_error: {e}"}

    # Face detection
    try:
        check = detect_face_opencv(image_path)
    except Exception as e:
        # transient bo'lishi mumkin — retry
        raise self.retry(exc=e)

    with transaction.atomic():
        selfie = VerificationSelfie.objects.select_for_update().get(id=selfie.id)
        user = User.objects.select_for_update().get(id=user.id)

        if not check.has_face:
            user.face_status = FaceStatus.REJECTED
            user.save(update_fields=["face_status"])

            selfie.note = f"No face detected ({check.reason})"
            selfie.save(update_fields=["note"])
            return {"ok": True, "status": "REJECTED", "faces": 0}

        # MVP: yuz bor bo'lsa avtomatik tasdiqlash
        user.face_status = FaceStatus.APPROVED
        user.save(update_fields=["face_status"])

        selfie.note = f"Face detected, count={check.faces_count}"
        selfie.save(update_fields=["note"])
        return {"ok": True, "status": "APPROVED", "faces": int(check.faces_count)}
