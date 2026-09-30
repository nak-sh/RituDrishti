import os,uuid,secrets,asyncio
from datetime import datetime,timezone
from typing import Literal
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI,APIRouter,HTTPException,Query,BackgroundTasks,Request
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from fastapi.middleware.cors import CORSMiddleware
from api.engine import Engine
from api.schemas import Confidence,Explanation,Hazard,FeedbackInput,Feedback
from api.verification import build_verification,summarise
from api.cases import build_cases
from api.decision import decision
from api.online import run_verification
from regions import REGIONS,INIT_TIMES

load_dotenv(Path(__file__).parent/'.env')
engine=None
client=AsyncIOMotorClient(os.environ['MONGO_URL'])
db=client[os.environ['DB_NAME']]
verification=None
case_data=None
online_lock=asyncio.Lock()
@asynccontextmanager
async def lifespan(app):
    global engine,verification,case_data
    engine=Engine()
    verification=build_verification(engine)
    case_data=build_cases(engine)
    await db.verification_runs.create_index('id',unique=True)
    yield
    client.close()

app=FastAPI(title='RituDrishti · synthetic forecast assurance',version='0.2.0',lifespan=lifespan,docs_url='/api/docs',openapi_url='/api/openapi.json')
app.add_middleware(CORSMiddleware,allow_origins=os.environ['CORS_ORIGINS'].split(','),allow_methods=['GET','POST'],allow_headers=['*'])
router=APIRouter()

def validate(init,region=None):
    if init not in INIT_TIMES:raise HTTPException(422,'Choose an available synthetic initialisation')
    if region and region not in [r[0] for r in REGIONS]:raise HTTPException(404,'Unknown forecast region')

@router.get('/health')
def health(): return {'status':'ok' if engine else 'loading','data_mode':'synthetic','model_loaded':engine is not None}

@router.get('/v1/confidence',response_model=Confidence)
def confidence(init:str=INIT_TIMES[0],hazard:Hazard='auto',region:str|None=None):
    validate(init,region);return engine.confidence(init,hazard,region)

@router.get('/v1/hotspots')
def hotspots(init:str=INIT_TIMES[0],min_prob:float=Query(.35,ge=0,le=1),hazard:Hazard='auto'):
    validate(init);return {'hotspots':engine.hotspots(init,min_prob,hazard),'data_mode':'synthetic'}

@router.get('/v1/bust-probability')
def probability(init:str=INIT_TIMES[0],hazard:Hazard='auto',lead:int=Query(1,ge=1,le=10)):
    validate(init);return engine.geojson(init,hazard,lead)

@router.get('/v1/explain',response_model=Explanation)
def explain(region:str,lead:int=Query(1,ge=1,le=10),lang:str=Query('en',pattern='^(en|hi)$'),init:str=INIT_TIMES[0],hazard:Hazard='auto'):
    validate(init,region);return engine.explain(region,lead,lang,init,hazard)

@router.get('/v1/analogs')
def analogs(region:str,lead:int=Query(1,ge=1,le=10),k:int=Query(5,ge=1,le=10),init:str=INIT_TIMES[0],hazard:Hazard='auto'):
    validate(init,region);d=engine.row(region,lead,init,hazard);m=engine.systems[int(d.iloc[0].hazard_id)]
    return {'analogs':m.analogs(d,k),'region':region,'data_mode':'synthetic'}

app.include_router(router,prefix='/api')
app.include_router(router,include_in_schema=False)

extra=APIRouter()
@extra.get('/v1/verification')
def verification_endpoint(period:Literal['all','2023','2024']='all'):
    if period=='all':return verification
    return summarise(engine,engine.evaluation[engine.evaluation.date.dt.year==int(period)])

@extra.get('/v1/cases')
def cases(): return {'cases':case_data,'data_mode':'synthetic'}

@extra.get('/v1/decision')
def decisions(cost_loss:float=Query(.15,gt=0,lt=1),init:str=INIT_TIMES[0]):
    validate(init);return decision(engine,cost_loss,init)

@extra.post('/v1/feedback',response_model=Feedback)
async def feedback(body:FeedbackInput):
    validate(body.init,body.region)
    if body.hazard not in ['rain','heat','cyclone']:raise HTTPException(422,'Choose a specific hazard')
    record=Feedback(**body.model_dump(),id=str(uuid.uuid4()),created_at=datetime.now(timezone.utc).isoformat())
    await db.feedback.insert_one(record.model_dump())
    return record

@extra.get('/v1/feedback',response_model=list[Feedback])
async def feedback_queue(): return await db.feedback.find({},{'_id':0}).sort('created_at',-1).to_list(200)

@extra.get('/v1/verification-runs')
async def runs():return {'runs':await db.verification_runs.find({},{'_id':0}).sort('created_at',-1).to_list(30)}

async def locked_verification(run_id):
    async with online_lock: await run_verification(engine,db,run_id)

@extra.post('/cron/verify')
async def cron_verify(request:Request,tasks:BackgroundTasks):
    # Cron endpoints must ack 2xx immediately; enqueue/background the actual work.
    expected=os.environ.get('WEBHOOK_CRON_SECRET')
    supplied=request.headers.get('authorization','')
    if not expected or not secrets.compare_digest(supplied,'Bearer '+expected):raise HTTPException(401,'Invalid scheduler credentials')
    try:body=await request.json()
    except Exception:raise HTTPException(400,'Invalid JSON envelope')
    if not isinstance(body,dict) or body.get('event')!='schedule.triggered' or not body.get('run_id'):raise HTTPException(400,'Invalid schedule envelope')
    run_id=request.headers.get('x-webhook-id') or body['run_id']
    try:await db.verification_runs.insert_one({'id':run_id,'status':'queued','created_at':datetime.now(timezone.utc).isoformat()})
    except DuplicateKeyError:return {'accepted':True,'duplicate':True}
    tasks.add_task(locked_verification,run_id)
    return {'accepted':True,'run_id':run_id}

app.include_router(extra,prefix='/api')
app.include_router(extra,include_in_schema=False)
@app.get('/docs',include_in_schema=False)
def docs_redirect():return RedirectResponse('/api/docs')