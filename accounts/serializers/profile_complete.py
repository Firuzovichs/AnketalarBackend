from rest_framework import serializers
from accounts.models import UserProfile, Interest, Purpose, Region, District

class ProfileCompleteSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.filter(is_active=True),
        many=True
    )
    purposes = serializers.PrimaryKeyRelatedField(
        queryset=Purpose.objects.filter(is_active=True),
        many=True
    )
    birth_region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    birth_district = serializers.PrimaryKeyRelatedField(queryset=District.objects.select_related("region").all())

    # IXTiyoriy fieldlar (yuborilmasa ham xato bermaydi)
    bio = serializers.CharField(required=False, allow_blank=True)
    telegram_link = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    instagram_link = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    tiktok_link = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    smoking = serializers.ChoiceField(required=False, choices=UserProfile._meta.get_field("smoking").choices)

    latitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6, allow_null=True)
    longitude = serializers.DecimalField(required=False, max_digits=9, decimal_places=6, allow_null=True)

    class Meta:
        model = UserProfile
        fields = (
            "first_name", "last_name",
            "birth_date", "gender",
            "birth_region", "birth_district",
            "height_cm", "weight_kg",
            "interests", "purposes",
            "bio",
            "telegram_link", "instagram_link", "tiktok_link",
            "smoking",
            "latitude", "longitude",
        )

    def validate(self, attrs):
        # district regionga mosligini tekshirish
        region = attrs.get("birth_region") or getattr(self.instance, "birth_region", None)
        district = attrs.get("birth_district") or getattr(self.instance, "birth_district", None)
        if region and district and district.region_id != region.id:
            raise serializers.ValidationError({"birth_district": "District tanlangan regionga tegishli emas."})

        # POST paytida majburiy: interests/purposes kamida 1 ta bo‘lsin
        if self.instance is None:
            if "interests" not in attrs or len(attrs["interests"]) < 1:
                raise serializers.ValidationError({"interests": "Kamida 1 ta qiziqish tanlang."})
            if "purposes" not in attrs or len(attrs["purposes"]) < 1:
                raise serializers.ValidationError({"purposes": "Kamida 1 ta maqsad tanlang."})

        return attrs

    def update(self, instance, validated_data):
        interests = validated_data.pop("interests", None)
        purposes = validated_data.pop("purposes", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.full_clean()
        instance.save()

        if interests is not None:
            instance.interests.set(interests)
        if purposes is not None:
            instance.purposes.set(purposes)

        return instance
