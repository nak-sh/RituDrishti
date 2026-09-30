import {useEffect,useMemo,useState} from 'react';
import {geoMercator,geoPath,geoTransform} from 'd3-geo';

export const fciColor=(v:number)=>v>=80?'#5eb9a0':v>=65?'#e2c463':v>=45?'#eaa06f':'#d97575';
export const IndiaMap=({regions=[],day=1,onSelect=()=>{},horizon=false}:any)=>{
 const [geo,setGeo]=useState<any>(null),[error,setError]=useState(false),[hover,setHover]=useState('');
 useEffect(()=>{fetch('/data/india.geojson').then(r=>r.json()).then(setGeo).catch(()=>setError(true))},[]);
 const projection=useMemo(()=>geoMercator().center([82,23]).scale(690).translate([300,263]),[]);
 const path=geoPath(geoTransform({point(x,y){const p=projection([x,y])!;this.stream.point(p[0],p[1])}}));
 const getRegion=(id:string)=>regions.find((r:any)=>r.id===id);
 const value=(id:string)=>getRegion(id)?.leads?.[day-1]?.fci;
 const selected=regions.find((r:any)=>r.id===hover);
 const activate=(id:string)=>{if(getRegion(id))onSelect(id,day)};
 const seas=[{id:'arabian',coords:[[68.5,12],[71.5,12],[72.5,18],[69,18],[68.5,12]]},{id:'bay',coords:[[86,17],[90,17],[90,21],[86,21],[86,17]]}];
 return <div className="map-wrap" data-testid="india-map">
 {error?<p role="alert" data-testid="map-error">Bundled map could not be loaded. Please refresh.</p>:!geo?<div className="skeleton map-skeleton" data-testid="map-loading"/>:<svg viewBox="0 0 600 575" role="img" aria-label="India forecast confidence, government boundary source">
 <defs><pattern id="ocean-grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M 28 0 L 0 0 0 28" fill="none" stroke="currentColor" strokeWidth=".3" opacity=".2"/></pattern></defs>
 <rect width="600" height="575" fill="url(#ocean-grid)"/>
 {seas.map(s=><path key={s.id} data-testid={`map-region-${s.id}`} d={path({type:'Polygon',coordinates:[s.coords.slice().reverse()]} as any)||''} fill={fciColor(value(s.id)??90)} fillOpacity=".25" stroke={fciColor(value(s.id)??90)} strokeDasharray="4 4" tabIndex={0} role="button" aria-label={getRegion(s.id)?.name||s.id} onClick={()=>activate(s.id)} onKeyDown={e=>e.key==='Enter'&&activate(s.id)}/>) }
 {geo.features.map((f:any,i:number)=><path key={i} data-testid={`map-state-${i}`} d={path(f)||''} fill={value(f.properties.region)===undefined?'#bed8d1':fciColor(value(f.properties.region))} stroke="var(--surface)" strokeWidth=".85" className={hover===f.properties.region?'map-state hovered':'map-state'} tabIndex={0} role="button" aria-label={`${f.properties.name}, ${Math.round(value(f.properties.region)??0)} confidence`} onMouseEnter={()=>setHover(f.properties.region)} onMouseLeave={()=>setHover('')} onFocus={()=>setHover(f.properties.region)} onBlur={()=>setHover('')} onClick={()=>activate(f.properties.region)} onKeyDown={e=>(e.key==='Enter'||e.key===' ')&&activate(f.properties.region)}><title>{f.properties.name} · {value(f.properties.region)??'—'} FCI</title></path>)}
 {[[74,33.6,'JAMMU & KASHMIR'],[78,35.7,'LADAKH'],[74.3,26.6,'RAJASTHAN'],[71.9,22.5,'GUJARAT'],[78.8,23.1,'MADHYA PRADESH'],[80.7,27.6,'UTTAR PRADESH'],[84.9,25.6,'BIHAR'],[75.8,18.9,'MAHARASHTRA'],[77,14.3,'KARNATAKA'],[79,10.2,'TAMIL NADU'],[95.3,28.2,'ARUNACHAL PRADESH'],[84.2,20.8,'ODISHA']].map(([x,y,t]:any)=>{const p=projection([x,y])!;return <text key={t} x={p[0]} y={p[1]} className="state-label" textAnchor="middle">{t}</text>})}
 <text x="98" y="345" className="sea-label">ARABIAN</text><text x="114" y="360" className="sea-label">SEA</text><text x="420" y="340" className="sea-label">BAY OF</text><text x="420" y="355" className="sea-label">BENGAL</text><text x="273" y="550" className="sea-label">INDIAN OCEAN</text>
 <g transform="translate(555 45)" className="north-arrow"><path d="M0 24 L0 0 L-4 9 M0 0 L4 9" fill="none" stroke="currentColor"/><text x="0" y="-8" textAnchor="middle">N</text></g>
 {horizon&&regions.map((r:any,i:number)=>{const xy=[[76,32],[74,28],[81,26],[78,23],[71,22],[74,19],[77,15],[76,10],[81,17],[94,26],[88,19],[70,15]][i];const p=projection(xy as [number,number])!;return <g key={r.id} transform={`translate(${p[0]},${p[1]})`} pointerEvents="none"><circle r="14" fill="#0b2545"/><text y="4" fill="white" textAnchor="middle" fontSize="11">{r.trust_horizon_day??'10+'}</text></g>})}
 </svg>}
 <div className="map-readout" data-testid="map-readout">{selected?<><span>{selected.name}</span><strong>{horizon?`Day ${selected.trust_horizon_day??'10+'}`:`${Math.round(value(hover))} FCI`}</strong></>:<><span>INDIA · 12 FORECAST REGIONS</span><strong>{horizon?'Trust horizon':'Forecast confidence'}</strong></>}</div>
 </div>
};