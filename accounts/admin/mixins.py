from django.utils.html import format_html

class ImagePreviewMixin:
    @staticmethod
    def img(url: str, h: int = 44):
        return format_html('<img src="{}" style="height:{}px;border-radius:10px;" />', url, h)

class MapLinkMixin:
    @staticmethod
    def map_link(lat, lon):
        if lat is None or lon is None:
            return "-"
        # Google Maps link (admin ichida qulay)
        return format_html(
            '<a target="_blank" href="https://www.google.com/maps?q={},{}">Open map</a>',
            lat, lon
        )
