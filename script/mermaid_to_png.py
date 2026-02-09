import sys
import os
import re
from playwright.sync_api import sync_playwright

def process_mermaid_content(content, md_file_path):
    """
    Scans content for mermaid blocks, converts them to PNGs,
    and returns (new_content, generated_png_paths).
    
    The new_content will have mermaid blocks replaced by markdown image links.
    """
    # Matches ```mermaid ... ```
    mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    matches = list(mermaid_pattern.finditer(content))

    if not matches:
        return content, []

    # Create assets dir
    md_dir = os.path.dirname(os.path.abspath(md_file_path))
    assets_dir = os.path.join(md_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(md_file_path))[0]
    
    print(f"  Found {len(matches)} mermaid blocks. Starting conversion...")
    
    generated_pngs = []
    replacements = [] # List of (start_index, end_index, replacement_string)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # Use a higher scale factor for better quality
            context = browser.new_context(device_scale_factor=2)
            page = context.new_page()

            for i, match in enumerate(matches):
                mermaid_code = match.group(1)
                
                # HTML template
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>
                        mermaid.initialize({{ 
                            startOnLoad: true,
                            theme: 'default',
                            securityLevel: 'loose'
                        }});
                    </script>
                    <style>
                        body {{ margin: 0; padding: 0; background: white; }}
                        #container {{ display: inline-block; padding: 10px; }}
                    </style>
                </head>
                <body>
                    <div id="container" class="mermaid">
                    {mermaid_code}
                    </div>
                </body>
                </html>
                """
                
                try:
                    page.set_content(html_content)
                    
                    # Wait for the svg to be generated
                    page.wait_for_selector('.mermaid svg', state='attached', timeout=10000)
                    
                    # Sometimes mermaid takes a moment to layout
                    page.wait_for_timeout(500)

                    # Locate the container to screenshot just the diagram
                    element = page.locator('#container')
                    
                    # Output filename: {filename}_mermaid_{index}.png
                    output_filename = f"{base_name}_mermaid_{i+1}.png"
                    output_path = os.path.join(assets_dir, output_filename)
                    
                    element.screenshot(path=output_path, omit_background=True)
                    print(f"  Saved: {output_path}")
                    
                    generated_pngs.append(output_path)
                    
                    # Prepare replacement string: ![Mermaid Diagram](assets/filename.png)
                    # We use relative path from the md file
                    rel_path = f"assets/{output_filename}"
                    replacement = f"![Mermaid Diagram]({rel_path})"
                    
                    replacements.append((match.start(), match.end(), replacement))
                    
                except Exception as e:
                    print(f"  Error converting block {i+1}: {e}")
                    # If failed, we don't replace, so the code block remains

            browser.close()
            print("  Mermaid conversion complete.")

    except Exception as e:
        print(f"  Playwright error: {e}")
        return content, generated_pngs

    # Apply replacements in reverse order to keep indices valid
    new_content = content
    for start, end, repl in sorted(replacements, key=lambda x: x[0], reverse=True):
        new_content = new_content[:start] + repl + new_content[end:]
        
    return new_content, generated_pngs

def convert_mermaid_in_file(md_file_path):
    print(f"Processing {md_file_path}...")
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read file {md_file_path}: {e}")
        return

    # In standalone mode, we might NOT want to modify the file content by default?
    # Or maybe we do? The user asked for "convert mermaid blocks to png", usually implies keeping them or replacing them?
    # The prompt said "convert mermaid blocks to png, generated pngs saved in assets".
    # It didn't explicitly say "replace code blocks in the file". 
    # BUT for export_wechat, we MUST replace.
    # For standalone usage, let's keep the file strictly read-only regarding content modification to be safe, 
    # OR we can just generate the PNGs. 
    # The original script I wrote ONLY generated PNGs and didn't modify the file.
    # Let's keep `convert_mermaid_in_file` behavior as "generate PNGs only" but use the core logic.
    
    # Actually, the user's previous request was "convert... saved in assets". 
    # My previous implementation just saved PNGs.
    # I'll stick to that for the standalone entry point.
    
    process_mermaid_content(content, md_file_path) 
    # We ignore the return value (new_content) so the file isn't changed, but PNGs are generated.

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script/mermaid_to_png.py <markdown_file_or_directory>")
        sys.exit(1)
        
    target = sys.argv[1]
    
    if os.path.isfile(target):
        convert_mermaid_in_file(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for f in files:
                if f.lower().endswith('.md'):
                    convert_mermaid_in_file(os.path.join(root, f))
    else:
        print(f"Error: {target} is not a valid file or directory")
