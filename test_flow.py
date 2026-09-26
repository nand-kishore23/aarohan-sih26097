import urllib.request, json, time

API = 'http://localhost:8000/api'

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    return json.loads(res.read())

def get(url):
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    return json.loads(res.read())

print('1. Interview')
res1 = post(f'{API}/demo/interview', {'text': 'Main tractor aur pump repair karta hoon, papa ke saath kaam karta hoon. Chhoti-moti machine repair kar leta hoon, lekin certificate nahi hai.', 'demo_mode': True})
ben_id = res1['beneficiary']['id']
print('Beneficiary ID:', ben_id)
print('Skills:', [s['normalized_skill'] for s in res1['skills']])

print('\n2. Profile')
res2 = get(f'{API}/beneficiaries/{ben_id}')
print('Profile fetched:', res2['name'])

print('\n3. Recommend Pathways')
res3 = post(f'{API}/pathways/recommend', {'beneficiary_id': ben_id})
print('Candidates:', len(res3['pathways']))
pathway_id = res3['pathways'][0]['id']
print('Top pathway ID:', pathway_id)
print('Top pathway name:', res3['pathways'][0]['pathway_name'])

print('\n4. Pathway Detail')
res4 = get(f'{API}/pathways/{pathway_id}')
print('Gaps:', len(res4['candidate']['skill_gaps']))

print('\n5. Human Decision')
res5 = post(f'{API}/pathways/{pathway_id}/decision', {'decision': 'interested', 'notes': 'Looks good'})
print('Decision recorded:', res5['decision'])
