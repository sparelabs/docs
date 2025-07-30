#!/usr/bin/env python3
import json
import html

def main():
    # Load sections
    sections = []
    current_json = ""
    brace_count = 0
    
    with open('/Users/joshandrews/Spare/docs/intercom-all-sections.json', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            current_json += line
            brace_count += line.count('{') - line.count('}')
            
            if brace_count == 0 and current_json:
                try:
                    section = json.loads(current_json)
                    sections.append(section)
                    current_json = ""
                except json.JSONDecodeError:
                    pass

    # Load collections
    with open('/Users/joshandrews/Spare/docs/intercom-collections.json', 'r') as f:
        collections_data = json.load(f)

    # Load current mapping
    with open('/Users/joshandrews/Spare/docs/intercom-backup/complete-mapping.json', 'r') as f:
        mapping_data = json.load(f)

    collections = {str(c['id']): c for c in collections_data['data']}
    sections_by_id = {str(s['id']): s for s in sections}

    print("# Resolved Collection Structure")
    print("=" * 50)
    print()

    # Create resolved mapping
    resolved_collections = {}
    
    for collection_name, articles in mapping_data['collections'].items():
        if collection_name.startswith('Unknown Collection '):
            # Extract the ID and try to resolve it
            collection_id = collection_name.replace('Unknown Collection ', '')
            
            if collection_id in sections_by_id:
                # This is actually a section, not a collection
                section = sections_by_id[collection_id]
                section_name = html.unescape(section['name'])
                parent_id = str(section.get('parent_id', ''))
                
                if parent_id in collections:
                    parent_collection = collections[parent_id]
                    full_name = f"{parent_collection['name']} - {section_name}"
                    resolved_collections[full_name] = {
                        'type': 'section',
                        'section_id': collection_id,
                        'section_name': section_name,
                        'parent_collection_id': parent_id,
                        'parent_collection_name': parent_collection['name'],
                        'articles': articles
                    }
                    print(f"✅ **{collection_name}** → **{full_name}**")
                    print(f"   Section: {section_name}")
                    print(f"   Parent Collection: {parent_collection['name']}")
                    print(f"   Articles: {len(articles)}")
                    print()
                else:
                    resolved_collections[collection_name] = {
                        'type': 'unknown_section',
                        'section_id': collection_id,
                        'section_name': section_name,
                        'parent_collection_id': parent_id,
                        'articles': articles
                    }
                    print(f"❓ **{collection_name}** → **{section_name}** (Unknown parent: {parent_id})")
                    print()
            else:
                # Keep as unknown
                resolved_collections[collection_name] = {
                    'type': 'unknown',
                    'articles': articles
                }
                print(f"❌ **{collection_name}** → Still unknown")
                print()
        else:
            # Known collection
            resolved_collections[collection_name] = {
                'type': 'collection',
                'articles': articles
            }

    print("## Proper Hierarchical Structure")
    print()

    # Group by parent collection
    by_parent = {}
    for name, data in resolved_collections.items():
        if data['type'] == 'section':
            parent = data['parent_collection_name']
            if parent not in by_parent:
                by_parent[parent] = []
            by_parent[parent].append({
                'section_name': data['section_name'],
                'full_name': name,
                'article_count': len(data['articles'])
            })
        elif data['type'] == 'collection':
            if name not in by_parent:
                by_parent[name] = []

    # Print the hierarchical structure
    for parent, sections in sorted(by_parent.items()):
        if sections:  # Has sections
            total_articles = sum(s['article_count'] for s in sections)
            print(f"### {parent} ({total_articles} total articles)")
            for section in sorted(sections, key=lambda x: x['section_name']):
                print(f"  - **{section['section_name']}** ({section['article_count']} articles)")
            print()
        else:  # Direct collection
            if parent in resolved_collections:
                article_count = len(resolved_collections[parent]['articles'])
                print(f"### {parent} ({article_count} articles)")
                print("  (No subsections)")
                print()

    # Save the resolved mapping
    output = {
        'resolved_collections': resolved_collections,
        'hierarchical_structure': by_parent,
        'sections_metadata': sections_by_id,
        'collections_metadata': collections
    }

    with open('/Users/joshandrews/Spare/docs/intercom-backup/resolved-structure.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("## Recommended Mintlify Structure")
    print()
    
    # Suggest proper mintlify structure based on resolved hierarchy
    suggestions = {}
    
    for parent, sections in sorted(by_parent.items()):
        # Clean parent name for directory
        clean_parent = parent.lower().replace(' ', '-').replace(':', '').replace('&', 'and')
        clean_parent = clean_parent.replace('spare-', '').replace('operations-', '')
        
        if sections:
            suggestions[clean_parent] = {
                'parent_name': parent,
                'sections': {}
            }
            for section in sections:
                clean_section = section['section_name'].lower().replace(' ', '-').replace('&', 'and')
                clean_section = clean_section.replace('admins-', '').replace('booking-agents-', '').replace('dispatchers-', '')
                suggestions[clean_parent]['sections'][clean_section] = {
                    'section_name': section['section_name'],
                    'article_count': section['article_count']
                }
        else:
            if parent in resolved_collections:
                suggestions[clean_parent] = {
                    'parent_name': parent,
                    'article_count': len(resolved_collections[parent]['articles']),
                    'sections': {}
                }

    for dir_name, info in suggestions.items():
        if 'sections' in info and info['sections']:
            total = sum(s['article_count'] for s in info['sections'].values())
            print(f"**{dir_name}/** ← {info['parent_name']} ({total} articles)")
            for subdir, section_info in info['sections'].items():
                print(f"  **{subdir}/** ← {section_info['section_name']} ({section_info['article_count']} articles)")
        else:
            count = info.get('article_count', 0)
            print(f"**{dir_name}/** ← {info['parent_name']} ({count} articles)")
        print()

    with open('/Users/joshandrews/Spare/docs/intercom-backup/mintlify-structure-suggestions.json', 'w') as f:
        json.dump(suggestions, f, indent=2)

    print("✅ Resolved structure saved to: resolved-structure.json")
    print("✅ Mintlify suggestions saved to: mintlify-structure-suggestions.json")

if __name__ == "__main__":
    main()