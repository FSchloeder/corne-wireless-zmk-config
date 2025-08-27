#!/usr/bin/env python3
"""
Visualize ZMK keymap by parsing and generating an HTML visualization
"""
import subprocess
import sys
import os

# Set UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Parse the keymap
try:
    result = subprocess.run(
        ['keymap', 'parse', '-c', '12', '-z', 'config/corne.keymap'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode == 0:
        # Save the YAML output
        with open('keymap.yaml', 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        print("✓ Successfully parsed keymap to keymap.yaml")
        
        # Now generate the SVG visualization
        print("Generating SVG visualization...")
        draw_result = subprocess.run(
            ['keymap', 'draw', 'keymap.yaml'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if draw_result.returncode == 0:
            with open('keymap.svg', 'w', encoding='utf-8') as f:
                f.write(draw_result.stdout)
            print("✓ Successfully generated keymap.svg")
            
            # Create an HTML wrapper for easy viewing
            html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>ZMK Keymap Visualization</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
        h1 {{ color: #333; }}
        .layer {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Your Corne Keyboard Layout (Neo-based)</h1>
    {draw_result.stdout}
</body>
</html>'''
            
            with open('keymap_visualization.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✓ Created keymap_visualization.html - open this file in your browser to view the layout")
        else:
            print(f"Error generating visualization: {draw_result.stderr}")
    else:
        print(f"Error parsing keymap: {result.stderr}")
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)