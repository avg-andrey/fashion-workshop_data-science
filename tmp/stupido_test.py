import markdown
from markdown2 import markdown
from PIL import Image, ImageDraw, ImageFont

# Markdown text
markdown_text = """
# Corsi Online
- **Coursera**: [Marketing Analytics](https://www.coursera.org/)
- **edX**: [Data Science for Business Leaders](https://www.edx.org/)
- **Udemy**: [Business Intelligence & Data Analytics](https://www.udemy.com/)

# Articoli e Blog
- [Towards Data Science](https://towardsdatascience.com/)
- [Harvard Business Review – Data Analytics](https://hbr.org/)
- [OpenAI Blog](https://openai.com/blog/)

# Strumenti di BI
- [Tableau](https://www.tableau.com/)
- [Power BI](https://powerbi.microsoft.com/)
"""

# Convert markdown to plain text
html = markdown(markdown_text)
plain_text = html.replace('<h1>', '\n# ').replace('</h1>', '\n').replace('<ul>', '').replace('</ul>', '').replace('<li>', '- ').replace('</li>', '\n').replace('<strong>', '**').replace('</strong>', '**').replace('<a href="', '(').replace('</a>', ')').replace('">', ' ').replace('</p>', '\n').replace('<p>', '\n')

# Create an image
image_width = 800
font_size = 20
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust as needed
font = ImageFont.truetype(font_path, font_size)

lines = plain_text.split('\n')
image_height = len(lines) * (font_size + 10) + 20

image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Draw the text on the image
y = 10
for line in lines:
    draw.text((10, y), line, fill="black", font=font)
    y += font_size + 10

# Save the image
image.save("markdown_image.png")
