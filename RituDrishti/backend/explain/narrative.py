import re

def narrative(data, lang='en'):
    if lang=='hi':
        text=f"{data['region']} में दिन {data['day']} का विश्वास सूचकांक {data['fci']} है। निर्णय बदलने वाली त्रुटि की अनुमानित संभावना {data['risk']}% है। प्रमुख संकेत: {data['driver']}। यह कृत्रिम परिदृश्य है, वास्तविक मौसम चेतावनी नहीं।"
    else:
        text=f"For {data['region']} on Day {data['day']}, forecast confidence is {data['fci']}. The calibrated probability of a decision-changing error is {data['risk']}%. The leading signal is {data['driver']}. This is a synthetic scenario, not an operational weather warning."
    expected=[str(data['day']),str(data['fci']),str(data['risk'])]
    actual=re.findall(r'\d+(?:\.\d+)?',text)
    # Region and driver labels contain no numeric tokens. Equality includes order and multiplicity.
    valid=actual==expected
    if not valid: raise ValueError('Narrative numeric grounding failed')
    return {'text':text,'source':data,'number_consistency_passed':valid}