# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
A user should be able to add tasks to a to-do list for specific days of the week, add a pet, and schedule times to do certain tasks while being able to filter out any time contraints they have.
- What classes did you include, and what responsibilities did you assign to each?
Owner class: stores user info and preferences
Pet class: represents pet(s) and its care needs
Task class: represents a care activity with duration and priority
Planner class: generates a daily schedule based on tasks and constraints

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
I added a Schedule class so Planner.generate_schedule could return a schedule, and I added a pets attribute to Owner to represent the “has many Pets” relationship. These changes kept the original design but ensured the code was valid and matched the UML.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Priority (highest first), scheduled time, completion status, pet name, due date, and frequency (daily/weekly).

- How did you decide which constraints mattered most?
Priority matters most (it's applied first in generate_schedule()). Time and pet filtering are secondary, called explicitly only when needed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is that it only checks for exact time matches, not overlapping durations
- Why is that tradeoff reasonable for this scenario?
It makes making tasks fast and simple (jut hash tasks by time string) so it works well for a lightweight MVP or when tasks are deliberately scheduled on different hour boundaries.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI for brainstorming scheduling algorithms, implementing new methods like sorting and filtering, debugging runtime errors in the Streamlit app, refactoring code for better structure, writing comprehensive tests, improving the UI with professional components, and documenting features in the README.
- What kinds of prompts or questions were most helpful?
Simple, specific prompts like "add a sorting method by time" or "fix this AttributeError" were most helpful. Open-ended questions like "suggest small algorithms for pet scheduling" helped with initial ideas.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When AI suggested a complex duration-based conflict detection algorithm, I chose a simpler exact-time matching approach instead.
- How did you evaluate or verify what the AI suggested?
I evaluated suggestions by checking if they fit the MVP scope, testing the code to ensure it works, and verifying logic against the UML design and user requirements.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested sorting tasks by time (including edge cases like missing times), automatic recurrence for daily/weekly tasks, conflict detection for overlapping schedules, and core functionality like task completion and pet management.
- Why were these tests important?
These tests were important to verify that the scheduling algorithms work correctly, handle edge cases, and maintain data integrity across different scenarios.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I'm almost 100% confident that my scheduler works because the core algorithms work reliably for the implemented features.
- What edge cases would you test next if you had more time?
I'd test overlapping task durations, scheduling across multiple pets simultaneously, and handling very large numbers of tasks for performance.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with implementing the intelligent scheduling algorithms and creating a professional, working Streamlit app with comprehensive tests.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
To improve/redeign, I'd add duration-based conflict detection, implement owner preference constraints, and enhance the UI with task editing and deletion capabilities.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned designing system with AI collaboration helps to quicken development. AI helps rapidly prototype ideas, but human judgment is still necessary for choosing appropriate tradeoffs and verifying that the code is correct.
