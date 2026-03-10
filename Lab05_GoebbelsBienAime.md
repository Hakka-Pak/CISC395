# Lab 5: AI Agents - Terminal-Based AI Operations
## CISC 395 - Applied Generative AI and LLM Applications

**Due:** [Date specified on Blackboard]

**Submission:** Upload to Blackboard — `Lab05_YourName.md` + generated files (see checklist)

---

## Prerequisites

**Complete before the lab begins.**

### Set Up Your Workspace and Download Lab Files

Open VS Code, then open the `CISC395/` folder (`File > Open Folder`). Open the integrated terminal (`` Ctrl+Shift+` `` on Windows, `` Cmd+Shift+` `` on Mac). Run:

```bash
mkdir Lab05
cd Lab05

# Download (curl is built-in on Mac and Windows 10/11)
curl -o Lab05.zip "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab05/Lab05.zip"

# Unzip (Mac / Linux)
unzip Lab05.zip

# Unzip (Windows)
tar -xf Lab05.zip

cd ..
```

Verify structure from the workspace root:

```bash
tree Lab05        # Mac/Linux
tree /F Lab05     # Windows
```

Expected:
```
Lab05/
├── data/
│   └── student_grades.csv
├── code/
│   ├── calculator.py
│   └── buggy_sort.py
├── messy/
│   └── [10 poorly-named files]
└── papers/
    └── [research paper PDF]
```

---

## Overview

| Exercise | Topic | Deliverable |
|----------|-------|-------------|
| 1 | Workspace Setup and Context File | `GEMINI.md` + answers in this file |
| 2 | AI-Powered Paper Reading | `papers/paper_summary.md` + answers in this file |
| 3 | Grade Data Analysis | `data/grade_report.md` + answers in this file |
| 4 | Digital Organization Challenge | reorganized `messy/` + answers in this file |
| Reflection | | answers in this file |

**No coding required.** All exercises use terminal AI sessions.

**How to enter a session:**
```bash
gemini       # Gemini CLI
copilot      # GitHub Copilot CLI
```

---

## Exercise 1: Workspace Setup and Context File (20 points)

### Part A: Enter Your First Session

Navigate into `Lab05/` and start a session:

```bash
cd Lab05
gemini
```

Approve the folder trust prompt when it appears.

**Screenshot:** Take a screenshot of the session start (`screenshot_01.png`).

---

### Part B: Create Your GEMINI.md

Inside the session, ask AI to draft a `GEMINI.md` context file for this project and save it:

**The prompt you used:**
```
[Paste your exact prompt here]

draft a 'GEMINI.md'  context file for this project and save it
```

After saving, verify it loaded:
```
> /memory show
```

**`/memory show` output (first 3–5 lines is enough):**
```
[Paste just enough to confirm the context file was loaded]

memory is currently empty.
```

> `GEMINI.md` will be submitted as a separate file — do not paste its full content here.

---

### Part C: Test Your Context

With `GEMINI.md` loaded, ask AI about `code/buggy_sort.py` — without describing it yourself:

```
> Look at code/buggy_sort.py and explain what it does. Is there a bug?
```

**AI's response:**
```
[Paste the full response here]

✦ code/buggy_sort.py is a Python script designed as a debugging exercise. It contains four common algorithms, each with intentional    
  logical errors for AI or students to identify and fix:


   1. `bubble_sort(arr)`: Has an off-by-one error in the inner loop range.
   2. `binary_search(arr, target)`: Contains two bugs: an incorrect initial right boundary and a missing increment when updating the   
      left pointer.
   3. `count_occurrences(arr, target)`: Has an out-of-bounds error in the loop range.
   4. `remove_duplicates(lst)`: Incorrectly checks for existence in the original list instead of the result list.


  The file includes a __main__ block to demonstrate these functions, which will currently produce errors or incorrect results when     
  executed.                              

```

**Reflection:** Did AI correctly identify the bug without any hints? Did having `GEMINI.md` make a difference compared to asking cold? (2–3 sentences)

```
[Your answer]

Comparing both scenarios I would say that there would not be much of a difference if the file was there or not for the AI to identify the bug, I feel that the AI would still be aware of this possible bug and Identify several causes. 
```

---

## Exercise 2: AI-Powered Paper Reading (30 points)

### Required Sections

Your `paper_summary.md` must contain all five sections:

| # | Section | What it should cover |
|---|---------|----------------------|
| 1 | **Introduction** | What the paper proposes and its key contribution |
| 2 | **Core Principles** | The key technical idea or methodology |
| 3 | **Impact and Influence** | Why this paper matters and how widely adopted |
| 4 | **Influence on Modern AI** | How the paper's ideas appear in today's systems |
| 5 | **Relevance to Your Major** | How this connects to your major/career — your own words |

