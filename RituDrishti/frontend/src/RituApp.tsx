import {useEffect,useState} from 'react';
import {BrowserRouter,Routes,Route} from 'react-router-dom';
import {Shell} from './components/Shell';
import {Toaster} from './components/ui/sonner';
import {useApi,query} from './lib/api';
import './lib/i18n';
import Dashboard from './pages/Dashboard';
import Analogues from './pages/Analogues';
import Reliability from './pages/Reliability';
import Cases from './pages/Cases';
import Decision from './pages/Decision';
import Feedback from './pages/Feedback';
import Architecture from './pages/Architecture';
import About from './pages/About';
import {ExplanationDrawer} from './components/ExplanationDrawer';
import {PageHeading} from './components/Common';
const ProgressPage=()=> <PageHeading eyebrow="EVIDENCE WORKSPACE" title="Evidence processing" description="This milestone is being connected to the forecast engine."/>;
export default function RituApp(){
const [init,setInit]=useState(''),[day,setDay]=useState(5),[hazard,setHazard]=useState('auto'),[selection,setSelection]=useState<any>(null),[dark,setDark]=useState(localStorage.getItem('ritu-dark')==='true');
const feed=useApi('/v1/confidence?'+query({init:init||undefined,hazard}));
useEffect(()=>{if(feed.data&&!init)setInit(feed.data.init)},[feed.data,init]);
useEffect(()=>{document.documentElement.classList.toggle('dark',dark);localStorage.setItem('ritu-dark',String(dark))},[dark]);
return <BrowserRouter><Shell {...{init,setInit,dark,setDark}} initTimes={feed.data?.init_times||[]}><Routes><Route path="/" element={<Dashboard feed={feed} {...{day,setDay,hazard,setHazard}} onSelect={(region:string,lead:number)=>setSelection({region,lead})}/>}/><Route path="/analogues" element={<Analogues init={init} regions={feed.data?.regions||[]}/>}/><Route path="/reliability" element={<Reliability/>}/><Route path="/cases" element={<Cases/>}/><Route path="/decision" element={<Decision init={init} onSelect={(region:string,lead:number)=>setSelection({region,lead})}/>}/><Route path="/feedback" element={<Feedback init={init}/>}/><Route path="/architecture" element={<Architecture/>}/><Route path="/about" element={<About/>}/><Route path="*" element={<PageHeading eyebrow="404" title="This view could not be found." description="Choose a workspace from the navigation."/>}/></Routes><ExplanationDrawer selection={selection} onClose={()=>setSelection(null)} init={init} hazard={hazard}/></Shell><Toaster position="bottom-right"/></BrowserRouter>
}