from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Goal, Milestone, Category, GoalUpdate

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'category', 'priority', 'target_date', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('category', css_class='form-group col-md-6 mb-3'),
                Column('priority', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'target_date',
            Field('is_public', css_class='form-check'),
            Submit('submit', 'Save Goal', css_class='btn btn-primary btn-lg')
        )

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'target_date',
            Submit('submit', 'Add Milestone', css_class='btn btn-success')
        )

class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = GoalUpdate
        fields = ['content', 'progress_change']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your progress...'}),
            'progress_change': forms.NumberInput(attrs={'class': 'form-control', 'min': -100, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'content',
            'progress_change',
            Submit('submit', 'Update Progress', css_class='btn btn-primary')
        )
