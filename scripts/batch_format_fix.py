#!/usr/bin/env python3
"""
Batch script to fix key formatting issues in help-center MDX files
"""
import os
import re
import glob

def fix_formatting_issues(content, filename):
    """Fix the most critical formatting issues"""
    fixes_applied = []
    
    # 1. Fix missing line breaks after headings
    original_content = content
    content = re.sub(r'(##\s+[^#\n]+)([A-Z][^#\n])', r'\1\n\n\2', content)
    if content != original_content:
        fixes_applied.append("Added line breaks after headings")
    
    # 2. Fix bullet list formatting for "At a glance" sections
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    in_at_glance = False
    
    for i, line in enumerate(lines):
        if '**At a glance**' in line:
            in_at_glance = True
            fixed_lines.append(line)
        elif in_at_glance and (line.startswith('##') or line.strip() == ''):
            in_at_glance = False
            fixed_lines.append(line)
        elif in_at_glance and line.strip() and not line.strip().startswith('-') and not line.strip().startswith('*'):
            # Convert to bullet point
            fixed_lines.append(f'- {line.strip()}')
        else:
            fixed_lines.append(line)
    
    new_content = '\n'.join(fixed_lines)
    if new_content != content:
        fixes_applied.append("Fixed bullet list formatting")
        content = new_content
    
    # 3. Fix navigation interface section
    original_content = content
    content = re.sub(r'(## 3\. Navigating the Interface)\*\*([^*]+)\*\*', r'\1\n\n- **\2**', content)
    if content != original_content:
        fixes_applied.append("Fixed navigation interface formatting")
    
    # 4. Add line breaks between sections
    original_content = content
    content = re.sub(r'(\*\*[^*]+\*\*)\n\n([A-Z][^*\n]+)', r'\1\n\n- \2', content)
    if content != original_content:
        fixes_applied.append("Added bullets to interface items")
    
    # 5. Fix status tables in trip request files
    if 'creating-a-trip-request' in filename or 'Status' in content:
        original_content = content
        # Fix merged status table headers
        content = re.sub(r'(\*\*\s*Status\s*\*\*)\n\n(\*\*Explanation\*\*)', r'| **Status** | **Explanation** |\n|------------|-----------------|', content)
        # Fix individual status rows
        content = re.sub(r'^([A-Z][^|\n]+)\n\n([^*\n][^|\n]+)', r'| \1 | \2 |', content, flags=re.MULTILINE)
        if content != original_content:
            fixes_applied.append("Fixed status table formatting")
    
    return content, fixes_applied

def process_directory(directory_path):
    """Process all MDX files in a directory"""
    mdx_files = glob.glob(os.path.join(directory_path, "*.mdx"))
    results = []
    
    for filepath in mdx_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content, fixes = fix_formatting_issues(content, os.path.basename(filepath))
            
            if fixes:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                results.append({
                    'file': os.path.basename(filepath),
                    'fixes': fixes
                })
            
        except Exception as e:
            results.append({
                'file': os.path.basename(filepath),
                'error': str(e)
            })
    
    return results

def main():
    base_path = "/Users/joshandrews/Spare/docs/help-center"
    
    directories = [
        "getting-started",
        "rider-app", 
        "assets",
        "administration",
        "miscellaneous",
        "reporting",
        "troubleshooting",
        "users-permissions",
        "work-orders",
        "integrations",
        "parts-inventory"
    ]
    
    all_results = {}
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        if os.path.exists(dir_path):
            print(f"Processing {directory}...")
            results = process_directory(dir_path)
            all_results[directory] = results
            print(f"  Processed {len(results)} files")
    
    return all_results

if __name__ == "__main__":
    results = main()
    
    # Print summary
    print("\n=== FORMATTING FIXES SUMMARY ===")
    total_files = 0
    total_fixes = 0
    
    for directory, files in results.items():
        print(f"\n{directory.upper()}:")
        for file_result in files:
            if 'error' in file_result:
                print(f"  ❌ {file_result['file']}: {file_result['error']}")
            else:
                total_files += 1
                total_fixes += len(file_result['fixes'])
                if file_result['fixes']:
                    print(f"  ✅ {file_result['file']}: {', '.join(file_result['fixes'])}")
                else:
                    print(f"  ⭕ {file_result['file']}: No fixes needed")
    
    print(f"\n=== TOTALS ===")
    print(f"Files processed: {total_files}")
    print(f"Total fixes applied: {total_fixes}")