### Write and Run Your Prompt

Write a prompt that reads the PDF, applies at least two techniques from Units 2–3, requires all five sections, and saves the result as `papers/paper_summary.md`.

**Your prompt:**
```
[Write your complete prompt here]

You are a college student in your senior year.

you will be writing a structured paper that goes in specific format

1) the introduction of the paper and what it entails while citing key information.
2) the principles and explaining what the technical ideas and methodology mean.
3) what is the purpose of the paper and how can it be widely used.
4) How this paper can have an affect on modern technology with the use of AI agents.
5) lastly, how is this paper relevant to a student who's major is Computer Information Systems. 

Techniques used: [e.g., "Role Prompting + Structured Output"]
```

> `papers/paper_summary.md` will be submitted as a separate file — do not paste its content here.

**Reflection:**

1. Which section did AI handle best? Which was weakest? Why? (2–3 sentences)

```
[Your answer]

Impact on modern technology and AI agents. personally I think the Introduction was the weakest. reason why I say this is because the other section captures the important detail of the paper of how technology has transformed, without the introduction I am certain someone would grab what the paper is about.
```

2. Did you need to refine your prompt or ask follow-up questions? What worked and what did not? (2–3 sentences)

```
[Your answer]

I did not have to refine the prompt. everything worked as it should, the AI gave a well structured response on the paper exactly how I Instructed it to format the paper. 
```

---

## Exercise 3: Grade Data Analysis (25 points)

### Part A: Explore the Data

Ask at least three different questions about `data/student_grades.csv`. For each, paste your prompt and the AI's response.

**Suggested questions (choose 3 or write your own):**
- What is the grade distribution (A/B/C/D/F)?
- Who are the top 3 students by total score?
- Which students are at risk (below 70%)?
- What is the class average, highest, and lowest score?

---

**Question 1 — Your prompt:**
```
[Paste your prompt]
What is the grade distribution (A/B/C/D/F)?

Look into the `data/student_grades.csv` and tell me what is the grade distribution of
a student having (A/B/C/D/F)
```
**AI's response:**
```
[Paste response]

──────────────────┬───────┬─────────────────────────────────────────────────────────────────────────────────────────┐
  │ Grade Category    │ Count │ Students                                                                                │
  ├───────────────────┼───────┼─────────────────────────────────────────────────────────────────────────────────────────┤
  │ A (A, A-)     │ 6     │ Carol Williams, Frank Martinez, James Wilson, Mia Jackson, Olivia Harris, Rachel Walker │
  │ B (B+, B, B-) │ 5     │ Alice Chen, David Lee, Henry Brown, Quinn Lewis, Tina Young                             │
  │ C (C+, C)     │ 3     │ Grace Kim, Kate Anderson, Noah White                                                    │
  │ D (D+, D)     │ 4     │ Bob Johnson, Iris Taylor, Peter Clark, Sam Hall                                         │
  │ F             │ 2     │ Emma Davis, Liam Thomas                                                                 │
  └───────────────────┴───────┴─────────────────────────────────────────────────────────────────────────────────────────┘


  Summary:
   - A: 30%
   - B: 25%
   - C: 15%
   - D: 20%
   - F: 10%
```

---

**Question 2 — Your prompt:**
```
[Paste your prompt]
Who are the top 3 students by total score?

Go into the `data/student_grades.csv` and look at all the studets scores, tell me who are the top 3 students by total score.   
```
**AI's response:**
```
[Paste response]

✦ The top 3 students by total score in data/student_grades.csv are:


   1. James Wilson (97.1)
   2. Olivia Harris (96.5)
   3. Carol Williams (96.1)
```

---

**Question 3 — Your prompt:**
```
[Paste your prompt]
What is the class average, highest, and lowest score?

Look in the `data/student_grades.csv` give me a structured and ordered format of the following outputs:
1. The class average score
2. The class highest score
3. The class lowest score
```
**AI's response:**
```
[Paste response]

✦ Based on the data in student_grades.csv, here are the class statistics for the total score:


   1. Class Average Score: 79.60
   2. Class Highest Score: 97.1 (James Wilson)
   3. Class Lowest Score: 55.8 (Emma Davis)
```

---

### Part B: Generate a Grade Report

Ask AI to synthesize findings into `data/grade_report.md` (class stats, top performers, students needing support, one recommendation).

**Your prompt:**
```
[Paste your prompt here]

You are a researcher who has vast knowledge in various topics.

You will use your knowledge to gather and examine information from the data/student_grades.csv and create a `data/grade_report.md` where you will provide the following:
1. Class statistics.
2. The class top performers.
3. Students that needs support due to a low grade, less than 70.
4. A recommendation of how the class can perform better overall.

```

