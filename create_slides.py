import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import re

def create_professional_slides(markdown_content, output_file):
    """
    Converts markdown content to professional PowerPoint slides
    
    Args:
        markdown_content (str): Markdown text with slide separators (---)
        output_file (str): Filename for output PowerPoint
    """
    prs = Presentation()
    
    # Set consistent font sizes and styles
    TITLE_FONT_SIZE = Pt(32)
    SUBTITLE_FONT_SIZE = Pt(20)
    CONTENT_FONT_SIZE = Pt(18)
    BULLET_FONT_SIZE = Pt(18)
    
    # Professional color scheme
    TITLE_COLOR = RGBColor(0, 51, 102)  # Dark blue
    TEXT_COLOR = RGBColor(0, 0, 0)      # Black
    ACCENT_COLOR = RGBColor(0, 102, 204) # Medium blue
    
    sections = re.split(r'\n---\n', markdown_content)
    
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.strip().split('\n')
        
        # Find title (lines with # or ##)
        title_line = next((line for line in lines if re.match(r'^#+\s+', line)), None)
        
        # Skip section if no title found
        if not title_line:
            continue
            
        # Determine slide layout based on content
        if title_line.startswith('# '):  # Main title slide
            slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title slide
            title_text = title_line.replace('# ', '')
            subtitle_line = lines[1] if len(lines) > 1 and not lines[1].startswith('#') else ""
            
            # Set title with formatting
            title_shape = slide.shapes.title
            title_shape.text = title_text
            title_para = title_shape.text_frame.paragraphs[0]
            title_para.alignment = PP_ALIGN.CENTER
            for run in title_para.runs:
                run.font.size = TITLE_FONT_SIZE
                run.font.color.rgb = TITLE_COLOR
                run.font.bold = True
            
            # Set subtitle with formatting if it exists
            if len(slide.placeholders) > 1 and subtitle_line:
                subtitle_shape = slide.placeholders[1]
                subtitle_shape.text = subtitle_line
                subtitle_para = subtitle_shape.text_frame.paragraphs[0]
                subtitle_para.alignment = PP_ALIGN.CENTER
                for run in subtitle_para.runs:
                    run.font.size = SUBTITLE_FONT_SIZE
                    run.font.color.rgb = TEXT_COLOR
        else:
            # Content slide
            slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and content
            title_text = title_line.replace('## ', '')
            
            # Set title with formatting
            title_shape = slide.shapes.title
            title_shape.text = title_text
            title_para = title_shape.text_frame.paragraphs[0]
            for run in title_para.runs:
                run.font.size = TITLE_FONT_SIZE
                run.font.color.rgb = TITLE_COLOR
                run.font.bold = True
            
            # Collect content (excluding the title)
            content_lines = [line for line in lines if line != title_line]
            
            # Process content for bullets and formatting
            if content_lines and len(slide.placeholders) > 1:
                text_frame = slide.placeholders[1].text_frame
                
                p = None
                for line in content_lines:
                    # Skip empty lines
                    if not line.strip():
                        continue
                    
                    # Bullet points with proper indentation
                    if line.strip().startswith('- '):
                        p = text_frame.add_paragraph()
                        p.text = line.strip()[2:]
                        p.level = 0
                        for run in p.runs:
                            run.font.size = BULLET_FONT_SIZE
                            run.font.color.rgb = TEXT_COLOR
                    
                    # Sub-bullets with proper indentation
                    elif line.strip().startswith('  - '):
                        p = text_frame.add_paragraph()
                        p.text = line.strip()[4:]
                        p.level = 1
                        for run in p.runs:
                            run.font.size = BULLET_FONT_SIZE
                            run.font.color.rgb = TEXT_COLOR
                    
                    # Regular text
                    else:
                        p = text_frame.add_paragraph()
                        p.text = line
                        for run in p.runs:
                            run.font.size = CONTENT_FONT_SIZE
                            run.font.color.rgb = TEXT_COLOR
    
    prs.save(output_file)


# Handle command line arguments
if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        # Default filenames if not provided
        input_file = "slides.md"
        output_file = "slides.pptx"
        
    try:
        # Read markdown content
        with open(input_file, 'r') as f:
            markdown_content = f.read()
        
        # Create slides
        create_professional_slides(markdown_content, output_file)
        print(f"Successfully created professional slides: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
