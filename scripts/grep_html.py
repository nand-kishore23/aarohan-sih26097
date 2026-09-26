import os, re, sys

files = [
    'C:/Users/HP/.gemini/antigravity/brain/ed2366bb-f9ff-451c-8f53-11bb35721977/.system_generated/steps/135/content.md',
    'C:/Users/HP/.gemini/antigravity/brain/ed2366bb-f9ff-451c-8f53-11bb35721977/.system_generated/steps/156/content.md',
    'C:/Users/HP/.gemini/antigravity/brain/ed2366bb-f9ff-451c-8f53-11bb35721977/.system_generated/steps/157/content.md',
    'C:/Users/HP/.gemini/antigravity/brain/ed2366bb-f9ff-451c-8f53-11bb35721977/.system_generated/steps/158/content.md'
]

for f in files:
    if os.path.exists(f):
        print(f'--- File: {f} ---')
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            import bs4
            soup = bs4.BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            print('Snippet length:', len(text))
            # Search for AGR/Q1108
            if 'AGR' in text or 'Tractor' in text or 'ELE' in text or 'Dairy' in text:
                idx = text.find('Q1108')
                if idx != -1: print('Found Q1108 context:', text[max(0, idx-200):idx+500])
                idx = text.find('Q3115')
                if idx != -1: print('Found Q3115 context:', text[max(0, idx-200):idx+500])
