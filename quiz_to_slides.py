import json
import sys
import os
import subprocess

def convert_quiz_to_markdown(quiz_json_file, output_md_file):
    """
    Converts a quiz JSON file to markdown format compatible with create_slides.py
    One question per slide with proper formatting
    """
    # Read the quiz JSON file
    with open(quiz_json_file, 'r') as f:
        quiz_data = json.load(f)
    
    # Start building markdown content
    markdown_content = []
    
    # Title slide
    markdown_content.append("# Quiz: Strategic Management")
    markdown_content.append("Pre-quiz and Post-quiz")
    
    # Pre-quiz introduction slide
    markdown_content.append("---")
    markdown_content.append("## Pre-Quiz (5 minutes)")
    markdown_content.append("")
    markdown_content.append("Answer these questions to assess your current knowledge.")
    
    # Create one slide per pre-quiz question
    for i, q in enumerate(quiz_data["pre_quiz"], 1):
        markdown_content.append("---")
        markdown_content.append(f"## Pre-Quiz: Question {i}")
        markdown_content.append("")
        markdown_content.append(f"{q['question_text']}")
        markdown_content.append("")
        markdown_content.append(f"a) {q['options']['a']}")
        markdown_content.append(f"b) {q['options']['b']}")
        markdown_content.append(f"c) {q['options']['c']}")
        markdown_content.append(f"d) {q['options']['d']}")
    
    # Post-quiz introduction slide
    markdown_content.append("---")
    markdown_content.append("## Post-Quiz (5 minutes)")
    markdown_content.append("")
    markdown_content.append("Now that we've completed our session, test your understanding.")
    
    # Create one slide per post-quiz question
    for i, q in enumerate(quiz_data["post_quiz"], 1):
        markdown_content.append("---")
        markdown_content.append(f"## Post-Quiz: Question {i}")
        markdown_content.append("")
        markdown_content.append(f"{q['question_text']}")
        markdown_content.append("")
        markdown_content.append(f"a) {q['options']['a']}")
        markdown_content.append(f"b) {q['options']['b']}")
        markdown_content.append(f"c) {q['options']['c']}")
        markdown_content.append(f"d) {q['options']['d']}")
    
    # Add answer key slide for instructor reference
    markdown_content.append("---")
    markdown_content.append("## Answer Key (Instructor Only)")
    markdown_content.append("")
    markdown_content.append("Pre-Quiz:")
    for i, q in enumerate(quiz_data["pre_quiz"], 1):
        markdown_content.append(f"{i}. {q['correct_answer']}")
    
    markdown_content.append("")
    markdown_content.append("Post-Quiz:")
    for i, q in enumerate(quiz_data["post_quiz"], 1):
        markdown_content.append(f"{i}. {q['correct_answer']}")
    
    # Write the markdown content to a file
    with open(output_md_file, 'w') as f:
        f.write('\n'.join(markdown_content))
    
    return output_md_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python quiz_to_slides.py quiz.json [output.pptx]")
        sys.exit(1)
    
    # Get input file
    quiz_json_file = sys.argv[1]
    
    # Set output filename if provided, otherwise use default
    if len(sys.argv) >= 3:
        output_pptx = sys.argv[2]
    else:
        # Use the same name as the input file but with .pptx extension
        output_pptx = os.path.splitext(quiz_json_file)[0] + '.pptx'
    
    # Generate temporary markdown file
    temp_md_file = os.path.splitext(quiz_json_file)[0] + '_temp.md'
    
    # Convert JSON to markdown
    convert_quiz_to_markdown(quiz_json_file, temp_md_file)
    
    # Call the create_slides.py script to generate PowerPoint
    try:
        subprocess.run([sys.executable, 'create_slides.py', temp_md_file, output_pptx], check=True)
        print(f"Successfully created quiz slides: {output_pptx}")
        
        # Clean up the temporary markdown file
        os.remove(temp_md_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running create_slides.py: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()