from django.urls import path
from dna_app.views import plot_dna, dna_input

urlpatterns = [
    path('plot/', plot_dna, name='plot_dna'),
    path('', dna_input, name='dna_input'),  # Add this line
]
