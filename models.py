import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    company_logo = db.Column(db.String(300), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # Full-Time, Internship, Remote, Contract
    experience = db.Column(db.String(50), nullable=False) # Fresher (0-1 yrs), 1-3 yrs, 3-5 yrs
    salary = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True) # newline separated
    responsibilities = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(255), nullable=False) # comma separated
    eligibility = db.Column(db.String(255), nullable=True)
    apply_url = db.Column(db.String(300), nullable=True)
    deadline = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(80), nullable=False) # Software Development, AI/ML, Cloud, Data, QA
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'company_logo': self.company_logo,
            'location': self.location,
            'job_type': self.job_type,
            'experience': self.experience,
            'salary': self.salary,
            'description': self.description,
            'requirements': [r.strip() for r in self.requirements.split('\n') if r.strip()] if self.requirements else [],
            'responsibilities': [r.strip() for r in self.responsibilities.split('\n') if r.strip()] if self.responsibilities else [],
            'skills': [s.strip() for s in self.skills.split(',') if s.strip()],
            'eligibility': self.eligibility,
            'deadline': self.deadline,
            'category': self.category,
            'featured': self.featured,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applicant_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    college = db.Column(db.String(150), nullable=True)
    grad_year = db.Column(db.String(20), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    resume_link = db.Column(db.String(300), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    cover_note = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Applied') # Applied, In Review, Shortlisted, Interview Scheduled, Offer
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else 'Unknown',
            'company': self.job.company if self.job else 'Unknown',
            'applicant_name': self.applicant_name,
            'email': self.email,
            'phone': self.phone,
            'college': self.college,
            'grad_year': self.grad_year,
            'experience': self.experience,
            'resume_link': self.resume_link,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'cover_note': self.cover_note,
            'status': self.status,
            'created_at': self.created_at.strftime('%b %d, %Y') if self.created_at else ''
        }

class PrepTopic(db.Model):
    __tablename__ = 'prep_topics'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # aptitude, technical, hr
    sub_category = db.Column(db.String(50), nullable=False) # quantitative, logical, verbal, os, dbms, cn, oop, hr-common
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False) # HTML/Markdown formatted notes & formulas
    read_time = db.Column(db.String(30), default='8 min read')
    icon = db.Column(db.String(50), default='book')

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'sub_category': self.sub_category,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'content': self.content,
            'read_time': self.read_time,
            'icon': self.icon
        }

class PrepQuestion(db.Model):
    __tablename__ = 'prep_questions'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # aptitude, technical, hr
    sub_category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_option = db.Column(db.String(10), nullable=False) # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='Medium') # Easy, Medium, Hard

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'sub_category': self.sub_category,
            'question': self.question,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_option': self.correct_option,
            'explanation': self.explanation,
            'difficulty': self.difficulty
        }

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False) # Service Based, Product Based, Tech Giant, FinTech
    logo_color = db.Column(db.String(50), default='bg-blue-600')
    tagline = db.Column(db.String(255), nullable=True)
    ctc_range = db.Column(db.String(100), nullable=False) # e.g. "₹3.5 LPA - ₹11.5 LPA"
    eligibility_summary = db.Column(db.String(255), nullable=False)
    difficulty_level = db.Column(db.String(30), default='Medium')
    
    # In-depth structured sections stored as JSON or formatted text
    packages_json = db.Column(db.Text, nullable=True) # profiles & CTC list
    eligibility_json = db.Column(db.Text, nullable=True) # detailed criteria
    rounds_json = db.Column(db.Text, nullable=True) # Round 1 to N details
    exam_pattern_json = db.Column(db.Text, nullable=True) # Sections, duration, marking
    syllabus_json = db.Column(db.Text, nullable=True) # Topic wise syllabus
    interview_tips = db.Column(db.Text, nullable=True) # Key prep strategies
    sample_questions = db.Column(db.Text, nullable=True) # Frequently asked questions

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'category': self.category,
            'logo_color': self.logo_color,
            'tagline': self.tagline,
            'ctc_range': self.ctc_range,
            'eligibility_summary': self.eligibility_summary,
            'difficulty_level': self.difficulty_level,
            'packages': json.loads(self.packages_json) if self.packages_json else [],
            'eligibility': json.loads(self.eligibility_json) if self.eligibility_json else {},
            'rounds': json.loads(self.rounds_json) if self.rounds_json else [],
            'exam_pattern': json.loads(self.exam_pattern_json) if self.exam_pattern_json else [],
            'syllabus': json.loads(self.syllabus_json) if self.syllabus_json else {},
            'interview_tips': json.loads(self.interview_tips) if self.interview_tips and self.interview_tips.startswith('[') else self.interview_tips,
            'sample_questions': json.loads(self.sample_questions) if self.sample_questions and self.sample_questions.startswith('[') else self.sample_questions
        }

class DSAProblem(db.Model):
    __tablename__ = 'dsa_problems'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(80), nullable=False) # Arrays, Two Pointers, Strings, Linked Lists, etc.
    title = db.Column(db.String(180), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False) # Easy, Medium, Hard
    leetcode_url = db.Column(db.String(255), nullable=True)
    gfg_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    approach = db.Column(db.Text, nullable=True)
    time_complexity = db.Column(db.String(80), nullable=True)
    space_complexity = db.Column(db.String(80), nullable=True)
    code_python = db.Column(db.Text, nullable=True)
    code_cpp = db.Column(db.Text, nullable=True)
    code_java = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, default=0)

    progress = db.relationship('UserProgress', backref='problem', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, user_status=None):
        return {
            'id': self.id,
            'topic': self.topic,
            'title': self.title,
            'difficulty': self.difficulty,
            'leetcode_url': self.leetcode_url,
            'gfg_url': self.gfg_url,
            'description': self.description,
            'approach': self.approach,
            'time_complexity': self.time_complexity,
            'space_complexity': self.space_complexity,
            'code_python': self.code_python,
            'code_cpp': self.code_cpp,
            'code_java': self.code_java,
            'order_index': self.order_index,
            'is_solved': user_status.is_solved if user_status else False,
            'is_revision': user_status.is_revision if user_status else False,
            'user_notes': user_status.notes if user_status else ''
        }

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('dsa_problems.id'), nullable=False)
    is_solved = db.Column(db.Boolean, default=False)
    is_revision = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
