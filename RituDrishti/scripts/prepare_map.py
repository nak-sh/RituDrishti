"""Bundle unaltered government geometries; no third-party basemap or tiles."""
import json, sys
from pathlib import Path
from shapely.geometry import shape, Point
from shapely.ops import unary_union
from shapely import make_valid
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from regions import REGIONS

def main():
    source=ROOT/'backend/data/india-government.geojson'
    j=json.loads(source.read_text())
    land=unary_union([make_valid(shape(f['geometry'])) for f in j['features']])
    probes={'Gilgit-Baltistan':[74.3,35.9],'PoK':[73.6,34.2],'Aksai Chin':[79.8,35.2],'Arunachal Pradesh':[95.5,28.4]}
    results={name:land.covers(Point(*xy)) for name,xy in probes.items()}
    if not all(results.values()): raise ValueError(f'Boundary coverage failed: {results}')
    for f in j['features']:
        name=f['properties']['STNAME']
        rid=next(r[0] for r in REGIONS if name in r[3])
        f['properties']={'name':name,'region':rid}
    (ROOT/'frontend/public/data/india.geojson').write_text(json.dumps(j,separators=(',',':')))
    metadata={'source':'NIC BharatMap, Government of India','url':'https://mapservice.gov.in/gismapservice/rest/services/BharatMapService/Admin_Boundary_District/MapServer/0','retrieved':'2026-09-30','state_ut_count':len(j['features']),'query_simplification_degrees':0.025,'coverage_probes':results,'extent':list(land.bounds),'notes':'Government-hosted source; international outline not edited. Metadata description is older than the returned geometry (which includes Ladakh). Probe checks and visual inspection are not Survey of India certification. Regional grouping is illustrative; all Maharashtra is grouped with Konkan, and islands with East Coast. Sea areas are illustrative forecast boxes, not maritime boundaries. TLS certificate-chain verification was unavailable in build environment; retrieval used a public government endpoint with that transport check disabled.'}
    (ROOT/'frontend/public/data/map-provenance.json').write_text(json.dumps(metadata,indent=2))
    print(json.dumps(metadata,indent=2))

if __name__=='__main__': main()