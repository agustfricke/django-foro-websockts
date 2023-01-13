from django.forms import ModelForm

from . models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'text-negro text-sm rounded-lg block w-full p-2.5 placeholder-gray-400'

        self.fields['name'].widget.attrs['placeholder'] = 'Room Name'