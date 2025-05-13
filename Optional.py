from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_presentation(slide_data, output_file="validated_output.pptx"):
    prs = Presentation()

    for data in slide_data:
        slide_layout = prs.slide_layouts[5]  # blank layout
        slide = prs.slides.add_slide(slide_layout)

        # Remove any placeholder shapes
        for shape in list(slide.shapes):
            if shape.is_placeholder:
                slide.shapes._spTree.remove(shape._element)

        # Add red heading
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(8.5), Inches(1))
        title_frame = title_box.text_frame
        title_frame.clear()
        title_para = title_frame.paragraphs[0]
        title_para.text = data.get('heading', '')
        title_para.font.size = Pt(28)
        title_para.font.bold = True
        title_para.font.color.rgb = RGBColor(255, 0, 0)

        # Add bullet points
        bullets = data.get('bullets', [])
        if bullets:
            bullet_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.5), Inches(4.5))
            bullet_frame = bullet_box.text_frame
            bullet_frame.clear()

            for i, bullet in enumerate(bullets):
                level = 1 if bullet.strip().lower().startswith("subbullet:") else 0
                clean_text = bullet.replace("SubBullet:", "").replace("Bullet:", "").strip()

                p = bullet_frame.add_paragraph() if i > 0 else bullet_frame.paragraphs[0]
                p.text = clean_text
                p.level = level
                p.font.size = Pt(20)
                p.font.name = 'Calibri'
                p.space_after = Pt(6)

        # Add speaker notes
        note_text = data.get('note')
        if note_text:
            notes_slide = slide.notes_slide
            notes_text_frame = notes_slide.notes_text_frame
            notes_text_frame.text = note_text.strip()

    prs.save(output_file)

# ✅ Sample data
slide_data = [
    {
        "heading": "Business Summary",
        "bullets": [
            "Bullet: Revenue increased by 25%",
            "SubBullet: North America +15%",
            "SubBullet: Europe +10%",
            "Bullet: Gross margin held steady"
        ],
        "note": "Explain Q1 performance was strong due to increased demand."
    },
    {
        "heading": "Challenges",
        "bullets": [
            "Bullet: Supply chain issues",
            "SubBullet: Chip shortages",
            "Bullet: Inflation impact on costs"
        ],
        "note": "Discuss the mitigation strategies being explored."
    }
]

# ✅ Run function
create_presentation(slide_data)
