
import re

def html_converter(md_text):
    md_text = re.sub(r'^# (.+)', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.+)', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^### (.+)', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)

    md_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', md_text)

    md_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', md_text)

    md_text = re.sub(r'\n\d+\. (.+)', r'\n<li>\1</li>', md_text)
    md_text = re.sub(r'(?:<li>.*?</li>\n?)+', lambda m: f"<ol>{m.group(0)}</ol>", md_text, flags=re.DOTALL)

    md_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md_text)
    
    return md_text

ex_test = """
# Exemplo

Este é um **exemplo** de *Markdown*.

1. Primeiro item
2. Segundo item
3. Terceiro item

Como pode ser consultado em [página da UC](http://www.uc.pt)
"""

html_output = html_converter(ex_test)
print(html_output)