from django import forms
from user.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Make your post...',
                'class': 'post-textarea',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'post-file-input',
            }),
        }
