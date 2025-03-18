from django import forms
from .models import Geojson,ColorRange,ColorRangeFamily
import json


class StateSelectionForm(forms.Form):
    state = forms.ChoiceField(
        label="Select State",
        widget=forms.Select(attrs={'class': 'form-control','id':'state-select'}),
        choices=[('', 'Select State')]
    )
    district = forms.ChoiceField(
        label="Select District",
        widget=forms.Select(attrs={'class': 'form-control','id':'district-select'}),
        choices=[('', 'Select District')],
        required=False
    )
    sub_district = forms.ChoiceField(
        label="Select Sub-District",
        widget=forms.Select(attrs={'class': 'form-control','id':'sub_district-select'}),
        choices=[('', 'Select Sub-District')],
        required=False
    )
    block = forms.ChoiceField(
        label="Select Block",
        widget=forms.Select(attrs={'class': 'form-control','id':'block-select'}),
        choices=[('', 'Select Block')],
        required=False
    )
    pincode = forms.ChoiceField(
        label="Select Pincode",
        widget=forms.Select(attrs={'class': 'form-control','id':'pincode-select'}),
        choices=[('', 'Select Pincode')],
        required=False
    )
    gram_panchayat = forms.ChoiceField(
        label="Select Gram Panchayat",
        widget=forms.Select(attrs={'class': 'form-control','id':'gram_panchayat-select'}),
        choices=[('', 'Select Gram Panchayat')],
        required=False
    )
    town_village = forms.ChoiceField(
        label="Select Town/Village",
        widget=forms.Select(attrs={'class': 'form-control','id':'town_village-select'}),
        choices=[('', 'Select Town/Village')],
        required=False
    )
    
    boundary = forms.ChoiceField(
        label="Boundary Type",
        widget=forms.Select(attrs={'class': 'form-control','id':'boundary-select'}),
        choices=[('', 'Select Boundary')],
        required=True
    )

    family_name = forms.ChoiceField(
        label="Color Family",
        widget=forms.Select(attrs={'class': 'form-control','id':'family_name-select'}),
        choices=[(1,'Default')],
        required=True
    )

    def __init__(self, *args, **kwargs):
        state = kwargs.pop('state', None)
        district = kwargs.pop('district', None)
        sub_district = kwargs.pop('sub_district', None)
        block = kwargs.pop('block', None)
        pincode = kwargs.pop('pincode', None)
        gram_panchayat = kwargs.pop('gram_panchayat', None)
        town_village = kwargs.pop('town_village', None)

        last_nonempty_field = kwargs.pop('last_nonempty_field', None)
        user = kwargs.pop('user',None)

        super().__init__(*args, **kwargs)
        # Populate state choices
        geojsons = Geojson.objects.all()
        state_list = [(geojson.state_name, geojson.state_name) for geojson in geojsons]
        self.fields['state'].choices += state_list

        # Populate color family choices
        color_families = ColorRangeFamily.objects.filter(created_by=user)
        family_list = [(family.id,family.family_name) for family in color_families]
        self.fields['family_name'].choices += family_list

        # Populate district choices if a state is provided
        if state:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.district_geojson.open('r') as file:
                geojson_data = json.load(file)
            district_list = [(feature['properties']['DIST_NAME'], feature['properties']['DIST_NAME']) for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower())]
            self.fields['district'].choices += district_list
                
        if district:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.sub_district_geojson.open('r') as file:
                geojson_data = json.load(file)
            sub_district_list = [(feature['properties']['SUB_DIST_N'],feature['properties']['SUB_DIST_N'])  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower())]
            self.fields['sub_district'].choices += sub_district_list

        if sub_district:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.block_geojson.open('r') as file:
                geojson_data = json.load(file)
            block_list = [(feature['properties']['BLOCK_NAME'],feature['properties']['BLOCK_NAME'])  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower())]
            self.fields['block'].choices += block_list

        if block:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.pincode_geojson.open('r') as file:
                geojson_data = json.load(file)
            pincode_list = [(feature['properties']['PINCODE'],feature['properties']['PINCODE'])  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower())]
            self.fields['pincode'].choices += pincode_list

        if pincode:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.gram_panchayat_geojson.open('r') as file:
                geojson_data = json.load(file)
            gram_panchayat_list = [(feature['properties']['GP_NAME'],feature['properties']['GP_NAME'])  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower()) and (feature['properties']['PINCODE'].lower()==pincode.lower())]
            self.fields['gram_panchayat'].choices += gram_panchayat_list

        if gram_panchayat:
            geojson = Geojson.objects.filter(state_name=state).first()
            with geojson.town_village_geojson.open('r') as file:
                geojson_data = json.load(file)
            town_village_list = [(feature['properties']['NAME'],feature['properties']['NAME'])  for feature in geojson_data['features'] if (feature['properties']['STATE_NAME'].lower()==state.lower()) and (feature['properties']['DIST_NAME'].lower()==district.lower()) and (feature['properties']['SUB_DIST_N'].lower()==sub_district.lower()) and (feature['properties']['BLOCK_NAME'].lower()==block.lower()) and (feature['properties']['PINCODE'].lower()==pincode.lower()) and (feature['properties']['GP_NAME'].lower()==gram_panchayat.lower())]
            self.fields['town_village'].choices += town_village_list

        

        if last_nonempty_field:
            field_boundaries = {
                'state':['State Boundary','District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                'district':['District Boundary','Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                'sub_district':['Sub-District Boundary','Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                'block':['Block Boundary','Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                'pincode':['Pincode Boundary','Grampanchayat Boundary','Town/Village Boundary'],
                'gram_panchayat':['Grampanchayat Boundary','Town/Village Boundary'],
                'town_village':['Town/Village Boundary']
            }

            boundary_list = [(boundary_name,boundary_name)  for boundary_name in field_boundaries[last_nonempty_field]]
            self.fields['boundary'].choices += boundary_list



class ColorRangeFamilyForm(forms.ModelForm):
    class Meta:
        model = ColorRangeFamily
        fields = ['family_name']
        widgets = {
            'family_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter family name',
                'id': 'family-name-input'
            }),
        }
        labels = {
            'family_name': 'Family Name',
        }



class ColorRangeForm(forms.ModelForm):
    class Meta:
        model = ColorRange
        fields = ['start', 'end', 'color']  # Include all required fields

        # Define widgets for fields
        widgets = {
            'start': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter start value',
                'id': 'start-input'
            }),
            'end': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter end value',
                'id': 'end-input'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control',
                'id': 'color-input'
            }),
        }

        # Define labels for fields
        labels = {
            'start': 'Start Range',
            'end': 'End Range',
            'color': 'Pick a Color',
        }


    # Validation logic remains unchanged
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end and start >= end:
            raise forms.ValidationError("The 'start' value must be less than the 'end' value.")

        return cleaned_data

