import django.forms as forms

from ..models import *


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = '__all__'
        exclude = ('gallery', 'seo', 'info_gallery')
        widgets = {
            'show_app_links': forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none'}),
            'description': forms.Textarea(attrs={'class': 'summernote'})
        }


class TariffSiteForm(forms.ModelForm):
    class Meta:
        model = TariffSite
        fields = '__all__'
        exclude = ('seo', 'gallery')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'summernote'})
        }


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = '__all__'
        exclude = ('gallery', 'seo', 'extra_gallery')
        widgets = {
            'director_photo': forms.FileInput(attrs={'class': ''}),
            'description': forms.Textarea(attrs={'class': 'summernote'}),
            'extra_description': forms.Textarea(attrs={'class': 'summernote'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'
        exclude = ('seo',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'summernote'}),
            'coordinate': forms.Textarea(attrs={'rows': 6}),

        }


class AboutUsDocumentForm(forms.ModelForm):
    class Meta:
        model = AboutUsDocument
        fields = '__all__'
        exclude = ('about_us',)
        widgets = {
            'file': forms.FileInput(attrs={'class': ''})
        }


AboutUsDocumentFormset = forms.modelformset_factory(model=AboutUsDocument, form=AboutUsDocumentForm, extra=0)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ('gallery',)
        widgets = {
            'img': forms.FileInput(attrs={'class': ''})
        }


PhotoFormset = forms.modelformset_factory(model=Photo, form=PhotoForm, extra=0)
ExtraPhotoFormset = forms.modelformset_factory(model=Photo, form=PhotoForm, extra=1)
HousePhotoFormset = forms.modelformset_factory(model=Photo, form=PhotoForm, extra=5)


class InfoPhotoForm(forms.ModelForm):
    class Meta:
        model = InfoPhoto
        fields = '__all__'
        exclude = ('gallery',)
        widgets = {
            'img': forms.FileInput(attrs={'class': ''}),
            'description': forms.Textarea(attrs={'class': 'summernote'})

        }


InfoPhotoFormset = forms.modelformset_factory(model=InfoPhoto, form=InfoPhotoForm, extra=0, can_delete=True)


class InfoPhotoLiteForm(forms.ModelForm):
    img = forms.FileField(label='Файл')
    title = forms.CharField(label='Подпись')

    class Meta:
        model = InfoPhoto
        fields = '__all__'
        exclude = ('gallery', 'description')
        widgets = {
            'img': forms.FileInput(attrs={'class': ''}),
        }


InfoPhotoLiteFormset = forms.modelformset_factory(model=InfoPhoto, form=InfoPhotoLiteForm, extra=0, can_delete=True)


class SeoForm(forms.ModelForm):
    class Meta:
        model = Seo
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'keywords': forms.Textarea(attrs={'rows': 6})
        }
