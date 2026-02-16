from accounts.models import VerificationSelfie, FaceStatus
from accounts.tasks import verify_selfie_task


def upload_selfie(*, user, image):
    obj, _ = VerificationSelfie.objects.update_or_create(
        user=user,
        defaults={"image": image, "note": None},
    )

    # darhol PENDING (background tekshiruv ketadi)
    user.face_status = FaceStatus.PENDING
    user.save(update_fields=["face_status"])

    # background task ishga tushadi
    verify_selfie_task.delay(user.id)

    return obj
