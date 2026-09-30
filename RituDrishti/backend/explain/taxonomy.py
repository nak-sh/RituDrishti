"""Curated driver taxonomy. Values are dimensionless synthetic proxies."""
DRIVERS = [
 ('ENS_SPREAD_HIGH','spread',.55,'Ensemble spread','एन्सेम्बल फैलाव','Members diverge as forecast uncertainty grows.','पूर्वानुमान की अनिश्चितता बढ़ने पर सदस्यों में अंतर बढ़ता है।'),
 ('FLIPFLOP_HIGH','flipflop',.45,'Cycle-to-cycle instability','चक्रों में अस्थिरता','Successive forecast cycles change the expected outcome.','लगातार पूर्वानुमान चक्र अपेक्षित परिणाम बदल रहे हैं।'),
 ('PADI_HIGH','padi',.5,'Physics–AI disagreement','भौतिकी–AI में मतभेद','The independent AI witness departs from the physics forecast.','स्वतंत्र AI संकेत भौतिक पूर्वानुमान से अलग है।'),
 ('EFI_HIGH','efi',.6,'Unusual forecast extremity','असामान्य तीव्रता','The forecast approaches the tail of its synthetic model climate.','पूर्वानुमान कृत्रिम मॉडल जलवायु की चरम सीमा के निकट है।'),
 ('ENS_TRACK_SPLIT','bimodality',.4,'Split ensemble scenarios','विभाजित एन्सेम्बल परिदृश्य','A bimodality proxy suggests competing circulation scenarios.','द्विशिखरी संकेत अलग-अलग परिसंचरण परिदृश्य दर्शाता है।'),
 ('JET_PV_UNCERTAIN','jet',.7,'Jet / PV uncertainty','जेट / PV अनिश्चितता','Upper-level circulation may amplify downstream errors.','ऊपरी वायुमंडलीय परिसंचरण आगे त्रुटियां बढ़ा सकता है।'),
 ('OROGRAPHIC_IVT_HIGH','moisture',.6,'Elevated moisture transport','उच्च नमी परिवहन','Strong moisture transport increases sensitivity to terrain.','तेज नमी परिवहन भूभाग के प्रति संवेदनशीलता बढ़ाता है।'),
 ('RAPID_ERROR_GROWTH','growth',.5,'Rapid error growth','तेजी से बढ़ती त्रुटि','Small initial differences can grow quickly at this lead.','इस अवधि में छोटे प्रारंभिक अंतर तेजी से बढ़ सकते हैं।'),
 ('BSISO_PHASE_HARD','hard_regime',.5,'Difficult BSISO regime','कठिन BSISO चरण','The current intraseasonal phase is difficult in this archive.','इस संग्रह में वर्तमान अंतर्मौसमी चरण कठिन है।'),
 ('RECENT_SKILL_LOSS','memory',.5,'Recent skill deterioration','हालिया कौशल में गिरावट','Recently verified errors signal persistent model weakness.','हाल में सत्यापित त्रुटियां मॉडल की कमजोरी दर्शाती हैं।'),
 ('OROGRAPHY_SENSITIVE','orography',.6,'Terrain sensitivity','भूभाग संवेदनशीलता','Steep terrain makes displacement errors consequential.','तीखा भूभाग स्थानांतरण की त्रुटियों को महत्वपूर्ण बनाता है।'),
 ('COASTAL_CONTRAST','land_sea',.5,'Land–sea contrast','स्थल–समुद्र अंतर','Coastal gradients complicate convection placement.','तटीय अंतर संवहन की स्थिति को जटिल बनाता है।'),
 ('LONG_LEAD','lead',5,'Long-range uncertainty','लंबी अवधि की अनिश्चितता','Forecast uncertainty accumulates with lead time.','पूर्वानुमान अवधि के साथ अनिश्चितता बढ़ती है।'),
 ('REGIONAL_SENSITIVITY','region_id',5,'Regional model sensitivity','क्षेत्रीय मॉडल संवेदनशीलता','Regional error patterns differ within the synthetic archive.','कृत्रिम संग्रह में क्षेत्रीय त्रुटियों के पैटर्न अलग हैं।'),
 ('MODEL_VERSION_SHIFT','model_version',.5,'Model-version shift','मॉडल संस्करण परिवर्तन','A simulated model upgrade changes error behaviour.','अनुकरणीय मॉडल उन्नयन त्रुटि व्यवहार बदलता है।'),
 ('LOW_SPREAD_OVERCONFIDENCE','underdispersion',.5,'Under-dispersive ensemble','अल्प फैलाव वाला एन्सेम्बल','Low spread coexists with independent disagreement.','कम फैलाव के साथ स्वतंत्र मतभेद मौजूद है।'),
 ('WD_MONSOON_INTERACTION','wd_interaction',.3,'Western disturbance–monsoon interaction','पश्चिमी विक्षोभ–मानसून अंतःक्रिया','Moisture and upper-level forcing interact near the Himalaya.','हिमालय के पास नमी और ऊपरी वायुमंडलीय बल मिलते हैं।'),
 ('RIDGE_PERSISTENCE_UNCERTAIN','ridge',.7,'Uncertain ridge persistence','रिज स्थायित्व में अनिश्चितता','Ridge persistence affects heat-wave duration.','रिज का स्थायित्व लू की अवधि को प्रभावित करता है।'),
 ('SOIL_MOISTURE_BIAS','soil',.7,'Soil-moisture sensitivity','मिट्टी की नमी संवेदनशीलता','Surface moisture changes sensible heating and Tmax.','सतही नमी ताप और अधिकतम तापमान बदलती है।'),
 ('XMODEL_VORTEX_DISAGREE','shear',.7,'Vortex / shear sensitivity','भंवर / पवन कर्तन संवेदनशीलता','A shear proxy flags sensitivity of the circulation track.','पवन कर्तन संकेत परिसंचरण मार्ग की संवेदनशीलता दर्शाता है।'),
]
BY_FEATURE={d[1]:d for d in DRIVERS}