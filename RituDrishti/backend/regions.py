REGIONS = [
    ('western-himalaya', 'Western Himalaya', 'पश्चिमी हिमालय', ['Jammu & Kashmir','Ladakh','Himachal Pradesh','Uttarakhand']),
    ('northwest', 'Northwest India', 'उत्तर-पश्चिम भारत', ['Punjab','Haryana','Rajasthan','Delhi','Chandigarh']),
    ('gangetic', 'Indo-Gangetic Plain', 'गंगा का मैदान', ['Uttar Pradesh','Bihar','West Bengal']),
    ('central', 'Central India', 'मध्य भारत', ['Madhya Pradesh','Chhattisgarh','Jharkhand']),
    ('gujarat', 'Gujarat & Saurashtra', 'गुजरात और सौराष्ट्र', ['Gujarat','Dadra,Nagar Haveli,Daman & Diu']),
    ('konkan', 'Konkan & Goa', 'कोंकण और गोवा', ['Maharashtra','Goa']),
    ('interior', 'Peninsular interior', 'प्रायद्वीपीय आंतरिक क्षेत्र', ['Karnataka','Telangana']),
    ('kerala', 'Kerala & Lakshadweep', 'केरल और लक्षद्वीप', ['Kerala','Lakshadweep']),
    ('east-coast', 'East coast', 'पूर्वी तट', ['Odisha','Andhra Pradesh','Tamil Nadu','Puducherry','Andaman & Nicobar']),
    ('northeast', 'Northeast India', 'पूर्वोत्तर भारत', ['Arunachal Pradesh','Assam','Manipur','Meghalaya','Mizoram','Nagaland','Sikkim','Tripura']),
    ('bay', 'North Bay of Bengal', 'उत्तरी बंगाल की खाड़ी', []),
    ('arabian', 'East Arabian Sea', 'पूर्वी अरब सागर', []),
]
HAZARDS = ['rain', 'heat', 'cyclone']
INIT_TIMES = ['2026-07-08T00:00:00Z', '2026-07-07T12:00:00Z', '2026-07-07T00:00:00Z']
DEMO = 'Demo data: synthetic, for illustration'

def region_dicts():
    return [dict(id=r[0], name=r[1], name_hi=r[2], states=r[3]) for r in REGIONS]