from bs4 import BeautifulSoup
import re

def process_text(text):
    # Parse the text with BeautifulSoup
    #soup = BeautifulSoup(text, 'html.parser')
    soup = BeautifulSoup(text)

    # Find all instances of bold text and wrap them in <strong> tags
    for bold in soup.find_all('b'):
        bold.replace_with('<strong>{}</strong>'.format(bold.text))

    # Find all instances of italic text and wrap them in <em> tags
    for italic in soup.find_all('i'):
        italic.replace_with('<em>{}</em>'.format(italic.text))

    # Find all instances of text with a URL pattern and wrap them in <a> tags
    for link in soup.find_all(text=re.compile('https?://')):
        link.replace_with('<a href="{}">{}</a>'.format(link.text, link.text))

    # Find all instances of text with 3 or more capital letters and wrap them in <h3> tags
    for heading in soup.find_all(text=re.compile('[A-Z]{3,}')):
        heading.replace_with('<h3>{}</h3>'.format(heading.text))

    # Find all instances of text that start with a number and wrap them in <li> tags within a <ul> list
    list_items = []
    for item in soup.find_all(text=re.compile('^[0-9]')):
        list_items.append('<li>{}</li>'.format(item.text))

    list_html = '<ul>{}</ul>'.format(''.join(list_items))

    soup.body.insert(0, list_html)

    # Find all instances of text that are separated by a tab character and wrap them in <td> tags within a <tr> row within a <table>
    rows = []
    for row in soup.find_all(text=re.compile('\t')):
        cells = row.text.split('\t')
        cells_html = ''.join(['<td>{}</td>'.format(cell) for cell in cells])
        rows.append('<tr>{}</tr>'.format(cells_html))

    table_html = '<table>{}</table>'.format(''.join(rows))

    soup.body.insert(0, table_html)

    # Find all instances of text with a URL pattern that ends in .jpg or .png and wrap them in <img> tags
    for image in soup.find_all(text=re.compile('https?://.*(jpg|png)$')):
        image.replace_with('<img src="{}" alt="">'.format(image.text))

    # Find all instances of text that are preceded by a > character and wrap them in <blockquote> tags
    for blockquote in soup.find_all(text=re.compile('^>')):
        blockquote.replace_with('<blockquote>{}</blockquote>'.format(blockquote.text))

    # Find all instances of text that are surrounded by backticks (`) and wrap them in <code> tags
    for code in soup.find_all(text=re.compile('^`(.*)`$')):
        code.replace_with('<code>{}</code>'.format(code.text))

    # Find all instances of text that are three or more hyphens (-) and wrap them in <hr> tags
    for hr in soup.find_all(text=re.compile('^---+$')):
        hr.replace_with('<hr>')

    # Find all instances of text that are separated by two or more newline characters and wrap them in <p> tags
    paragraphs = []
    for paragraph in soup.find_all(text=re.compile('\n{2,}')):
        paragraphs.append('<p>{}</p>'.format(paragraph.text))

    paragraphs_html = ''.join(paragraphs)

    soup.body.insert(0, paragraphs_html)

    # Find all instances of text that are separated by a single newline character and wrap them in <br> tags
    for line_break in soup.find_all(text=re.compile('\n')):
        line_break.replace_with('<br>')

    # Find all instances of text that match a specific pattern and wrap them in custom <custom> tags
    for custom in soup.find_all(text=re.compile('custom pattern')):
        custom.replace_with('<custom>{}</custom>'.format(custom.text))

    # Find all instances of text that match a specific pattern and wrap them in <span> tags with a specific font style
    for font in soup.find_all(text=re.compile('font pattern')):
        font.replace_with('<span style="font-style: italic;">{}</span>'.format(font.text))

    # Find all instances of text that match a specific pattern and wrap them in <span> tags with a specific font color
    for color in soup.find_all(text=re.compile('color pattern')):
        color.replace_with('<span style="color: red;">{}</span>'.format(color.text))

    # Find all instances of text that match a specific pattern and wrap them in <span> tags with a specific font size
    for size in soup.find_all(text=re.compile('size pattern')):
        size.replace_with('<span style="font-size: 18px;">{}</span>'.format(size.text))

    # Render the text with the inserted HTML tags
    return {'text': soup.prettify()}