**Verify the file was created** (paste one line of terminal output):
```
[e.g.,   dir data   →   student_grades.csv   grade_report.md]

✦ The Lab05/data directory contains the following files:
   - grade_report.md (The report I just created)
   - student_grades.csv (The original grades dataset)
```

> `data/grade_report.md` will be submitted as a separate file — do not paste its content here.

---

## Exercise 4: Digital Organization Challenge (15 points)

### Part A: Show the Current State

Run `dir messy` (Windows) or `ls messy` (Mac/Linux) and paste the output:

```
[Paste terminal output showing all 10 files]

 ✓  ReadFolder Lab05/messy                                                                                                       │    
│                                                                                                                                 │    
│ Listed 10 item(s).                                                                                                              │    
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯    
✦ The Lab05/messy directory contains 10 files with disorganized naming conventions, including .txt, .csv, and .py files. Based on the
  GEMINI.md mandates, I should propose a reorganization plan before moving them.
```

---

### Part B: Ask AI to Propose an Organization Plan

Ask AI to analyze `messy/`, propose a folder structure as a tree diagram, assign each file to a subfolder with a reason, and suggest better names — **without moving anything yet**.

**Your prompt:**
```
[Paste your prompt here]

Analyze the `messy/` and propose a structure that is a tree diagram, make sure to assign each file to a subfolder with a reason and suggest better names without moving anything yet.

```

**AI's proposed plan:**
```
[Paste the tree structure, file assignments, and naming suggestions]


✦ Based on my analysis of the file contents, I propose the following reorganization for the messy/ directory:


    1 messy/
    2 ├── assignments/             (Formal submissions and homework)
    3 │   ├── lab03_submission.txt        <-- 20241103_assignment_submission_DONE.txt
    4 │   └── assignment01_submission.txt <-- hw1 FINAL(2) v3.txt
    5 ├── notes/                   (Class notes, ideas, and presentation materials)
    6 │   ├── prompt_eng_week02.txt       <-- Copy of notes week2(1).txt
    7 │   ├── final_project_ideas.txt     <-- Untitled Document (3).txt
    8 │   └── week04_demo_script.txt      <-- NEW new version script REVISED.txt
    9 ├── reports/                 (Progress and status reports)
   10 │   └── week03_progress_report.txt  <-- report draft REAL one.docx.txt
   11 ├── scripts/                 (Python code and utility scripts)
   12 │   ├── hello_world.py              <-- temp.py
   13 │   └── simple_addition.py          <-- untitled1.py
   14 ├── data/                    (Raw data and CSV files)
   15 │   └── small_score_sheet.csv       <-- asdfghjkl.csv
   16 └── archive/                 (Old or redundant files)
  Rationale:
   - assignments/: Groups all work intended for submission to keep it separate from rough notes.
   - notes/: Captures ideas and classroom learning materials.
   - reports/: Specifically for periodic status updates.
   - scripts/: Separates functional Python code from text-based documentation.
   - data/: Isolates structured data files.
   - archive/: Moves "junk" or backup files out of the active workspace without deleting them yet.


  Suggested Renaming: I have replaced vague names like Untitled Document (3) and asdfghjkl with descriptive names that reflect the     
  actual content found inside the files.


  Would you like me to proceed with creating these folders and moving/renaming the files accordingly?
```

---

### Part C: Evaluate and Implement

**Your evaluation:** Do you agree with the plan? What would you change? (2–3 sentences)

```
[Your answer]

I can say I agree with some portions of how the files are named and layed out, However I feel that their could have been a better improvement of the overall structure. I feel that each chapter should have the assignments and notes within that folder, following the other files or scripts. 
```

Ask AI to execute the plan. Show the result:

```bash
tree messy        # Mac/Linux
tree /F messy     # Windows
```

**`tree messy` output after reorganization:**
```
[Paste here]

✦ I will now display the tree structure of the reorganized messy/ directory to verify the file movements and renaming.

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮    
│ ✓  Shell tree /F Lab05/messy [current working directory C:\Users\gibbe\OneDrive\Desktop\CISC395] (Display the tree structure o… │    
│                                                                                                                                 │    
│ ... first 10 lines hidden (Ctrl+O to show) ...                                                                                  │    
│ ├───data                                                                                                                        │    
│ │       small_score_sheet.csv                                                                                                   │    
│ │                                                                                                                               │    
│ ├───notes                                                                                                                       │    
│ │       final_project_ideas.txt                                                                                                 │    
│ │       prompt_eng_week02.txt                                                                                                   │    
│ │       week04_demo_script.txt                                                                                                  │    
│ │                                                                                                                               │    
│ ├───reports                                                                                                                     │    
│ │       week03_progress_report.txt                                                                                              │    
│ │                                                                                                                               │    
│ └───scripts                                                                                                                     │    
✦ The reorganization of the messy/ directory is complete. Each file has been renamed for clarity and placed in its respective subfolder
  based on its content.
```

