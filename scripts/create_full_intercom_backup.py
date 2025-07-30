#!/usr/bin/env python3
import json
import os
import html
from pathlib import Path

def clean_filename(title):
    """Convert title to safe filename"""
    # Remove HTML entities and convert to lowercase
    cleaned = html.unescape(title)
    # Replace problematic characters
    cleaned = cleaned.replace('/', '-').replace(':', '-').replace('?', '').replace('!', '').replace("'", '').replace('"', '').replace('&', 'and')
    cleaned = cleaned.replace(' ', '-').replace('---', '-').replace('--', '-')
    # Remove leading/trailing dashes
    cleaned = cleaned.strip('-').lower()
    return cleaned

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

    collections = {str(c['id']): c for c in collections_data['data']}

    # Create backup directory
    backup_dir = Path('/Users/joshandrews/Spare/docs/intercom-backup')
    backup_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for each collection
    by_collection = {}
    published_count = 0
    
    for article in articles:
        if isinstance(article, dict) and article.get('state') == 'published':
            published_count += 1
            parent_ids = article.get('parent_ids', [])
            
            for parent_id in parent_ids:
                collection_info = collections.get(str(parent_id), {'name': f'Unknown Collection {parent_id}'})
                collection_name = collection_info['name']
                
                # Clean collection name for directory
                clean_collection = clean_filename(collection_name)
                collection_dir = backup_dir / clean_collection
                collection_dir.mkdir(exist_ok=True)
                
                # Save article content
                filename = clean_filename(article['title']) + '.json'
                article_path = collection_dir / filename
                
                # Add collection info to article
                article_with_meta = {
                    **article,
                    'collection_name': collection_name,
                    'collection_id': parent_id,
                    'collection_info': collection_info
                }
                
                with open(article_path, 'w') as f:
                    json.dump(article_with_meta, f, indent=2)
                
                # Track for mapping
                if collection_name not in by_collection:
                    by_collection[collection_name] = []
                by_collection[collection_name].append({
                    'id': article['id'],
                    'title': article['title'],
                    'url': article.get('url', ''),
                    'filename': filename,
                    'created_at': article['created_at'],
                    'updated_at': article['updated_at']
                })

    print(f'Backed up {published_count} articles to {backup_dir}')
    
    # Create comprehensive mapping file
    mapping = {
        'total_articles': published_count,
        'total_collections': len(by_collection),
        'collections': by_collection,
        'collection_metadata': {str(k): v for k, v in collections.items()}
    }
    
    with open(backup_dir / 'complete-mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2)
        
    # Create comparison with current Mintlify structure
    mintlify_files = []
    help_center_path = Path('/Users/joshandrews/Spare/docs/help-center')
    for mdx_file in help_center_path.rglob('*.mdx'):
        relative_path = mdx_file.relative_to(help_center_path)
        mintlify_files.append(str(relative_path))
    
    comparison = {
        'intercom_articles': published_count,
        'mintlify_files': len(mintlify_files),
        'missing_in_mintlify': published_count - len(mintlify_files),
        'mintlify_structure': mintlify_files
    }
    
    with open(backup_dir / 'mintlify-comparison.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f'Created comprehensive mapping and comparison files')
    print(f'Intercom: {published_count} articles')
    print(f'Mintlify: {len(mintlify_files)} files')
    print(f'Missing: {published_count - len(mintlify_files)} articles')

if __name__ == "__main__":
    main()