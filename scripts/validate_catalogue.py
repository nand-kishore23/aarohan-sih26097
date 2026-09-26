import json
import sys

def validate():
    try:
        with open('data/normalized/qualification_catalogue.json', 'r', encoding='utf-8') as f:
            cat = json.load(f)
        assert cat.get('catalogue_version'), 'Missing catalogue_version'
        assert cat.get('status'), 'Missing status'
        for rec in cat.get('records', []):
            assert rec.get('qp_code'), 'Missing qp_code'
            assert 'nos' in rec, f'Missing nos list for {rec.get("qp_code")}'
            assert 'competencies' in rec, f'Missing competencies list for {rec.get("qp_code")}'
        print('Catalogue schema is valid.')
    except Exception as e:
        print(f'Validation failed: {e}')
        sys.exit(1)

if __name__ == '__main__':
    validate()
