import fitz, requests, sys

def extract(url, name):
    try:
        if url.startswith('http'):
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                print(f'Failed to download {name}: HTTP {r.status_code}')
                return
            doc = fitz.open(stream=r.content, filetype='pdf')
        else:
            doc = fitz.open(url)
        text = ''
        for i in range(min(15, doc.page_count)):
            text += doc[i].get_text('text') + '
'
        with open(f'{name}.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Extracted {name}')
    except Exception as e:
        print(f'Error {name}: {e}')

extract('https://nsdcindia.org/sites/default/files/AGRQ1108_Tractor%20Mechanic_v1_28.05.2018.pdf', 'tractor')
# For ELE/Q3115, the link is a node page, let me search for the PDF link directly.
# For now I will download it later.
extract('https://www.nqr.gov.in/public/qualification/file/QFile-Dairy%20Product%20Processor.pdf', 'dairy')
