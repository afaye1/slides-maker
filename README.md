# MBA Study Group - Strategic Management

This repository contains all materials for the Strategic Management MBA study group sessions.

## Overview

These materials support a 10-week study program covering the five units of Strategic Management, with:
- 90-minute main sessions (Saturdays)
- 60-minute mid-week check-ins (Wednesdays)

## Repository Structure

### Content Files
- `unitX-markdown.md` - Slide content for each unit in markdown format
- `unitX-quiz.json` - Pre/post quiz questions for each unit in JSON format

### Python Scripts
- `create_slides.py` - Converts markdown files to PowerPoint presentations
- `quiz_to_slides.py` - Converts quiz JSON files to PowerPoint quiz slides

### Documentation
- `workflow-system.md` - Complete process for session preparation and execution
- `README.md` - This overview file

## How to Use These Materials

### Generating Presentations

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Generate content slides**:
   ```
   python create_slides.py unitX-markdown.md unitX-slides.pptx
   ```

3. **Generate quiz slides**:
   ```
   python quiz_to_slides.py unitX-quiz.json unitX-quiz.pptx
   ```

### Recommended Session Structure

#### Saturday Main Sessions (90 min)
- Welcome & Pre-Quiz (15 min)
- Content Presentation (40 min)
- Break (5 min)
- Interactive Application (25 min)
- Post-Quiz & Wrap-up (15 min)

#### Wednesday Check-ins (60 min)
- Quick Review (15 min)
- Discussion & Application (30 min)
- Preview & Preparation (15 min)

## Unit Content Overview

1. **Unit 1: Introduction to Strategy**
   - Strategy definitions
   - Strategic hierarchy
   - Market structures

2. **Unit 2: Strategic Planning**
   - Organizational goals
   - Internal & external analysis
   - Strategic management tools

3. **Unit 3: Creating Competitive Advantage**
   - Competitive advantage concepts
   - Value creation factors
   - Total Quality Management

4. **Unit 4: Corporate Strategy**
   - Growth strategies
   - Contraction strategies
   - Strategy evaluation

5. **Unit 5: 21st-Century Strategy**
   - Global strategic management
   - Innovation & technology
   - Strategic agility

## Additional Resources

- Discord server: discord.gg/h9qaMtC4HV
- YouTube channel: www.youtube.com/@SaylorAcademyMBAStudyGroup

## Contributing

Study group members are encouraged to:
- Submit corrections or improvements
- Share additional resources
- Provide feedback on session content

## Contact

For questions or support, please contact us on the Discord server.
