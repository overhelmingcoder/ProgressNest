from django import forms
from .models import BlogPost, Comment, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class BlogPostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'excerpt', 'featured_image', 'categories', 'tags', 'status', 'allow_comments']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'excerpt',
            'content',
            'featured_image',
            'categories',
            'tags',
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('allow_comments', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Post', css_class='btn btn-primary')
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Add Comment', css_class='btn btn-primary')
        )
