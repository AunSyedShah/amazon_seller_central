from django.contrib import admin
from .models import Product, UserProfile, Order
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def resize_image_for_product(image, width, height):
    im = Image.open(image)
    im = im.resize((width, height))
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=100)
    resized_image = InMemoryUploadedFile(
        im_io,
        None,
        image.name,
        "image/jpeg",
        im_io.getbuffer().nbytes,
        None,
    )
    return resized_image


class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.image:
            obj.image = resize_image_for_product(obj.image, 300, 300)
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)
admin.site.register(Order)