---

## Reflection (10 points)

**1. Session vs. Single Command**

This lab used session-based interaction where AI built up context across multiple messages. How did that change the quality of results compared to asking one-off questions? Give a specific example from your session. (3–4 sentences)

```
[Your answer]

By using the session based interaction with AI, it is like you are engaging in a conversation with a person. the reason why I say this is because I felt that the AI was less confused and was able to keep a working memory of what was asked of it. The exercise with the student grades where I provided the AI with the class grades and
the AI agent was able to recall and pull the data and turn it into a md report file.
```

**2. Permissions**

Describe one moment where AI asked your permission before taking an action. What did it want to do, and did you review the content before approving? (2–3 sentences)

```
[Your answer]

There was multiple instances during the session where I used commands in order to complete a task, and the AI did provide me with choices if I only wanted to allow this once, during the session, or not at all. I briefly reviewed the content and only allowed it for the current session, nothing beyond. 
```

**3. One Real Use Case**

Name one task from your actual student or professional life that you will use terminal AI for after this lab. Be specific: what folder, what prompt, what output. (2–3 sentences)

```
[Your answer]

This is my first time actually using AI on a terminal, I most likely would probably be using it for class assignments or projects to see what else I can do with it and how far it can go. In terms of a folder I would classify it as 'school projects', for a prompt, something along the lines of projects that covers the materials with each chapter, the output would be formatted, making it easier to read and follow. 
```

---

## Submission Checklist

**Upload all of the following to Blackboard:**

- [ ] `Lab05_YourName.md` — this file, fully filled in
- [ ] `GEMINI.md` — your context file (from Exercise 1B)
- [ ] `papers/paper_summary.md` — AI-generated paper summary (from Exercise 2)
- [ ] `data/grade_report.md` — AI-generated grade report (from Exercise 3B)
- [ ] `screenshot_01.png` — session start screenshot (from Exercise 1A)

> The reorganized `messy/` folder is verified by the `tree` output pasted in Exercise 4C — no separate upload needed.

---

## Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Exercise 1** | **20** | |
| Screenshot (session start) | 5 | Screenshot shows successful session with folder authorization |
| Prompt + `/memory show` | 8 | Prompt is complete; `/memory show` confirms context loaded |
| Code context test | 7 | AI response pasted; reflection shows understanding of why context helps |
| **Exercise 2** | **30** | |
| Prompt design (2+ techniques) | 10 | Techniques named and correctly applied |
| `paper_summary.md` (submitted file) | 15 | All 5 sections present and substantive; Section 5 in student's own words |
| Reflection | 5 | Honest evaluation of AI output quality |
| **Exercise 3** | **25** | |
| 3 prompts + AI responses | 15 | Questions are specific; responses are accurate and informative |
| `grade_report.md` (submitted file) | 10 | Report includes stats, insights, and a recommendation |
| **Exercise 4** | **15** | |
| Before state shown | 3 | All 10 files visible in terminal output |
| Organization prompt + AI plan | 8 | Plan is logical; student evaluates it critically |
| Tree output after reorganization | 4 | Files moved and renamed; folder structure visible |
| **Reflection** | **10** | |
| Session context reflection | 4 | Specific example cited |
| Permissions moment | 3 | Concrete example from the session |
| Future use case | 3 | Realistic and specific |
| **Total** | **100** | |

---

## Common Commands Reference

**Navigation**

| Task | Windows | Mac / Linux |
|------|---------|-------------|
| Show current path | `cd` | `pwd` |
| Go into a folder | `cd Lab05` | `cd Lab05` |
| Go up one level | `cd ..` | `cd ..` |
| List files | `dir` | `ls` |
| List a subfolder | `dir data` | `ls data` |
| Show folder tree | `tree /F` | `tree` |

**Gemini CLI**

| Command | What it does |
|---------|--------------|
| `gemini` | Enter an interactive session |
| `/memory show` | Display loaded GEMINI.md context |
| `/memory refresh` | Reload GEMINI.md after editing |
| `/compress` | Compress long conversation |
| `/quit` | Exit the session |

**GitHub Copilot CLI**

| Command | What it does |
|---------|--------------|
| `copilot` | Enter an interactive session |
| `/compact` | Compress long conversation |
| `/quit` | Exit the session |

---

**Estimated time:** 90 minutes in class, with optional finishing at home

**End of Lab 5**
