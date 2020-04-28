from . import models
from django.forms import ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
