#!/usr/bin/env python3
import json
import os
import shutil
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

def clean_folder_name(name):
    """Convert name to safe folder name"""
    # Remove HTML entities
    cleaned = html.unescape(name)
    # Replace problematic characters for folders
    cleaned = cleaned.replace('/', '-').replace(':', '').replace('?', '').replace('!', '').replace("'", '').replace('"', '')
    cleaned = cleaned.replace('&', 'and').replace('  ', ' ').strip()
    return cleaned

def main():
    # Load the resolved structure
    with open('/Users/joshandrews/Spare/docs/intercom-backup/resolved-structure.json', 'r') as f:
        resolved_data = json.load(f)

    # Load articles data
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

    # Create articles lookup by ID
    articles_by_id = {str(article['id']): article for article in articles if isinstance(article, dict) and article.get('state') == 'published'}

    # Create new structured backup directory
    new_backup_dir = Path('/Users/joshandrews/Spare/docs/intercom-structured-backup')
    if new_backup_dir.exists():
        shutil.rmtree(new_backup_dir)
    new_backup_dir.mkdir(exist_ok=True)

    # Copy metadata files
    metadata_files = ['complete-mapping.json', 'resolved-structure.json', 'mintlify-structure-suggestions.json', 'structural-analysis.json']
    for metadata_file in metadata_files:
        src = Path('/Users/joshandrews/Spare/docs/intercom-backup') / metadata_file
        if src.exists():
            shutil.copy2(src, new_backup_dir / metadata_file)

    print("# Restructuring Intercom Backup with Proper Hierarchy")
    print("=" * 60)
    print()

    # Process each resolved collection
    resolved_collections = resolved_data['resolved_collections']
    
    for collection_name, collection_data in resolved_collections.items():
        collection_type = collection_data['type']
        articles_list = collection_data['articles']
        
        if collection_type == 'section':
            # This is a section under a parent collection
            parent_collection_name = collection_data['parent_collection_name']
            section_name = collection_data['section_name']
            
            # Create parent collection folder
            parent_folder_name = clean_folder_name(parent_collection_name)
            parent_dir = new_backup_dir / parent_folder_name
            parent_dir.mkdir(exist_ok=True)
            
            # Create section subfolder
            section_folder_name = clean_folder_name(section_name)
            section_dir = parent_dir / section_folder_name
            section_dir.mkdir(exist_ok=True)
            
            print(f"📁 {parent_folder_name}/")
            print(f"  📁 {section_folder_name}/ ({len(articles_list)} articles)")
            
            # Save articles in this section
            for article_info in articles_list:
                article_id = str(article_info['id'])
                if article_id in articles_by_id:
                    article = articles_by_id[article_id]
                    filename = clean_filename(article['title']) + '.json'
                    
                    # Add hierarchy metadata to article
                    article_with_meta = {
                        **article,
                        'hierarchy': {
                            'collection_name': parent_collection_name,
                            'collection_folder': parent_folder_name,
                            'section_name': section_name,
                            'section_folder': section_folder_name,
                            'full_path': f"{parent_folder_name}/{section_folder_name}"
                        }
                    }
                    
                    article_path = section_dir / filename
                    with open(article_path, 'w') as f:
                        json.dump(article_with_meta, f, indent=2)
                    
                    print(f"    📄 {filename}")
            print()
            
        elif collection_type == 'collection':
            # This is a direct collection (no sections)
            collection_folder_name = clean_folder_name(collection_name)
            collection_dir = new_backup_dir / collection_folder_name
            collection_dir.mkdir(exist_ok=True)
            
            print(f"📁 {collection_folder_name}/ ({len(articles_list)} articles)")
            
            # Save articles directly in collection folder
            for article_info in articles_list:
                article_id = str(article_info['id'])
                if article_id in articles_by_id:
                    article = articles_by_id[article_id]
                    filename = clean_filename(article['title']) + '.json'
                    
                    # Add hierarchy metadata to article
                    article_with_meta = {
                        **article,
                        'hierarchy': {
                            'collection_name': collection_name,
                            'collection_folder': collection_folder_name,
                            'section_name': None,
                            'section_folder': None,
                            'full_path': collection_folder_name
                        }
                    }
                    
                    article_path = collection_dir / filename
                    with open(article_path, 'w') as f:
                        json.dump(article_with_meta, f, indent=2)
                    
                    print(f"  📄 {filename}")
            print()
            
        elif collection_type == 'unknown':
            # Handle remaining unknown items
            unknown_folder_name = clean_folder_name(collection_name)
            unknown_dir = new_backup_dir / "unknown" / unknown_folder_name
            unknown_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"❓ unknown/{unknown_folder_name}/ ({len(articles_list)} articles)")
            
            for article_info in articles_list:
                article_id = str(article_info['id'])
                if article_id in articles_by_id:
                    article = articles_by_id[article_id]
                    filename = clean_filename(article['title']) + '.json'
                    
                    article_with_meta = {
                        **article,
                        'hierarchy': {
                            'collection_name': collection_name,
                            'collection_folder': f"unknown/{unknown_folder_name}",
                            'section_name': None,
                            'section_folder': None,
                            'full_path': f"unknown/{unknown_folder_name}"
                        }
                    }
                    
                    article_path = unknown_dir / filename
                    with open(article_path, 'w') as f:
                        json.dump(article_with_meta, f, indent=2)
                    
                    print(f"  📄 {filename}")
            print()

    # Create a summary file showing the complete structure
    structure_summary = []
    
    def scan_directory(path, level=0):
        """Recursively scan directory structure"""
        indent = "  " * level
        folder_name = path.name
        
        # Count articles in this directory
        json_files = list(path.glob("*.json"))
        article_count = len([f for f in json_files if f.name not in metadata_files])
        
        # Count subdirectories
        subdirs = [d for d in path.iterdir() if d.is_dir()]
        
        if article_count > 0:
            structure_summary.append(f"{indent}📁 {folder_name}/ ({article_count} articles)")
        else:
            structure_summary.append(f"{indent}📁 {folder_name}/")
        
        # List articles if any
        for json_file in sorted(json_files):
            if json_file.name not in metadata_files:
                structure_summary.append(f"{indent}  📄 {json_file.name}")
        
        # Recurse into subdirectories
        for subdir in sorted(subdirs):
            scan_directory(subdir, level + 1)

    print("\n" + "=" * 60)
    print("# Complete Structured Backup Directory Tree")
    print("=" * 60)
    print()
    
    # Scan the new backup directory
    for item in sorted(new_backup_dir.iterdir()):
        if item.is_dir():
            scan_directory(item)
        elif item.suffix == '.json' and item.name in metadata_files:
            print(f"📄 {item.name} (metadata)")
    
    # Save the structure summary
    structure_summary_text = "\\n".join(structure_summary)
    with open(new_backup_dir / 'directory-structure.txt', 'w') as f:
        f.write("Intercom Articles - Structured Backup\\n")
        f.write("=" * 40 + "\\n\\n")
        f.write("\\n".join(structure_summary))
    
    print(f"\\n✅ Restructured backup created at: {new_backup_dir}")
    print(f"📄 Directory structure saved to: directory-structure.txt")
    
    # Count totals
    total_articles = 0
    total_folders = 0
    
    for root, dirs, files in os.walk(new_backup_dir):
        total_folders += len(dirs)
        json_files = [f for f in files if f.endswith('.json') and f not in metadata_files]
        total_articles += len(json_files)
    
    print(f"📊 Total: {total_articles} articles in {total_folders} folders")

if __name__ == "__main__":
    main()