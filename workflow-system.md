# Automated MBA Study Group Workflow - Setup Guide

This guide explains how to set up and use the automated workflow system for generating study materials for any MBA course.

## System Overview

The automated system consists of:

1. **Content Generation** - Creates markdown slide content and quizzes
2. **Slide Conversion** - Converts the content into PowerPoint presentations
3. **Workflow Management** - Organizes all materials for a structured study approach

## Files in the System

- `modular_prompt.txt` - Template for AI content generation
- `auto_generate_content.py` - Main script that orchestrates the process
- `create_slides.py` - Converts markdown to PowerPoint slides
- `quiz_to_slides.py` - Converts JSON quizzes to PowerPoint
- `README.md` - Overall project documentation

## Setup Instructions

### 1. Install Required Packages

```bash
pip install python-pptx==0.6.21 markdown==3.4.3
```

If you want to use the OpenAI integration:
```bash
pip install openai
```

### 2. Prepare Your Course Materials

1. Place your course study guide in a folder (this is required)
2. Place any lesson documents in a folder (optional but recommended)

### 3. Run the Automated Process

The system can run in two modes:

#### Without API Key (Manual AI Interaction)

```bash
python auto_generate_content.py --study-guide path/to/study_guide.md --lessons-dir path/to/lessons --output-dir output --unit 2
```

This will:
1. Extract Unit 2 information from the study guide
2. Create a prompt file in the output directory
3. You'll need to manually use this prompt with an AI tool
4. Save the AI outputs as directed in the terminal output

#### With API Key (Fully Automated)

```bash
python auto_generate_content.py --study-guide path/to/study_guide.md --lessons-dir path/to/lessons --output-dir output --unit_number --api-key your_openai_api_key
```

This will:
1. Extract unit_number information from the study guide
2. Use the OpenAI API to generate content
3. Save markdown and quiz files
4. Automatically convert them to PowerPoint presentations

### 4. Process All Units at Once

To generate materials for all units in the course:

```bash
python auto_generate_content.py --study-guide path/to/study_guide.md --lessons-dir path/to/lessons --output-dir output --all --api-key your_openai_api_key
```

## Folder Structure

After running the process, your output directory will contain:

```
output/
├── unit1-markdown.md       # Slide content in markdown
├── unit1-quiz.json         # Quiz questions in JSON
├── unit1-slides.pptx       # Main presentation
├── unit1-quiz.pptx         # Quiz presentation
├── unit2-markdown.md
├── unit2-quiz.json
...etc
```

## Customization Options

### Modifying the Prompt Template

Edit `modular_prompt.txt` to change how content is generated:

- Adjust formatting instructions
- Change slide types
- Modify quiz structure
- Add specific requirements for your course

### Customizing Slide Design

The slide generation system uses basic PowerPoint templates. For more advanced designs:

1. Create a custom PowerPoint template (.pptx)
2. Use it with the slide generator:
   ```bash
   python create_slides_updated.py input_dir output_dir your_template.pptx
   ```

## Troubleshooting

### Common Issues:

1. **No units found in study guide**
   - Ensure your study guide uses headers like "Unit X: Title" or "Section X: Title"

2. **Content generation fails**
   - Check your API key
   - Look for specific error messages
   - Try the manual approach by using the generated prompt

3. **Slide conversion fails**
   - Check that python-pptx is properly installed
   - Verify the markdown follows the expected format

## Workflow Integration

This automated system works best when integrated with a study group workflow:

1. Run the generation process 3-4 days before your session
2. Review and refine the generated materials
3. Upload presentations to your online platforms
4. Use the main slides for Saturday sessions
5. Use quiz slides for pre/post assessment

## Support

If you encounter issues or need help customizing this workflow, check the documentation or reach out via the Discord community.