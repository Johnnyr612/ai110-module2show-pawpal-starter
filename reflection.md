# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
+------------------+        1       * +------------------+
|      Owner       |------------------|       Pet        |
|------------------|                  |------------------|
| - name           |                  | - name           |
| - preferences    |                  | - species        |
|------------------|                  |------------------|
| + get_info()     |                  | + get_info()     |
+------------------+                  +------------------+
        ^                                      |
        |                                      |
        |                                      |
        | 1                                    * |
        |                                      |
+------------------+                  +------------------+
|    Scheduler     |<-----------------|      Task        |
|------------------|                  |------------------|
| + generate_plan()|                  | - title          |
| + explain_plan() |                  | - duration       |
|                  |                  | - priority       |
|------------------|                  |------------------|
|                  |                  | + get_info()     |
+------------------+                  +------------------+
- What classes did you include, and what responsibilities did you assign to each?
Classes include Owner, Pet, Task, and Scheduler. Pet and Tasks are related, Scheduler depends on Task, and Owner uses Scheduler. Owner can have many Pet and Pets can have more than one Task. Each class has self explanitory methods that correlate to class.

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
I simplified the relationshsips between the classes and made everything output in the Scheduler class(Final plan).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers task time first, since the main goal is to build a daily care plan that is easy to follow. It also accounts for whether a task is recurring, whether it is already completed, and which pet the task belongs to.
- How did you decide which constraints mattered most?
I decided that time was the most important constraint because the app is organizing when care tasks should happen. Recurring tasks and conflict detection were also important because they affect whether the schedule is realistic. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is that it prioritizes time-based organization over more complex decision-making. For example, it will sort tasks by scheduled time and warn about conflicts, but it does not fully optimize the plan for things like urgency or duration.
- Why is that tradeoff reasonable for this scenario?
It's reasonable for this scenario because the main goal of the app is to create a simple, understandable daily care schedule for a pet owner. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
AI was useful in getting a fast understanding of the logic and functionality of the project. If i had further questions about the files, i would attach the file as context and ask specific questions.
- What kinds of prompts or questions were most helpful?
Prompts like, 'give me a thorough explination of the methods inside pawpal_system.py and the logic behind them'. Prompts like this would help me understand the bigger picture faster.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I had to ask follow-up question when trying to map out the initial UML becuase I noticed it was not being accurate and vague at times.
- How did you evaluate or verify what the AI suggested?
I would read the explinations the chatbot gave and then verify with my own eyes if it is true or not. The pytest was also a helpful measure when verifying new outputs.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion and status, adding tasks to pets, sorting tasks by pet and completion status, and detect schduling conflicts.
- Why were these tests important?
These tasks were important because they verified the main functions of the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
The scheduler works correctly for sure, i tested it.
- What edge cases would you test next if you had more time?
I would include a test case for handling an empty scheduler or invalid/missing time values.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm satified with completing the `pawpal_system.py` file with correct logic that makes the app run nice.

**b. What you would improve**
I would include a mechanism that flags a scheduling conflict before the user generates the schedule so the user knows if there will be a scheduling conflic before the the generation.

- If you had another iteration, what would you improve or redesign?
I would definitely improve the UI icons and their placements. Other than that, i liked the app icon(paws).

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
It's nice to have a visual like a UML to see what talks to what. It's a nice upgrade from just having to read comments.
