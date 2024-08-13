# dna_app/forms.py
from django import forms

class DNAForm(forms.Form):
    dna1 = forms.CharField(label='DNA Sequence 1', max_length=100, required=True)
    dna2 = forms.CharField(label='DNA Sequence 2', max_length=100, required=True)
