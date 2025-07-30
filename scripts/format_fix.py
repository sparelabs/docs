#!/usr/bin/env python3
"""
Script to fix formatting issues in help-center MDX files
"""
import re
import os
import glob

def fix_mdx_formatting(content):
    """Fix common formatting issues in MDX content"""
    
    # Fix heading hierarchy - add line breaks after headings when content follows immediately
    content = re.sub(r'(##\s+[^#\n]+)([A-Z][^#\n])', r'\1\n\n\2', content)
    
    # Fix table formatting - convert definition lists to proper tables
    # Pattern: Term followed by definition
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if we're in a concepts section with term-definition pairs
        if '## 2. Core Concepts' in line:
            fixed_lines.append(line)
            fixed_lines.append('')
            
            # Add table header
            fixed_lines.append('| Term | What it means |')
            fixed_lines.append('|------|---------------|')
            i += 1
            
            # Skip existing table headers if they exist
            while i < len(lines) and (lines[i].strip() == '' or 'Term' in lines[i] or 'What it means' in lines[i] or '|' in lines[i] or '-' in lines[i]):
                i += 1
            
            # Process term-definition pairs
            while i < len(lines):
                if lines[i].strip() == '':
                    i += 1
                    continue
                if lines[i].startswith('##'):
                    break
                    
                # Look for bold terms (potential table rows)
                if lines[i].startswith('**') and lines[i].endswith('**'):
                    term = lines[i]
                    i += 1
                    # Skip empty lines
                    while i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    # Get definition
                    if i < len(lines) and not lines[i].startswith('**') and not lines[i].startswith('##'):
                        definition = lines[i]
                        fixed_lines.append(f'| {term} | {definition} |')
                        i += 1
                    else:
                        # No definition found, add term as regular content
                        fixed_lines.append(term)
                else:
                    i += 1
            continue
            
        # Check if we're in a workflows section
        elif '## 4. Common Workflows' in line:
            fixed_lines.append(line)
            fixed_lines.append('')
            
            # Add table header
            fixed_lines.append('| Task | How to do it |')
            fixed_lines.append('|------|-------------|')
            i += 1
            
            # Skip existing headers
            while i < len(lines) and (lines[i].strip() == '' or 'Task' in lines[i] or 'How to do it' in lines[i] or '|' in lines[i] or '-' in lines[i]):
                i += 1
            
            # Process task-description pairs
            while i < len(lines):
                if lines[i].strip() == '':
                    i += 1
                    continue
                if lines[i].startswith('##'):
                    break
                    
                # Look for bold tasks
                if lines[i].startswith('**') and lines[i].endswith('**'):
                    task = lines[i]
                    i += 1
                    # Skip empty lines
                    while i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    # Collect description (may span multiple lines until next ** or ##)
                    description_lines = []
                    while i < len(lines) and not lines[i].startswith('**') and not lines[i].startswith('##'):
                        if lines[i].strip():
                            description_lines.append(lines[i])
                        i += 1
                    
                    if description_lines:
                        description = ' <br><br> '.join(description_lines)
                        fixed_lines.append(f'| {task} | {description} |')
                    else:
                        fixed_lines.append(task)
                else:
                    i += 1
            continue
        
        # Fix bullet lists - ensure proper bullet formatting
        elif line.strip().startswith('**At a glance**'):
            fixed_lines.append(line)
            i += 1
            # Skip empty line
            if i < len(lines) and lines[i].strip() == '':
                fixed_lines.append(lines[i])
                i += 1
            
            # Convert next few lines to bullet points if they're not already
            while i < len(lines) and not lines[i].startswith('##') and lines[i].strip():
                if not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*'):
                    fixed_lines.append(f'- {lines[i].strip()}')
                else:
                    fixed_lines.append(lines[i])
                i += 1
            continue
            
        # Fix navigation interface section
        elif '## 3. Navigating the Interface' in line:
            fixed_lines.append(line)
            fixed_lines.append('')
            i += 1
            
            # Convert following lines to bullet points if not already
            while i < len(lines) and not lines[i].startswith('##'):
                if lines[i].strip() and not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*') and lines[i].startswith('**'):
                    fixed_lines.append(f'- {lines[i].strip()}')
                else:
                    fixed_lines.append(lines[i])
                i += 1
            continue
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single MDX file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_mdx_formatting(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

if __name__ == "__main__":
    # Test with the current file
    filepath = "/Users/joshandrews/Spare/docs/help-center/getting-started/admins---getting-started.mdx"
    if process_file(filepath):
        print(f"Successfully processed {filepath}")
    else:
        print(f"Failed to process {filepath}")