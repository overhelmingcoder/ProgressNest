from django import forms
from .models import Book, BookCategory, BookRating, ReadingList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=BookCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'categories', 'file', 'cover_image', 
                 'format', 'language', 'pages', 'publisher', 'publication_date', 'tags', 
                 'is_public', 'allow_download']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'author',
            'isbn',
            'description',
            'categories',
            Row(
                Column('file', css_class='form-group col-md-6 mb-0'),
                Column('cover_image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('format', css_class='form-group col-md-4 mb-0'),
                Column('language', css_class='form-group col-md-4 mb-0'),
                Column('pages', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('publisher', css_class='form-group col-md-6 mb-0'),
                Column('publication_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'tags',
            Row(
                Column('is_public', css_class='form-group col-md-6 mb-0'),
                Column('allow_download', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Upload Book', css_class='btn btn-primary')
        )

class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]),
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review...'})
        }

class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['status', 'progress', 'notes']
        widgets = {
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'notes': forms.Textarea(attrs={'rows': 3})
        }
