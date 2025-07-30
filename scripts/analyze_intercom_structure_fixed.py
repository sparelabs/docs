#!/usr/bin/env python3
import json
import os

def main():
    # Load articles
    articles = []
    current_json = ""
    brace_count = 0
    
    with open('/Users/joshandrews/Spare/docs/intercom-all-articles.json', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            current_json += line
            brace_count += line.count('{') - line.count('}')
            
            if brace_count == 0 and current_json:
                try:
                    article = json.loads(current_json)
                    articles.append(article)
                    current_json = ""
                except json.JSONDecodeError:
                    pass
                    
    # Load collections
    with open('/Users/joshandrews/Spare/docs/intercom-collections.json', 'r') as f:
        collections_data = json.load(f)

    collections = {str(c['id']): c['name'] for c in collections_data['data']}

    print(f'Total articles found: {len(articles)}')
    print()

    # Group by parent_ids (collections)
    by_collection = {}
    published_count = 0
    
    for article in articles:
        if isinstance(article, dict) and article.get('state') == 'published':  # Only published articles
            published_count += 1
            parent_ids = article.get('parent_ids', [])
            for parent_id in parent_ids:
                parent_name = collections.get(str(parent_id), f'Unknown Collection {parent_id}')
                if parent_name not in by_collection:
                    by_collection[parent_name] = []
                by_collection[parent_name].append({
                    'id': article['id'],
                    'title': article['title'],
                    'url': article.get('url', ''),
                    'created_at': article['created_at'],
                    'updated_at': article['updated_at']
                })

    print(f'Published articles: {published_count}')
    print()

    # Print structure
    for collection_name in sorted(by_collection.keys()):
        if collection_name not in ['OLD DO NOT USE', 'Untitled collection', 'Example collection']:
            print(f'## {collection_name} ({len(by_collection[collection_name])} articles)')
            for article in sorted(by_collection[collection_name], key=lambda x: x['title']):
                print(f'  - {article["title"]}')
            print()

    # Write detailed mapping to file
    with open('/Users/joshandrews/Spare/docs/intercom-structure-mapping.json', 'w') as f:
        json.dump(by_collection, f, indent=2)

    print("Detailed mapping saved to intercom-structure-mapping.json")

if __name__ == "__main__":
    main()