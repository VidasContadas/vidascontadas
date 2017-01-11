 # -*- coding: utf-8 -*-
import csv, codecs
from unidecode import unidecode
from geopy.geocoders import GoogleV3

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == "__main__":

    geolocator = GoogleV3()

    # carto_file = open('ensanche/datos/cartodb5.csv', 'wb') 
    # output = csv.writer(carto_file, delimiter='\t')
    # output.writerow(['Nombre', 'Dirección', 'Latitud', 'Longitud'])

    f = codecs.open('ensanche/datos/cartodb5.csv', 'wb')
    output = UnicodeWriter(f)

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
       
