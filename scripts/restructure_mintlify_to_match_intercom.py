#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
import re

def clean_filename_for_path(name):
    """Convert name to safe path component"""
    # Remove HTML entities and problematic characters
    cleaned = name.replace('/', '-').replace(':', '').replace('?', '').replace('!', '')
    cleaned = cleaned.replace("'", '').replace('"', '').replace('&', 'and')
    cleaned = cleaned.replace(' ', '-').replace('---', '-').replace('--', '-')
    cleaned = cleaned.strip('-').lower()
    return cleaned

def find_matching_mdx_files(title, current_files):
    """Find MDX files that might match this article title"""
    # Clean the title for comparison
    clean_title = clean_filename_for_path(title)
    
    # Try various matching strategies
    potential_matches = []
    
    for file_path in current_files:
        file_stem = file_path.stem.lower()
        
        # Direct match
        if clean_title == file_stem:
            potential_matches.append((file_path, 'exact'))
            
        # Contains match
        elif clean_title in file_stem or file_stem in clean_title:
            potential_matches.append((file_path, 'contains'))
            
        # Word-based matching
        title_words = set(clean_title.split('-'))
        file_words = set(file_stem.split('-'))
        
        if len(title_words & file_words) >= min(3, len(title_words) * 0.6):
            potential_matches.append((file_path, 'words'))
    
    # Return best match
    if potential_matches:
        # Prioritize exact matches
        exact_matches = [m for m in potential_matches if m[1] == 'exact']
        if exact_matches:
            return exact_matches[0][0]
        
        # Then contains matches
        contains_matches = [m for m in potential_matches if m[1] == 'contains']
        if contains_matches:
            return contains_matches[0][0]
            
        # Finally word matches
        return potential_matches[0][0]
    
    return None

