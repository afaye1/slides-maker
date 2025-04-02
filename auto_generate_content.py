import os
import sys
import glob
import re
import json
import subprocess
import argparse
from datetime import datetime

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def extract_units_from_study_guide(study_guide_path):
    """Extract unit information from study guide file"""
    try:
        with open(study_guide_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for unit headers
        unit_matches = re.findall(r'#+\s+Unit\s+(\d+):\s+(.*?)(?=\n)', content, re.IGNORECASE)
        
        if not unit_matches:
            print("No unit headers found in study guide. Looking for section headers...")
            # Try alternative formats like "Section X: Title"
            unit_matches = re.findall(r'#+\s+(?:Section|Module|Part)\s+(\d+):\s+(.*?)(?=\n)', content, re.IGNORECASE)
        
        units = []
        for number, title in unit_matches:
            units.append({
                'number': number,
                'title': title.strip()
            })
        
        # Extract course code and title if available
        course_match = re.search(r'#+\s+([A-Z]+\d+):\s+(.*?)(?=\n)', content)
        course_info = {}
        if course_match:
            course_info['code'] = course_match.group(1)
            course_info['title'] = course_match.group(2).strip()
        
        return units, course_info
    except Exception as e:
        print(f"Error extracting units from study guide: {e}")
        return [], {}

def generate_content_for_unit(unit, course_info, study_guide_path, lesson_path, output_dir, api_key=None):
    """Generate content for a unit using AI"""
    print(f"Generating content for Unit {unit['number']}: {unit['title']}...")
    
    # Create prompt from template
    with open('modular_prompt.txt', 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Replace placeholders
    prompt = prompt_template.replace('[UNIT_NUMBER]', unit['number'])
    prompt = prompt.replace('[UNIT_TITLE]', unit['title'])
    
    # Add course info if available
    if course_info.get('code'):
        prompt = prompt.replace('[COURSE_CODE]', course_info.get('code'))
        prompt = prompt.replace('[COURSE_TITLE]', course_info.get('title'))
    else:
        # Use defaults if course info not available
        prompt = prompt.replace('[COURSE_CODE]', 'MBA Course')
        prompt = prompt.replace('[COURSE_TITLE]', 'Business Administration')
    
    # Prepare study materials to include with the prompt
    study_materials = ""
    
    # Add relevant content from study guide
    try:
        with open(study_guide_path, 'r', encoding='utf-8') as f:
            study_guide_content = f.read()
        
        # Try to extract just the section for this unit
        unit_pattern = rf"#+\s+Unit\s+{unit['number']}:.*?(?=#+\s+Unit\s+\d+:|$)"
        unit_content = re.search(unit_pattern, study_guide_content, re.DOTALL)
        
        if unit_content:
            study_materials += "===== STUDY GUIDE CONTENT =====\n"
            study_materials += unit_content.group(0) + "\n\n"
        else:
            study_materials += "===== STUDY GUIDE CONTENT =====\n"
            study_materials += study_guide_content + "\n\n"
    except Exception as e:
        print(f"Warning: Could not extract from study guide: {e}")
    
    # Add relevant content from lesson document if available
    if lesson_path and os.path.exists(lesson_path):
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                lesson_content = f.read()
            
            study_materials += "===== LESSON CONTENT =====\n"
            study_materials += lesson_content + "\n\n"
        except Exception as e:
            print(f"Warning: Could not extract from lesson document: {e}")
    
    # Full prompt with materials
    full_prompt = prompt + "\n\n" + study_materials
    
    # You'll need to replace this with your actual AI integration
    if api_key:
        # Add your API-based AI implementation here
        # Example with OpenAI (you'd need to add the openai package)
        try:
            import openai
            openai.api_key = api_key
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional curriculum developer with expertise in MBA courses."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            ai_content = response.choices[0].message.content
            
            # Extract markdown and JSON content
            md_match = re.search(r'```markdown(.*?)```', ai_content, re.DOTALL)
            json_match = re.search(r'```json(.*?)```', ai_content, re.DOTALL)
            
            if md_match:
                md_content = md_match.group(1).strip()
            else:
                # Try to extract markdown content without code blocks
                # This is a fallback method if the AI doesn't use code blocks
                lines = ai_content.split('\n')
                md_content = []
                json_section = False
                
                for line in lines:
                    if line.strip().startswith('{') and '"pre_quiz":' in line:
                        json_section = True
                        continue
                    if json_section and line.strip().endswith('}'):
                        json_section = False
                        continue
                    if not json_section and not line.startswith('quiz_') and '```' not in line:
                        md_content.append(line)
                
                md_content = '\n'.join(md_content)
            
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Try to extract JSON content
                json_section = re.search(r'(\{[\s\S]*"pre_quiz"[\s\S]*"post_quiz"[\s\S]*\})', ai_content)
                if json_section:
                    json_content = json_section.group(1)
                else:
                    print("Warning: Could not extract JSON quiz content")
                    json_content = """
                    {
                      "pre_quiz": [
                        {
                          "question_text": "Placeholder question 1",
                          "options": {
                            "a": "Option A",
                            "b": "Option B",
                            "c": "Option C",
                            "d": "Option D"
                          },
                          "correct_answer": "a"
                        }
                      ],
                      "post_quiz": [
                        {
                          "question_text": "Placeholder question 1",
                          "options": {
                            "a": "Option A",
                            "b": "Option B",
                            "c": "Option C",
                            "d": "Option D"
                          },
                          "correct_answer": "a"
                        }
                      ]
                    }
                    """
            
        except ImportError:
            print("OpenAI package not installed. Please install with: pip install openai")
            return None, None
        except Exception as e:
            print(f"Error generating content with AI: {e}")
            return None, None
    else:
        # Fallback to simpler approach - save the prompt to a file and let user manually get AI response
        prompt_file = os.path.join(output_dir, f"unit{unit['number']}_prompt.txt")
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(full_prompt)
        
        print(f"Prompt saved to {prompt_file}")
        print("Please use this prompt with your preferred AI tool and save the outputs as:")
        print(f"  - unit{unit['number']}-markdown.md")
        print(f"  - unit{unit['number']}-quiz.json")
        
        return None, None
    
    # Save content to files
    md_file = os.path.join(output_dir, f"unit{unit['number']}-markdown.md")
    json_file = os.path.join(output_dir, f"unit{unit['number']}-quiz.json")
    
    try:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)
            
        print(f"Created markdown file: {md_file}")
        print(f"Created quiz file: {json_file}")
        
        return md_file, json_file
    except Exception as e:
        print(f"Error saving generated content: {e}")
        return None, None

def process_unit(unit, course_info, study_guide_path, lessons_dir, output_dir, api_key=None):
    """Process a single unit - generate content and convert to slides"""
    # Find lesson document for this unit if available
    lesson_path = None
    if lessons_dir and os.path.exists(lessons_dir):
        # Look for files with unit number in name
        pattern = os.path.join(lessons_dir, f"*unit*{unit['number']}*")
        matches = glob.glob(pattern, recursive=False)
        
        if not matches:
            # Try different pattern formats
            pattern = os.path.join(lessons_dir, f"*{unit['number']}*")
            matches = glob.glob(pattern, recursive=False)
        
        if matches:
            lesson_path = matches[0]
            print(f"Found lesson document: {lesson_path}")
    
    # Generate content
    md_file, json_file = generate_content_for_unit(
        unit, course_info, study_guide_path, lesson_path, output_dir, api_key
    )
    
    if md_file and os.path.exists(md_file):
        # Convert markdown to slides
        slides_output = os.path.join(output_dir, f"unit{unit['number']}-slides.pptx")
        try:
            subprocess.run([sys.executable, "create_slides_updated.py", md_file, slides_output], check=True)
            print(f"Successfully created slides: {slides_output}")
        except Exception as e:
            print(f"Error creating slides: {e}")
    
    if json_file and os.path.exists(json_file):
        # Convert quiz to slides
        quiz_output = os.path.join(output_dir, f"unit{unit['number']}-quiz.pptx")
        try:
            subprocess.run([sys.executable, "quiz_to_slides_updated.py", json_file, quiz_output], check=True)
            print(f"Successfully created quiz slides: {quiz_output}")
        except Exception as e:
            print(f"Error creating quiz slides: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generate MBA study materials from course documents')
    parser.add_argument('--study-guide', required=True, help='Path to the study guide document')
    parser.add_argument('--lessons-dir', help='Directory containing lesson documents')
    parser.add_argument('--output-dir', default='output', help='Directory to save generated content')
    parser.add_argument('--unit', type=int, help='Specific unit number to process')
    parser.add_argument('--api-key', help='OpenAI API key for content generation')
    parser.add_argument('--all', action='store_true', help='Process all units')
    
    args = parser.parse_args()
    
    # Create output directory
    create_directory_if_not_exists(args.output_dir)
    
    # Extract units from study guide
    units, course_info = extract_units_from_study_guide(args.study_guide)
    
    if not units:
        print("No units found in the study guide. Exiting.")
        sys.exit(1)
    
    print(f"Found {len(units)} units in the study guide:")
    for unit in units:
        print(f"  Unit {unit['number']}: {unit['title']}")
    
    # Process units
    if args.unit:
        # Process specific unit
        unit_to_process = next((u for u in units if u['number'] == str(args.unit)), None)
        if unit_to_process:
            process_unit(unit_to_process, course_info, args.study_guide, args.lessons_dir, args.output_dir, args.api_key)
        else:
            print(f"Unit {args.unit} not found in study guide.")
    elif args.all:
        # Process all units
        for unit in units:
            process_unit(unit, course_info, args.study_guide, args.lessons_dir, args.output_dir, args.api_key)
    else:
        print("Please specify --unit NUMBER to process a specific unit or --all to process all units.")
        print("Available units:")
        for unit in units:
            print(f"  Unit {unit['number']}: {unit['title']}")

if __name__ == "__main__":
    main()