from django import forms
from .models import Resource, ResourceComment, ResourceRating

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'category', 'resource_type', 'file', 'url', 'thumbnail', 'tags', 'is_public', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        }

class ResourceCommentForm(forms.ModelForm):
    class Meta:
        model = ResourceComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class ResourceRatingForm(forms.ModelForm):
    class Meta:
        model = ResourceRating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts on this resource (optional)'}),
            'rating': forms.RadioSelect(), # Renders as radio buttons for star rating
        }
