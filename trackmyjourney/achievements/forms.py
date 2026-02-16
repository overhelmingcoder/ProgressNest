from django import forms
from .models import Achievement, AchievementComment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'category', 'badge_type', 'image', 'date_achieved', 'is_public']
        widgets = {
            'date_achieved': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('badge_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'image',
            Row(
                Column('date_achieved', css_class='form-group col-md-6 mb-0'),
                Column('is_public', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Achievement', css_class='btn btn-primary')
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = AchievementComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Add Comment', css_class='btn btn-primary btn-sm')
        )
