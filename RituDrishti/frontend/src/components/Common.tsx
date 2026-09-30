import {AlertCircle,RefreshCw,FlaskConical,ArrowUpRight} from 'lucide-react';
import {useTranslation} from 'react-i18next';
import {Link} from 'react-router-dom';
import {Button} from './ui/button';
export const DemoBadge=({testId='demo-data-badge'}:{testId?:string})=>{const {t}=useTranslation();return <span className="demo-badge" data-testid={testId}><FlaskConical size={12}/>{t('demo')}</span>};
export const DataState=({loading,error,retry}:any)=>loading?<div className="loading-state" data-testid="loading-state"><div className="skeleton"/><div className="skeleton"/><div className="skeleton"/><span>Preparing computed forecast intelligence…</span></div>:error?<div className="error-state" role="alert" data-testid="error-state"><AlertCircle/><h2>We couldn’t load this view</h2><p>{error}</p><Button data-testid="retry-data" onClick={retry}><RefreshCw size={15}/>Try again</Button></div>:null;
export const PageHeading=({eyebrow,title,description,children}:any)=><div className="page-heading"><div><div className="eyebrow" data-testid="page-eyebrow">{eyebrow}</div><h1 data-testid="page-title">{title}</h1>{description&&<p data-testid="page-description">{description}</p>}</div>{children}</div>;
export const PanelTitle=({title,subtitle,children}:any)=><div className="panel-title"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div>{children}</div>;
export const TextLink=({to,children,testId}:any)=><Link className="text-link" to={to} data-testid={testId}>{children}<ArrowUpRight size={14}/></Link>;