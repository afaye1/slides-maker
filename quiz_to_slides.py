import json
import sys
import os
import glob
import subprocess

def convert_quiz_to_markdown(quiz_json_file, output_md_file, title=None):
    """
    Converts a quiz JSON file to markdown format compatible with create_slides.py
    One question per slide with proper formatting
    
    Args:
        quiz_json_file (str): Path to the quiz JSON file
        output_md_file (str): Path for the output markdown file
        title (str, optional): Title to use for the quiz (if not provided, extracted from filename)
    """
    # Read the quiz JSON file
    with open(quiz_json_file, 'r') as f:
        quiz_data = json.load(f)
    
    # Extract course and unit info from filename if title not provided
    if title is None:
        base_name = os.path.basename(quiz_json_file)
        # Try to extract unit number from filename
        unit_match = re.search(r'unit[\-_]?(\d+)', base_name.lower())
        if unit_match:
            unit_num = unit_match.group(1)
            title = f"Unit {unit_num} Assessment"
        else:
            # Use filename without extension
            title = os.path.splitext(base_name)[0].replace("_", " ").replace("-", " ").title()
    
    # Start building markdown content
    markdown_content = []
    
    # Title slide
    markdown_content.append(f"# {title}")
    markdown_content.append("Pre-quiz and Post-quiz")
    
    # Pre-quiz introduction slide
    markdown_content.append("---")
    markdown_content.append("## Pre-Quiz (5 minutes)")
    markdown_content.append("")
    markdown_content.append("Answer these questions to assess your current knowledge.")
    
    # Create one slide per pre-quiz question
    for i, q in enumerate(quiz_data.get("pre_quiz", []), 1):
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
    for i, q in enumerate(quiz_data.get("post_quiz", []), 1):
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
    for i, q in enumerate(quiz_data.get("pre_quiz", []), 1):
        markdown_content.append(f"{i}. {q.get('correct_answer', '?')}")
    
    markdown_content.append("")
    markdown_content.append("Post-Quiz:")
    for i, q in enumerate(quiz_data.get("post_quiz", []), 1):
        markdown_content.append(f"{i}. {q.get('correct_answer', '?')}")
    
    # Write the markdown content to a file
    with open(output_md_file, 'w') as f:
        f.write('\n'.join(markdown_content))
    
    return output_md_file


def process_all_quiz_files(input_dir=None, output_dir=None):
    """
    Process all JSON quiz files in the input directory and convert them to markdown and PowerPoint
    
    Args:
        input_dir (str, optional): Directory containing JSON quiz files (default: current dir)
        output_dir (str, optional): Directory for output files (default: current dir)
    """
    if input_dir is None:
        input_dir = os.getcwd()
    
    if output_dir is None:
        output_dir = os.getcwd()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all JSON files that seem to be quizzes
    quiz_files = []
    for json_file in glob.glob(os.path.join(input_dir, "*.json")):
        # Check if it's a quiz file by looking for typical quiz structure
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if "pre_quiz" in data or "post_quiz" in data:
                    quiz_files.append(json_file)
        except:
            pass  # Not a valid JSON or not a quiz file
    
    if not quiz_files:
        print(f"No quiz JSON files found in {input_dir}")
        return
    
    for quiz_file in quiz_files:
        base_name = os.path.basename(quiz_file)
        base_name_no_ext = os.path.splitext(base_name)[0]
        temp_md_file = os.path.join(output_dir, f"{base_name_no_ext}_temp.md")
        output_pptx = os.path.join(output_dir, f"{base_name_no_ext}.pptx")
        
        try:
            # Convert JSON to markdown
            convert_quiz_to_markdown(quiz_file, temp_md_file)
            
            # Check if create_slides.py is in the same directory
            create_slides_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_slides.py")
            if not os.path.exists(create_slides_script):
                create_slides_script = "create_slides.py"  # Assume it's in PATH
            
            # Call the create_slides.py script to generate PowerPoint
            subprocess.run([sys.executable, create_slides_script, temp_md_file, output_pptx], check=True)
            print(f"Successfully created quiz slides: {output_pptx}")
            
            # Clean up the temporary markdown file
            os.remove(temp_md_file)
        except Exception as e:
            print(f"Error processing {quiz_file}: {str(e)}")


def main():
    import re
    
    if len(sys.argv) == 1:
        # No arguments, process all quiz files in current directory
        process_all_quiz_files()
    elif len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Usage:")
        print("  python quiz_to_slides.py                      # Process all quiz JSON files in current directory")
        print("  python quiz_to_slides.py quiz.json [output.pptx]  # Process a single quiz file")
        print("  python quiz_to_slides.py input_dir output_dir     # Process all quiz files in input_dir")
    elif len(sys.argv) == 2:
        # One argument, process a single quiz file
        quiz_json_file = sys.argv[1]
        if not os.path.isfile(quiz_json_file):
            print(f"Error: {quiz_json_file} is not a file.")
            sys.exit(1)
        
        # Use the same name as the input file but with .pptx extension
        output_pptx = os.path.splitext(quiz_json_file)[0] + '.pptx'
        
        # Generate temporary markdown file
        temp_md_file = os.path.splitext(quiz_json_file)[0] + '_temp.md'
        
        # Convert JSON to markdown
        convert_quiz_to_markdown(quiz_json_file, temp_md_file)
        
        # Call the create_slides.py script to generate PowerPoint
        try:
            create_slides_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_slides.py")
            if not os.path.exists(create_slides_script):
                create_slides_script = "create_slides.py"  # Assume it's in PATH
                
            subprocess.run([sys.executable, create_slides_script, temp_md_file, output_pptx], check=True)
            print(f"Successfully created quiz slides: {output_pptx}")
            
            # Clean up the temporary markdown file
            os.remove(temp_md_file)
        except subprocess.CalledProcessError as e:
            print(f"Error running create_slides.py: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    elif len(sys.argv) == 3:
        # Two arguments, could be:
        # 1. Single file conversion: quiz.json output.pptx
        # 2. Batch processing: input_dir output_dir
        if os.path.isfile(sys.argv[1]):
            # Single file conversion
            quiz_json_file = sys.argv[1]
            output_pptx = sys.argv[2]
            
            # Generate temporary markdown file
            temp_md_file = os.path.splitext(quiz_json_file)[0] + '_temp.md'
            
            # Convert JSON to markdown
            convert_quiz_to_markdown(quiz_json_file, temp_md_file)
            
            # Call the create_slides.py script to generate PowerPoint
            try:
                create_slides_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_slides.py")
                if not os.path.exists(create_slides_script):
                    create_slides_script = "create_slides.py"  # Assume it's in PATH
                    
                subprocess.run([sys.executable, create_slides_script, temp_md_file, output_pptx], check=True)
                print(f"Successfully created quiz slides: {output_pptx}")
                
                # Clean up the temporary markdown file
                os.remove(temp_md_file)
            except subprocess.CalledProcessError as e:
                print(f"Error running create_slides.py: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        elif os.path.isdir(sys.argv[1]):
            # Batch processing
            input_dir = sys.argv[1]
            output_dir = sys.argv[2]
            
            process_all_quiz_files(input_dir, output_dir)
        else:
            print(f"Error: {sys.argv[1]} is neither a file nor a directory.")
            sys.exit(1)
    else:
        print("Usage: python quiz_to_slides.py quiz.json [output.pptx]")
        print("       python quiz_to_slides.py input_dir output_dir")
        sys.exit(1)

if __name__ == "__main__":
    main()