from django import forms
from django.forms import ModelForm
from communityforum.models import ForumPost,Topic

class ForumPostForm(ModelForm):

    topics = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), 
                                            widget=forms.CheckboxSelectMultiple(attrs={"class":"d-flex"}),
                                            required=False,
                                            label="Relevant Topics")

    class Meta:
        model = ForumPost
        fields = ['title','topics','content','image','video_url']
        labels = {
            'title': 'Post Title',
            'topics': 'Relevant topics',
            'content': 'Post Content',
            'image': 'Image',
            'video_url': 'Video (YouTube)'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Title...'}),
            'content' : forms.Textarea(attrs={'class':'form-control','placeholder':'Content...'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'\'https://youtube.com\' (any youtube video url)','title':'Will add support for X, Vimeo etc... later'}),
        }

    def clean_video_url(self):
        url = str(self.cleaned_data.get('video_url'))

        valid_prefixes = [
            'https://www.youtube.com/watch?v=',
            'https://youtu.be/',
            'https://www.youtube.com/embed/',
        ]

        if not url.startswith('https://'):
            url = 'https://'+url

        url_match = False
        for prefix in valid_prefixes:
            if url.startswith(prefix):
                url_match = True
                break
        
        if not url_match:
            raise forms.ValidationError("Please enter a valid YouTube URL.")

        # Convert to embed format
        video_id = None
        if '/watch?v=' in url:
            url = url.split('watch?v=')[-1]
            video_id = url.split('&')[0]
        elif '/youtu.be/' in url:
            video_id = url.split('/')[-1]
        elif '/embed/' in url:
            return url

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'

        raise forms.ValidationError("Unable to extract YouTube video ID.")