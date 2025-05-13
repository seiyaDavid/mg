from docx import Document
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# 1. Parse the Word .docx file
def parse_word_docx(docx_path):
    doc = Document(docx_path)
    slide_data = []
    current_slide = {}
    bullets = []

    for para in doc.paragraphs:
        line = para.text.strip()
        if not line:
            continue

        if line.startswith("[SLIDE:"):
            if current_slide:
                current_slide['bullets'] = bullets
                slide_data.append(current_slide)
                current_slide = {}
                bullets = []
        elif line.startswith("Heading:"):
            current_slide['heading'] = line.replace("Heading:", "").strip()
        elif line.startswith("Bullet:") or line.startswith("SubBullet:"):
            bullets.append(line)
        elif line.startswith("Note:"):
            current_slide['note'] = line.replace("Note:", "").strip()

    if current_slide:
        current_slide['bullets'] = bullets
        slide_data.append(current_slide)

    return slide_data

# 2. Create the PowerPoint
def create_presentation(slide_data, output_file="from_word.pptx"):
    prs = Presentation()

    for idx, data in enumerate(slide_data):
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # blank slide

        # Remove default placeholders
        for shape in list(slide.shapes):
            if shape.is_placeholder:
                slide.shapes._spTree.remove(shape._element)

        # Title in red with slide number
        title_text = f"[Slide {idx + 1}] {data.get('heading', '')}"
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(8.0), Inches(1))
        title_frame = title_box.text_frame
        title_frame.clear()
        p = title_frame.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 0, 0)

        # Bullets
        bullets = data.get('bullets', [])
        if bullets:
            body_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.0), Inches(4.5))
            tf = body_box.text_frame
            tf.word_wrap = True
            tf.clear()

            for i, bullet in enumerate(bullets):
                level = 1 if bullet.lower().startswith("subbullet:") else 0
                clean_text = bullet.replace("Bullet:", "").replace("SubBullet:", "").strip()

                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                p.text = clean_text
                p.level = level
                p.font.size = Pt(20)
                p.font.name = 'Calibri'

        # Notes
        note_text = data.get('note')
        if note_text:
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = note_text.strip()

    prs.save(output_file)

# 3. Run it
docx_file = "your_input.docx"  # Replace with your actual Word file
slide_data = parse_word_docx(docx_file)
create_presentation(slide_data, output_file="generated_from_word.pptx")






[SLIDE:1]
Heading: Business Strategy
Bullet: Increase market share
SubBullet: Focus on emerging markets
Bullet: Launch new product line
Note: Mention the Q4 timeline here

[SLIDE:2]
Heading: Risks and Mitigations
Bullet: Supply chain challenges
SubBullet: Diversify suppliers
Note: Stress importance of risk planning
