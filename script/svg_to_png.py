import sys
import os
from playwright.sync_api import sync_playwright

def batch_convert_svg_to_png(svg_paths):
    """
    批量将 SVG 转换为 PNG
    """
    if not svg_paths:
        return []
    
    generated_pngs = []
    print(f"正在转换 {len(svg_paths)} 个 SVG 文件为 PNG...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            
            for svg_path in svg_paths:
                if not os.path.exists(svg_path):
                    print(f"警告: 找不到文件 {svg_path}，跳过转换")
                    continue
                    
                png_path = os.path.splitext(svg_path)[0] + ".png"
                print(f"  Converting: {svg_path} -> {png_path}")
                
                try:
                    page = browser.new_page()
                    # Use file:/// URI
                    abs_path_str = os.path.abspath(svg_path).replace('\\', '/')
                    uri = f"file:///{abs_path_str}"
                    page.goto(uri)
                    
                    # 获取 svg 元素并截图
                    svg_element = page.locator('svg').first
                    if svg_element.count() > 0:
                        svg_element.screenshot(path=png_path, omit_background=True)
                        generated_pngs.append(png_path)
                    else:
                        print(f"  Failed: No <svg> element found in {svg_path}")
                    
                    page.close()
                except Exception as e:
                    print(f"  Failed to convert {svg_path}: {e}")
            
            browser.close()
    except Exception as e:
        print(f"Playwright error: {e}")
    
    return generated_pngs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python scripts/svg_to_png.py <svg文件路径1> [svg文件路径2 ...]")
        print("或者: python scripts/svg_to_png.py <包含svg的目录>")
    else:
        paths = sys.argv[1:]
        svg_files = []
        
        for p in paths:
            if os.path.isfile(p) and p.lower().endswith('.svg'):
                svg_files.append(p)
            elif os.path.isdir(p):
                for root, dirs, files in os.walk(p):
                    for f in files:
                        if f.lower().endswith('.svg'):
                            svg_files.append(os.path.join(root, f))
        
        if not svg_files:
            print("未找到 SVG 文件")
        else:
            batch_convert_svg_to_png(svg_files)
