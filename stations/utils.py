
def create_point(long, lat):
    keyword: str = "Point"
    sep: str = ';'

    return f"{keyword}{sep}{long},{lat}"

def get_geojson_point(value: str):
    point = value.split(';')
    long_lat = point[1].split(',')
    return {
        'type': point[0].strip() ,
        'coordinate' : [float(long_lat[0]), float(long_lat[1])]
    }