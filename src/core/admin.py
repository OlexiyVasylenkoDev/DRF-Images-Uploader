from django.contrib import admin

from core.models import AccountTier, CustomUser, Image, Thumbnail

# Register your models here.


admin.site.register([Thumbnail, AccountTier])


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "account_tier", "number_of_images")
    list_filter = ("account_tier",)
    search_fields = ("username__icontains",)

    def number_of_images(self, user):
        return Image.objects.filter(user=user).count()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ("img_preview",)
    list_display = (
        "id",
        "file",
        "img_preview",
        "user",
    )
    list_filter = ("user",)
    search_fields = ("username__icontains",)
