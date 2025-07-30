#!/usr/bin/env python3
import json
import os
from pathlib import Path

def main():
    # Load the comprehensive mapping
    with open('/Users/joshandrews/Spare/docs/intercom-backup/complete-mapping.json', 'r') as f:
        intercom_data = json.load(f)
    
    # Load the comparison data  
    with open('/Users/joshandrews/Spare/docs/intercom-backup/mintlify-comparison.json', 'r') as f:
        comparison_data = json.load(f)
    
    print("# Intercom to Mintlify Structure Analysis")
    print("=" * 50)
    print()
    
    print(f"**Total Intercom Articles**: {intercom_data['total_articles']}")
    print(f"**Total Mintlify Files**: {comparison_data['mintlify_files']}")
    print(f"**Missing Articles**: {comparison_data['missing_in_mintlify']}")
    print()
    
    print("## Key Issues Identified:")
    print()
    
    # 1. Structure mismatch
    print("### 1. Structure Mismatch")
    print("The current Mintlify structure doesn't match Intercom's organization:")
    print()
    
    # Map Intercom collections to current Mintlify structure
    intercom_collections = list(intercom_data['collections'].keys())
    
    # Group current mintlify files by top-level directory
    mintlify_groups = {}
    for file_path in comparison_data['mintlify_structure']:
        top_dir = file_path.split('/')[0]
        if top_dir not in mintlify_groups:
            mintlify_groups[top_dir] = []
        mintlify_groups[top_dir].append(file_path)
    
    print("**Intercom Collections (Real Structure):**")
    proper_collections = [c for c in intercom_collections if not c.startswith('Unknown Collection')]
    unknown_collections = [c for c in intercom_collections if c.startswith('Unknown Collection')]
    
    for collection in sorted(proper_collections):
        count = len(intercom_data['collections'][collection])
        print(f"- {collection} ({count} articles)")
    
    print()
    print("**Current Mintlify Structure:**")
    for group, files in sorted(mintlify_groups.items()):
        print(f"- {group}/ ({len(files)} files)")
    
    print()
    print("### 2. Missing Collection Mappings")
    print(f"There are {len(unknown_collections)} 'Unknown Collections' that need proper mapping:")
    print()
    
    # Try to identify what these unknown collections should be
    collection_meta = intercom_data['collection_metadata']
    
    for unknown in sorted(unknown_collections):
        collection_id = unknown.replace('Unknown Collection ', '')
        if collection_id in collection_meta:
            meta = collection_meta[collection_id]
            count = len(intercom_data['collections'][unknown])
            print(f"- Collection ID {collection_id}: {count} articles")
            if 'description' in meta and meta['description']:
                print(f"  Description: {meta['description']}")
            # Show a few sample articles
            sample_articles = intercom_data['collections'][unknown][:3]
            for article in sample_articles:
                print(f"  - {article['title']}")
            print()
    
    print("### 3. Proper Collection Structure Should Be:")
    print()
    
    # Recommend proper structure based on Intercom
    recommended_structure = {
        'General Support': 'general-support',
        'Spare Operations: Service Administrators': 'service-administrators', 
        'Spare Operations: Booking Agents': 'booking-agents',
        'Spare Operations: Dispatchers': 'dispatchers',
        'Spare Operations: Schedulers': 'schedulers',
        'Spare Driver': 'driver',
        'Spare Rider': 'rider',
        'Spare Analytics': 'analytics',
        'Spare Open Fleets': 'open-fleets',
        'Spare Eligibility': 'eligibility',
        'Spare Realize': 'realize',
        'Spare API': 'api',
        'Spare Workflows': 'workflows',
        'Spare EAM': 'eam',
        'Spare AI': 'ai',
        'Release Notes and FAQs': 'release-notes'
    }
    
    for intercom_name, suggested_dir in recommended_structure.items():
        if intercom_name in intercom_data['collections']:
            count = len(intercom_data['collections'][intercom_name])
            print(f"- {suggested_dir}/ <- '{intercom_name}' ({count} articles)")
    
    print()
    print("### 4. Current Issues with File Organization")
    print()
    print("The current structure has many articles in inappropriate directories:")
    print("- Many rider-related articles are in 'miscellaneous/'")
    print("- Driver articles are mixed across multiple directories") 
    print("- Service administration content is scattered")
    print("- No clear separation between user roles (admin, dispatcher, etc.)")
    
    print()
    print("## Recommendations:")
    print()
    print("1. **Restructure based on Intercom collections** - Use the proper collection names and hierarchy")
    print("2. **Map Unknown Collections** - Identify and properly categorize the unknown collections")
    print("3. **Consolidate scattered content** - Move misplaced articles to appropriate directories")
    print("4. **Update docs.json navigation** - Reflect the proper structure in Mintlify configuration")
    print("5. **Preserve all content** - Ensure no articles are lost in the restructuring")
    
    # Save detailed mapping for reference
    detailed_mapping = {
        'recommended_structure': recommended_structure,
        'current_mintlify_groups': mintlify_groups,
        'intercom_collections': {k: len(v) for k, v in intercom_data['collections'].items()},
        'unknown_collections_detail': {}
    }
    
    # Add details for unknown collections
    for unknown in unknown_collections:
        collection_id = unknown.replace('Unknown Collection ', '')
        if collection_id in collection_meta:
            detailed_mapping['unknown_collections_detail'][collection_id] = {
                'name': unknown,
                'metadata': collection_meta[collection_id],
                'article_count': len(intercom_data['collections'][unknown]),
                'sample_articles': [a['title'] for a in intercom_data['collections'][unknown][:5]]
            }
    
    with open('/Users/joshandrews/Spare/docs/intercom-backup/structural-analysis.json', 'w') as f:
        json.dump(detailed_mapping, f, indent=2)
    
    print()
    print("Detailed analysis saved to: structural-analysis.json")

if __name__ == "__main__":
    main()