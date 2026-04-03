#!/usr/bin/env python3
import json
from pathlib import Path

def load_json(input_file):
    """加载 JSON 数据"""
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_commands(data):
    """提取所有第3层级命令"""
    commands = set()
    for category in data:
        for subcategory in category.get('subcategories', []):
            for command in subcategory.get('commands', []):
                commands.add(command['command'])
    return sorted(commands)

def generate_tags_html(commands):
    """生成标签HTML"""
    tags_html = '<div class="tags">\n'
    for cmd in commands:
        tags_html += f'                    <span class="tag" onclick="jumpToTool(\'{cmd}\')">{cmd}</span>\n'
    tags_html += '                </div>'
    return tags_html

def update_html_file(input_html, output_html, new_tags_html):
    """更新HTML文件"""
    with open(input_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到标签部分并替换
    start_marker = '<div class="tags">'
    end_marker = '</div>'
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("错误：找不到标签部分")
        return False
    
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("错误：找不到标签结束部分")
        return False
    
    end_idx += len(end_marker)
    new_content = content[:start_idx] + new_tags_html + content[end_idx:]
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """主函数"""
    json_file = 'my-cmd-final.json'
    html_file = 'terminal-commands.html'
    
    if not Path(json_file).exists():
        print(f'错误：输入文件 {json_file} 不存在')
        return
    
    if not Path(html_file).exists():
        print(f'错误：HTML文件 {html_file} 不存在')
        return
    
    data = load_json(json_file)
    commands = extract_commands(data)
    new_tags_html = generate_tags_html(commands)
    
    if update_html_file(html_file, html_file, new_tags_html):
        print(f'成功更新标签部分，共生成 {len(commands)} 个命令标签')
        print('生成的命令标签：', ', '.join(commands))
    else:
        print('更新失败')

if __name__ == '__main__':
    main()