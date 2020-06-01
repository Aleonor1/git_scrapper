from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'


class InstanceCreationForm(forms.Form):
    some_field = forms.BooleanField(required=False)
    some_field2 = forms.BooleanField(required=False)
    some_field3 = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(InstanceCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            #This is a syntax error
            Field('some_field', data-label-text="whatever")
        )
        self.helper.add_input(Submit('submit', 'Submit'))