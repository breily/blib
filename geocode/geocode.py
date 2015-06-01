import urllib

api = 'http://maps.google.com/maps/geo?%s'

def reverse_geocode(lat, long):
    params = urllib.urlencode(
        {'ll':','.join([str(lat), str(long)]), 'output':'csv'}
    )
    fp = urllib.urlopen(api % params)
    data = fp.read().split(',')
    ret = {}
    ret['status'] = data[0]
    ret['accuracy'] = data[1]
    ret['address'] = ','.join(data[2:])
    return ret

def geocode(address):
    params = urllib.urlencode({'q': address, 'output': 'csv'})
    fp = urllib.urlopen(api % params)
    data = fp.read().split(',')
    ret = {}
    ret['status'] = data[0]
    ret['accuracy'] = data[1]
    ret['latitude'] = data[2]
    ret['longitude'] = data[3]
    return ret
