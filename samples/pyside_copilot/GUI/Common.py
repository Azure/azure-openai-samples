import html

global vision_flag
vision_flag = False

def replace_code_block(match):
    code = match.group(2)
    escaped_code = html.escape(code)
    return f'<pre style="background-color: #f0f0f0; color: black;"><code>{escaped_code}</code></pre>'