def main():
    # Paths
    intercom_backup = Path('/Users/joshandrews/Spare/docs/intercom-structured-backup')
    current_help_center = Path('/Users/joshandrews/Spare/docs/help-center')
    new_help_center = Path('/Users/joshandrews/Spare/docs/help-center-restructured')
    
    # Create backup of current structure
    if current_help_center.exists():
        backup_path = Path('/Users/joshandrews/Spare/docs/help-center-backup')
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(current_help_center, backup_path)
        print(f"✅ Backed up current help-center to: {backup_path}")
    
    # Create new restructured directory
    if new_help_center.exists():
        shutil.rmtree(new_help_center)
    new_help_center.mkdir()
    
    # Get all current MDX files
    current_mdx_files = list(current_help_center.rglob('*.mdx'))
    print(f"Found {len(current_mdx_files)} current MDX files")
    
    # Track files that we've moved
    moved_files = set()
    migration_log = []
    
    print("\n# Restructuring Help Center to Match Intercom Structure")
    print("=" * 60)
    
    # Process each collection in intercom-structured-backup
    for collection_dir in sorted(intercom_backup.iterdir()):
        if not collection_dir.is_dir():
            continue
            
        collection_name = collection_dir.name
        print(f"\n## Processing: {collection_name}")
        
        # Create collection directory in new structure
        new_collection_dir = new_help_center / clean_filename_for_path(collection_name)
        new_collection_dir.mkdir(exist_ok=True)
        
        # Check if this collection has subsections
        has_subsections = any(item.is_dir() for item in collection_dir.iterdir() if not item.name.endswith('.json'))
        
        if has_subsections:
            # Process subsections
            for subsection_dir in sorted(collection_dir.iterdir()):
                if not subsection_dir.is_dir():
                    continue
                    
                subsection_name = subsection_dir.name
                print(f"  📁 {subsection_name}/")
                
                # Create subsection directory
                new_subsection_dir = new_collection_dir / clean_filename_for_path(subsection_name)
                new_subsection_dir.mkdir(exist_ok=True)
                
                # Process articles in this subsection
                json_files = list(subsection_dir.glob('*.json'))
                for json_file in json_files:
                    # Load article metadata
                    with open(json_file, 'r') as f:
                        article_data = json.load(f)
                    
                    article_title = article_data['title']
                    
                    # Find matching MDX file
                    matching_file = find_matching_mdx_files(article_title, current_mdx_files)
                    
                    if matching_file and matching_file not in moved_files:
                        # Move the file
                        new_file_path = new_subsection_dir / matching_file.name
                        shutil.copy2(matching_file, new_file_path)
                        moved_files.add(matching_file)
                        
                        migration_log.append({
                            'article_title': article_title,
                            'old_path': str(matching_file.relative_to(current_help_center)),
                            'new_path': str(new_file_path.relative_to(new_help_center)),
                            'collection': collection_name,
                            'subsection': subsection_name
                        })
                        
                        print(f"    ✅ {matching_file.name} → {new_file_path.relative_to(new_help_center)}")
                    else:
                        print(f"    ❌ No match found for: {article_title}")
        
        else:
            # Process direct articles in collection
            json_files = list(collection_dir.glob('*.json'))
            for json_file in json_files:
                # Load article metadata
                with open(json_file, 'r') as f:
                    article_data = json.load(f)
                
                article_title = article_data['title']
                
                # Find matching MDX file
                matching_file = find_matching_mdx_files(article_title, current_mdx_files)
                
                if matching_file and matching_file not in moved_files:
                    # Move the file
                    new_file_path = new_collection_dir / matching_file.name
                    shutil.copy2(matching_file, new_file_path)
                    moved_files.add(matching_file)
                    
                    migration_log.append({
                        'article_title': article_title,
                        'old_path': str(matching_file.relative_to(current_help_center)),
                        'new_path': str(new_file_path.relative_to(new_help_center)),
                        'collection': collection_name,
                        'subsection': None
                    })
                    
                    print(f"  ✅ {matching_file.name} → {new_file_path.relative_to(new_help_center)}")
                else:
                    print(f"  ❌ No match found for: {article_title}")
    
    # Handle unmoved files
    unmoved_files = [f for f in current_mdx_files if f not in moved_files]
    if unmoved_files:
        print(f"\n## Unmoved Files ({len(unmoved_files)})")
        unmoved_dir = new_help_center / "unmapped"
        unmoved_dir.mkdir(exist_ok=True)
        
        for unmoved_file in unmoved_files:
            new_file_path = unmoved_dir / unmoved_file.name
            shutil.copy2(unmoved_file, new_file_path)
            print(f"  📄 {unmoved_file.name} → unmapped/")
            
            migration_log.append({
                'article_title': unmoved_file.stem,
                'old_path': str(unmoved_file.relative_to(current_help_center)),
                'new_path': str(new_file_path.relative_to(new_help_center)),
                'collection': 'unmapped',
                'subsection': None
            })
    
    # Save migration log
    with open(new_help_center / 'migration-log.json', 'w') as f:
        json.dump(migration_log, f, indent=2)
    
    # Create summary
    summary = {
        'total_files_processed': len(current_mdx_files),
        'files_moved_to_structure': len(moved_files),
        'files_unmapped': len(unmoved_files),
        'collections_created': len([d for d in new_help_center.iterdir() if d.is_dir() and d.name != 'unmapped']),
        'migration_success_rate': f"{(len(moved_files) / len(current_mdx_files) * 100):.1f}%"
    }
    
    with open(new_help_center / 'migration-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n" + "=" * 60)
    print("# Migration Summary")
    print("=" * 60)
    print(f"📊 Total files: {summary['total_files_processed']}")
    print(f"✅ Successfully mapped: {summary['files_moved_to_structure']}")
    print(f"❓ Unmapped: {summary['files_unmapped']}")
    print(f"📁 Collections created: {summary['collections_created']}")
    print(f"🎯 Success rate: {summary['migration_success_rate']}")
    
    print(f"\n✅ Restructured help center created at: {new_help_center}")
    print(f"📄 Migration log saved to: migration-log.json")
    print(f"📊 Summary saved to: migration-summary.json")
    
    print("\n⚠️  Next steps:")
    print("1. Review the unmapped files and manually place them")
    print("2. Update docs.json to reflect the new structure")
    print("3. Test the new structure")
    print("4. Replace the old help-center with the new one")

if __name__ == "__main__":
    main()