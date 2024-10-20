**Overview:**
ClassMonitor is a dynamic and robust student and classroom management system built with Django. It enables efficient management of students, assignments, and classroom activities, offering features for teachers to streamline their workflow. The system includes functionality for students to track their progress and stay updated on assignments and class-related activities.

The project implements the MVC (Model-View-Controller) architecture pattern with a user-friendly interface, ensuring smooth navigation across different features. It also integrates authentication and role-based access control, enhancing security and accessibility for both teachers and students.

**Key Features:**
Student Profiles: Manage student information, track attendance, and display their assignments and classroom activities.
Assignment Management: Teachers can upload assignments, while students can track submission statuses and deadlines.
Classroom Assignment: Real-time tracking of class activities, assignment submissions, and class performance.
Role-Based Access Control (RBAC): Separate access levels for teachers and students.
Efficient URL Mapping and Error Handling: Used Django's urls.py and reverse() for dynamic URL management.

**Technologies Used:**
**Backend:**
Django Framework: For rapid backend development and ORM integration.
Django URL Mapping: Utilized Django’s reverse() and NoReverseMatch exception handling for seamless navigation and error prevention.

**Frontend:**
HTML/CSS: For designing the front-end views and templates.
Bootstrap: To create a responsive and mobile-friendly UI.

**Database:**
SQLite (default Django database): To store student information, assignments, and classroom data. Can be easily upgraded to PostgreSQL or MySQL for production.

**Authentication:**
Django’s Auth System: For user login, registration, and role-based access control (RBAC).

**Notable Implementations:**
Error Handling: Implemented robust exception handling for errors such as NoReverseMatch, RecursionError, and user attribute access failures.
Optimized Views: Created separate views for teachers and students, ensuring efficient data access.
Custom User Model: Extended Django’s default user model to accommodate student and teacher profiles.

**Challenges Solved:**
Reverse URL Matching: Overcame challenges related to NoReverseMatch by properly registering namespaces and URLs.
Recursion Depth Issues: Handled RecursionError by refactoring method calls to avoid deep recursion loops.
Student-User Attribute: Addressed attribute issues by improving user model relations in Django’s ORM.

**Future Enhancements:**
Real-Time Notifications: Integrate real-time assignment submission notifications using WebSockets or Django Channels.
API Integration: Add REST API endpoints using Django REST Framework for better scalability and third-party integration.
Deployment: Plan to deploy the system on cloud platforms like Heroku or AWS etc.


**How to Run the Project:**

**1.Clone the repository:**
git clone https://github.com/yourusername/classmonitor.git

**2.Install dependencies:**
pip install -r requirements.txt

**3.Run migrations:**
python manage.py makemigrations
python manage.py migrate

**4.Create a superuser (admin):**
python manage.py createsuperuser

**5.Run the server:**
python manage.py runserver

**6.Access the app at** http://127.0.0.1:8000/
