import csv
from comercios.models import Asociado, CategoriaComercio
from asociacion.models import Convenio, CategoriaConvenio

/home/serendipity/webapps/areacomercial_django/
with open('ensanche/datos/CONVENIOS/convenios.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        print row[1]        
        a = Convenio()
        a.name = row[1]
        a.descripcion = row[2]
        a.save()

with open('ensanche/datos/CONVENIOS/categorias.txt', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        print row[0].upper()
        c = CategoriaConvenio()
        c.name = row[0].upper()
        c.save()

import csv
from comercios.models import Asociado, CategoriaComercio
with open('ensanche/datos/asociados.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        print ', '.join(row)        
        a = Asociado()
        a.nombre = row[0]
        a.direccion = row[1]
        a.save()

with open('ensanche/datos/categorias.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        print row[0]
        c = CategoriaComercio()
        c.name = row[0]
        c.save()

import os
import filer.models as filer_models
from django.core.files import File as DjangoFile
from django.contrib.auth.models import User

usuario = User.objects.get(username='alabarga')

folder, created = filer_models.Folder.objects.get_or_create(name='convenios')

directory = '/home/serendipity/webapps/areacomercial_django/ensanche/datos/CONVENIOS/LOGOS/'

path = r"%s" % directory

for image_name in os.listdir(path):
    filename = os.path.join(path, image_name)
    print filename
    # filename = '/home/alabarga/Proyectos/ComercioPamplona/materiales/CONVENIOS/LOGOS/logo_2.jpg'
    # image_name = 'logo_2.png'
    logo_file = DjangoFile(open(filename, 'rb'), name=image_name)
    image = filer_models.Image.objects.create(owner=usuario,
                                              original_filename=image_name,
                                              file=logo_file)
    image.folder = folder
    image.save()        

      
directory = '/home/serendipity/webapps/areacomercial_django/ensanche/datos/CONVENIOS/DOCUMENTOS/'

path = r"%s" % directory

for doc_name in os.listdir(path):
    filename = os.path.join(path, doc_name)
    print filename
    # filename = '/home/alabarga/Proyectos/ComercioPamplona/materiales/CONVENIOS/LOGOS/logo_2.jpg'
    # image_name = 'logo_2.png'
    doc_file = DjangoFile(open(filename, 'rb'), name=doc_name)
    image = filer_models.File.objects.create(owner=usuario,
                                              original_filename=doc_name,
                                              file=doc_file)
    image.folder = folder
    image.save()        


with open('ensanche/datos/categorias.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        print row[0]
        c = CategoriaComercio()
        c.name = row[0]
        c.save() 

import csv
from unidecode import unidecode
from geopy.geocoders import GoogleV3

geolocator = GoogleV3()

carto_file = open('ensanche/datos/cartodb4.csv', 'wb', encoding="utf-8") 
output = csv.writer(carto_file, delimiter='\t')
output.writerow(['Nombre', 'Direccion', 'Latitud', 'Longitud'])
with open('ensanche/datos/mapa.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:        
        name = row[0]
        direccion = row[1]
        direccion = u'%s, Spain' % direccion.decode("utf-8")        
        print unidecode(direccion)
        try:
            address, (latitude, longitude) = geolocator.geocode(unidecode(direccion))
            print name, latitude, longitude, direccion
            output.writerow([name.decode("utf-8"), address.decode("utf-8"), latitude, longitude])
        except:
            print "FAILED:", name, direccion
            pass
carto_file.close()            


