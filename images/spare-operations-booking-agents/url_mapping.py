#!/usr/bin/env python3
"""
Script to generate the complete URL mapping for downloaded booking agents images
"""
import os
import re
import glob

def extract_images_from_mdx(file_path):
    """Extract image URLs and alt text from MDX file"""
    images = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all markdown image patterns: ![alt](url)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        for alt_text, url in matches:
            # Only include external URLs (http/https)
            if url.startswith(('http://', 'https://')):
                images.append({
                    'alt': alt_text,
                    'url': url,
                    'file': file_path
                })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return images

def main():
    base_dir = "/Users/joshandrews/Spare/docs/help-center/spare-operations-booking-agents"
    images_dir = "/Users/joshandrews/Spare/docs/images/spare-operations-booking-agents"
    
    # Directory mapping for prefixes
    prefix_map = {
        'booking-agents-getting-started': 'bas',
        'booking-agents-managing-riders': 'bamr', 
        'booking-agents-managing-trips': 'bamt',
        'booking-agents-troubleshooting-and-faqs': 'batf'
    }
    
    all_images = []
    
    # Process each subdirectory
    for subdir, prefix in prefix_map.items():
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.exists(subdir_path):
            # Find all MDX files in subdirectory
            mdx_files = glob.glob(os.path.join(subdir_path, "*.mdx"))
            
            for mdx_file in mdx_files:
                images = extract_images_from_mdx(mdx_file)
                for img in images:
                    img['prefix'] = prefix
                    img['subdir'] = subdir
                all_images.append(images)
    
    # Flatten the list
    flat_images = []
    for img_list in all_images:
        flat_images.extend(img_list)
    
    print(f"Found {len(flat_images)} external images")
    
    # Get downloaded files
    downloaded_files = sorted(os.listdir(images_dir))
    downloaded_files = [f for f in downloaded_files if f.endswith(('.png', '.jpg', '.gif'))]
    
    print(f"Downloaded {len(downloaded_files)} image files")
    
    # Generate mapping
    print("\n=== COMPLETE URL MAPPING ===")
    
    # Group by prefix
    by_prefix = {}
    for img in flat_images:
        prefix = img['prefix']
        if prefix not in by_prefix:
            by_prefix[prefix] = []
        by_prefix[prefix].append(img)
    
    # Match downloaded files to URLs by prefix and order
    for prefix in ['bas', 'bamr', 'bamt', 'batf']:
        if prefix in by_prefix:
            prefix_images = by_prefix[prefix]
            prefix_files = [f for f in downloaded_files if f.startswith(prefix + '_')]
            
            print(f"\n### {prefix.upper()}_ ({len(prefix_files)} files)")
            
            for i, img in enumerate(prefix_images):
                if i < len(prefix_files):
                    filename = prefix_files[i]
                    print(f"{img['url']} → {filename}")
                else:
                    print(f"WARNING: No file found for {img['url']}")

if __name__ == "__main__":
    main()