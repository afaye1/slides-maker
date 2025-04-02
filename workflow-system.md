# MBA Study Group Workflow System

## Overview
This document outlines the systematic workflow for preparing and conducting MBA study group sessions for the Strategic Management course.

## File Structure and Organization

### Markdown Content Files (Teaching Materials)
- Unit1-markdown.md
- Unit2-markdown.md
- Unit3-markdown.md
- Unit4-markdown.md
- Unit5-markdown.md

### Quiz Files (Assessment Materials)
- Unit1-quiz.json
- Unit2-quiz.json
- Unit3-quiz.json
- Unit4-quiz.json
- Unit5-quiz.json

### Python Scripts
- create_slides.py - Converts markdown to PowerPoint slides
- quiz_to_slides.py - Converts quiz JSON to slides for interactive sessions

## Weekly Preparation Workflow

### 1. Content Preparation (3-4 days before Saturday session)
- Review unit materials from course documents
- Update or create markdown content files with key concepts
- Structure content in slide-ready format with clear section breaks
- Add practical examples and discussion prompts
- Generate quiz questions for pre/post assessment

### 2. Slide Generation (2 days before Saturday session)
```bash
# Generate main content slides
python create_slides.py UnitX-markdown.md UnitX-slides.pptx

# Generate quiz slides
python quiz_to_slides.py UnitX-quiz.json UnitX-quiz-slides.pptx
```

### 3. Session Planning (1 day before Saturday session)
- Review generated slides
- Prepare facilitator notes for each section
- Plan timing for each segment (content, discussion, quiz)
- Prepare any additional materials (case studies, exercises)
- Upload materials to Discord for early access

## Session Structure (90 minutes - Saturday)

### 1. Welcome and Pre-Quiz (15 minutes)
- Welcome and agenda overview (2 min)
- Pre-quiz to assess baseline knowledge (10 min)
- Brief discussion of pre-quiz results (3 min)

### 2. Content Presentation (40 minutes)
- Present main concepts from slides (30 min)
- Incorporate real-world examples (5 min)
- Clarify questions (5 min)

### 3. Break (5 minutes)

### 4. Interactive Application (25 minutes)
- Group discussion or case study analysis
- Practical application of concepts
- Small group breakouts if attendance is high

### 5. Post-Quiz and Wrap-up (15 minutes)
- Post-quiz to measure learning (10 min)
- Preview next session (3 min)
- Administrative announcements (2 min)

## Mid-week Check-in Structure (60 minutes - Wednesday)

### 1. Quick Review (15 minutes)
- Recap key concepts from Saturday
- Address any follow-up questions

### 2. Discussion of Application (30 minutes)
- Discuss how concepts apply in practical settings
- Share insights from additional readings/materials
- Work through challenging aspects

### 3. Preview and Preparation (15 minutes)
- Preview upcoming Saturday session
- Assign any preparation tasks
- Open forum for questions

## Post-Session Tasks

### 1. Documentation (Within 24 hours after session)
- Upload session recording to YouTube
- Post summary notes to Discord
- Share any additional resources mentioned

### 2. Assessment and Iteration (Within 48 hours)
- Review quiz results to identify knowledge gaps
- Note areas that generated most questions/confusion
- Adjust upcoming session plans based on feedback

## Technical Requirements

### Software Dependencies
```
python-pptx==0.6.21
markdown==3.4.3
```

### Platform Access
- Ensure Discord server access for all participants
- Maintain YouTube channel for recordings
- Have Google Meet links ready for live sessions

## Continuous Improvement

After each full unit cycle:
1. Collect feedback from participants
2. Assess engagement and learning outcomes
3. Refine content and delivery methods
4. Update workflow process as needed

This systematic approach ensures consistent, high-quality study sessions while maximizing learning effectiveness within the time constraints.
