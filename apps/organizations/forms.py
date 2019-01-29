import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        pattern = re.compile(r'^1[35678]\d{9}$')
        ret = re.search(pattern, mobile)
        if ret:
            return mobile
        else:
            return forms.ValidationError('手机号码非法', code='mobile_invalid')
