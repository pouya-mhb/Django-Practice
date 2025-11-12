from django import forms
from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter the title"}),
            "body": forms.Textarea(attrs={"placeholder": "Write your post here"}),
            "tags": forms.TextInput(
                attrs={"placeholder": "Add tags separated by commas"}
            ),
        }


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Your name")
    email = forms.EmailField(label="Your email")
    to = forms.EmailField(label="Recipient email")
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(),
        label="Add a comment (optional)",
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("title", "body")
