from django import forms
from .models import Group, GroupPost, GroupPostComment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'category', 'privacy', 'cover_image', 'logo', 'rules', 'tags', 'allow_member_posts', 'require_approval']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'rules': forms.Textarea(attrs={'rows': 6}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('privacy', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cover_image', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'rules',
            'tags',
            Row(
                Column('allow_member_posts', css_class='form-group col-md-6 mb-0'),
                Column('require_approval', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create Group', css_class='btn btn-primary')
        )

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['title', 'content', 'image', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('file', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create Post', css_class='btn btn-primary')
        )

class GroupPostCommentForm(forms.ModelForm):
    class Meta:
        model = GroupPostComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})
        }
