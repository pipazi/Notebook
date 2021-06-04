# -*- coding: utf-8 -*-
"""
Created on 2021/6/3 16:01

@author: sun shaowen
"""
import math
import s2sphere

earthCircumferenceMeters = 1000 * 40075.017
MAX_S2_CELLS = 10000


def earthMetersToRadians(meters):
    return (2 * math.pi) * (float(meters) / earthCircumferenceMeters)


def getCircleCoveringRect(lat, lng, radius, parent_level):
    radius_radians = earthMetersToRadians(radius)
    latlng = s2sphere.LatLng.from_degrees(float(lat), float(lng)).normalized().to_point()
    region = s2sphere.Cap.from_axis_height(latlng, (radius_radians * radius_radians) / 2)
    coverer = s2sphere.RegionCoverer()
    coverer.min_level = int(parent_level)
    coverer.max_level = int(parent_level)
    coverer.max_cells = MAX_S2_CELLS
    covering = coverer.get_covering(region)
    s2_rect = []
    for cell_id in covering:
        new_cell = s2sphere.Cell(cell_id)
        vertices = []
        for i in range(4):
            vertex = new_cell.get_vertex(i)
            latlng = s2sphere.LatLng.from_point(vertex)
            vertices.append((math.degrees(latlng.lat().radians), math.degrees(latlng.lng().radians)))
        s2_rect.append(vertices)
    return s2_rect


def getRectCoveringRect(max_lon, min_lon, max_lat, min_lat):
    r = s2sphere.RegionCoverer()
    p1 = s2sphere.LatLng.from_degrees(min_lat, min_lon)
    p2 = s2sphere.LatLng.from_degrees(max_lat, max_lon)
    cell_ids = r.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))
    return cell_ids


# import s2sphere
# lat = 52.809766
# lng = -2.088996
# print(
#     s2sphere.CellId.from_lat_lng(s2sphere.LatLng.from_degrees(lat, lng)),
#     s2sphere.CellId.from_lat_lng(s2sphere.LatLng.from_degrees(lat, lng)).parent(30)
# )
