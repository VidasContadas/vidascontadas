from cicu.widgets import CicuUploaderInput
from django import forms
from models import Imagen, Comercio, Local, Pagina, Propuesta
from geoposition.forms import GeopositionField

class ComercioForm(forms.ModelForm):

   class Meta:
        model = Comercio
        exclude = ['date_created','date_modified','date_removed','deleted','administradores','slug']

        cicuOptions = {
            'ratioWidth': '950',       #fix-width ratio, default 0
            'ratioHeight':'450',       #fix-height ratio , default 0
            'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
        }
        widgets = {
            'imagen': CicuUploaderInput(options=cicuOptions)
        }

class ImagenCrop(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen','visible']

        cicuOptions = {
            'ratioWidth': '460',       #fix-width ratio, default 0
            'ratioHeight':'590',       #fix-height ratio , default 0
            'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
        }
        widgets = {
            'imagen': CicuUploaderInput(options=cicuOptions)
        }

class ComercioLocal(forms.ModelForm):
    localizacion = GeopositionField(initial='42.813127326939224,-1.6393232345581055')
    class Meta:
        model = Local
        exclude = ['comercio',]

class ComercioPropuesta(forms.ModelForm):
    class Meta:
        model = Propuesta
        fields = ['titulo', 'imagen', 'presentacion', 'visible']

        cicuOptions = {
            'ratioWidth': '460',       #fix-width ratio, default 0
            'ratioHeight':'590',       #fix-height ratio , default 0
            'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
        }
        widgets = {
            'imagen': CicuUploaderInput(options=cicuOptions)
        }

class ComercioPagina(forms.ModelForm):
    class Meta:
        model = Pagina
        exclude = ['comercio',]        