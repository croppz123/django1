import os

from PIL import Image
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django_countries.widgets import CountrySelectWidget
from dj1.settings import MEDIA_ROOT
from django.core.files.images import get_image_dimensions

from core.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'birth_date', 'city', 'country', 'bio']
        widgets = {
            'country': CountrySelectWidget(),
            'birth_date': DatePickerInput(options={'dateFormat': 'yy-mm-dd',
                                                   'changeMonth': True,
                                                   'changeYear': True}),
            'bio': forms.Textarea(attrs={'rows': 6,
                                         'style': 'resize: none;',
                                         'maxlength': Profile._meta.get_field('bio').max_length})
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {'avatar': forms.FileInput}

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        width, height = get_image_dimensions(avatar)
        if width < 150 or height < 150:
            raise forms.ValidationError("avatar must be at least 150 x 150 px")

        return avatar

    def save(self, commit=True):
        super().save()
        avatar = self.instance.avatar
        with Image.open(avatar.file) as image:
            cropped = self._crop(image)
            resized = cropped.resize((150, 150), Image.LANCZOS)
            resized.save(
                os.path.join(MEDIA_ROOT, avatar.name),
                format=image.format, quality=100,
                save=True
            )

    @staticmethod
    def _crop(image):
        width, height = image.size
        if width == height:
            return image

        target_size = min(image.size)

        if width > target_size:
            left = width // 2 - target_size // 2
            right = width // 2 + target_size // 2
            box = left, 0, right, target_size
        else:
            up = height // 2 - target_size // 2
            down = height // 2 + target_size // 2
            box = 0, up, target_size, down

        image = image.crop(box)
        return image












