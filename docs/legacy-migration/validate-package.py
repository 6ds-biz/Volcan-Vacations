"""Validate the inert migration package. Reads JSON only; no network/DB/import code."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def validate():
    for path in ROOT.glob('*.json'):
        json.loads(path.read_text())
    inventory = read('legacy-tour-inventory.json')
    tours = inventory['tours']
    summary = read('audit-summary.json')
    staged = read('staged-import.json')
    media = read('legacy-media-inventory.json')['items']
    sources = read('source-manifest.json')
    questions = read('partner-verification.json')
    ids = {t['legacy_id'] for t in tours}
    media_ids = {m['id'] for m in media}
    source_urls = {r['url'] for r in sources['requests']}
    statuses = set(inventory['status_definitions'])
    assert len(ids) == len(tours) == 13
    assert len({t['legacy_url'] for t in tours}) == len(tours)
    assert len(media_ids) == len(media) == summary['media_sources']
    assert all(t['legacy_url'] in source_urls for t in tours)
    assert summary['named_tours'] == 12 and summary['transportation_products'] == 1
    assert summary['uploaded_videos'] == sum(m['media_type'] == 'video' and m['wordpress_id'] is not None for m in media) == 18
    assert summary['one_dollar_prices'] == sum(t['fields']['legacy_retail_price']['value'] == '1.00' for t in tours) == 10
    for t in tours:
        assert t['verification_status'] in statuses
        for f in t['fields'].values():
            assert f['verification_status'] in statuses
            assert not f['current_business_verified']
            if f['verification_status'] == 'MISSING':
                assert f['value'] == 'MISSING'
            else:
                assert f['provenance'], (t['legacy_id'], f)
                for p in f['provenance']:
                    assert p['url'] in source_urls and p['source_sha256'], p
        assert set(t['gallery_media_ids']).issubset(media_ids)
        assert set(t['all_page_media_ids']).issubset(media_ids)
        assert set(t['identical_description_legacy_ids']).issubset(ids)
        assert all(t['fields'][k]['verification_status'] == 'MISSING' for k in ['current_verified_retail_price', 'supplier_cost', 'vv_gross_margin'])
    assert staged['execution_allowed'] is False and staged['database_writes_performed'] is False
    assert staged['supplier_inserts'] == []
    assert len(staged['products']) == len(tours)
    assert {p['legacy_url'] for p in staged['products']} == {t['legacy_url'] for t in tours}
    dispositions = collections.Counter(p['disposition'] for p in staged['products'])
    assert {k: dispositions[k] for k in staged['disposition_counts']} == summary['product_staging'] == staged['disposition_counts']
    for p in staged['products']:
        draft = p['product_draft']
        assert p['import_allowed'] is False and p['media_import_allowed'] is False
        assert draft['active'] is False and draft['featured'] is False
        assert draft['supplier_id'] is None and draft['retail_price'] is None and draft['supplier_cost'] is None
        assert p['current_verified_retail_price'] is None and p['supplier_cost'] is None and p['vv_gross_margin'] is None
        assert p['product_images'] == [] and p['blocked_reasons'] and p['missing_required_import_fields']
        assert p['api_compatible_now'] is False
    assert len(questions['pricing_rows']) == questions['pricing_row_count'] == 13
    assert questions['question_prompt_count'] == len(questions['shared_questions']) + sum(len(t['questions']) for t in questions['tour_questions']) == summary['partner_question_prompts']
    assert dict(collections.Counter(m['migration_recommendation'] for m in media)) == summary['media_recommendations']
    assert all(m['rights_status'] == 'NEEDS_PARTNER_VERIFICATION' for m in media)
    assert all(m['migration_recommendation'] != 'KEEP' for m in media)
    assert all(set(m['exact_duplicate_ids']).issubset(media_ids) for m in media)
    redirects = read('legacy-url-redirect-map.json')
    assert len(redirects) == summary['public_content_urls_inspected'] == len(sources['pages'])
    assert len({r['old_url'] for r in redirects}) == len(redirects)
    assert all(r['implemented'] is False for r in redirects)
    assert all(not r['new_route_exists'] for r in redirects if r['page_classification'] == 'CATALOG_PRODUCT')
    assert read('legacy-contact-audit.json')['canonical_email'] == staged['public_contact']['email'] == 'info@volcanvacations.com'
    assert len(read('current-inventory-comparison.json')['six_seed_products']) == 6
    required = ['legacy-tour-inventory.md', 'partner-verification-list.md', 'legacy-media-inventory.md', 'legacy-copy-audit.md', 'legacy-url-redirect-map.md', 'migration-plan.md']
    assert all((ROOT / name).is_file() for name in required)
    print(json.dumps({'result': 'PASS', 'products': len(tours), 'media_sources': len(media), 'redirect_dispositions': len(redirects), 'all_products_inactive_and_blocked': True, 'database_or_network_access': False}))


if __name__ == '__main__':
    validate()
