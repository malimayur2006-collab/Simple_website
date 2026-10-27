import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Job, Application, PrepTopic, PrepQuestion, Company, DSAProblem, UserProgress, QuizAttempt
from seed_data import seed_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-career-portal-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_database()

# ----------------- PAGE ROUTES ----------------- #

@app.route('/')
def index():
    featured_jobs = Job.query.filter_by(featured=True).limit(4).all()
    if not featured_jobs:
        featured_jobs = Job.query.limit(4).all()
    
    companies = Company.query.limit(4).all()
    prep_topics = PrepTopic.query.limit(4).all()
    
    # DSA stats
    total_dsa = DSAProblem.query.count()
    solved_dsa = UserProgress.query.filter_by(is_solved=True).count()
    dsa_percent = round((solved_dsa / total_dsa * 100) if total_dsa > 0 else 0)
    
    total_jobs = Job.query.count()
    total_apps = Application.query.count()

    return render_template(
        'index.html',
        featured_jobs=featured_jobs,
        companies=companies,
        prep_topics=prep_topics,
        total_dsa=total_dsa,
        solved_dsa=solved_dsa,
        dsa_percent=dsa_percent,
        total_jobs=total_jobs,
        total_apps=total_apps
    )

@app.route('/jobs')
def jobs():
    category = request.args.get('category', '').strip()
    job_type = request.args.get('type', '').strip()
    experience = request.args.get('exp', '').strip()
    query = request.args.get('q', '').strip()

    q = Job.query
    if category:
        q = q.filter(Job.category == category)
    if job_type:
        q = q.filter(Job.job_type == job_type)
    if experience:
        q = q.filter(Job.experience == experience)
    if query:
        search_filter = f"%{query}%"
        q = q.filter(
            (Job.title.ilike(search_filter)) |
            (Job.company.ilike(search_filter)) |
            (Job.skills.ilike(search_filter)) |
            (Job.location.ilike(search_filter))
        )

    all_jobs = q.order_by(Job.id.desc()).all()
    categories = [c[0] for c in db.session.query(Job.category).distinct()]
    job_types = [t[0] for t in db.session.query(Job.job_type).distinct()]
    experiences = [e[0] for e in db.session.query(Job.experience).distinct()]

    return render_template(
        'jobs.html',
        jobs=all_jobs,
        selected_cat=category,
        selected_type=job_type,
        selected_exp=experience,
        search_query=query,
        categories=categories,
        job_types=job_types,
        experiences=experiences
    )

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    similar_jobs = Job.query.filter(Job.category == job.category, Job.id != job.id).limit(3).all()
    return render_template('job_detail.html', job=job, similar_jobs=similar_jobs)

@app.route('/prep')
def prep():
    category = request.args.get('category', 'aptitude').lower()
    sub = request.args.get('sub', '').lower()

    # Available categories
    topics_query = PrepTopic.query
    if category:
        topics_query = topics_query.filter_by(category=category)
    if sub:
        topics_query = topics_query.filter_by(sub_category=sub)

    topics = topics_query.all()
    questions = PrepQuestion.query.filter_by(category=category).all()
    
    # Sub-category lists for filters
    aptitude_subs = ["quantitative", "logical", "verbal"]
    technical_subs = ["os", "dbms", "cn", "oop"]
    hr_subs = ["hr-common", "hr-behavioral"]

    return render_template(
        'prep.html',
        category=category,
        current_sub=sub,
        topics=topics,
        questions=questions,
        aptitude_subs=aptitude_subs,
        technical_subs=technical_subs,
        hr_subs=hr_subs
    )

@app.route('/prep/<slug>')
def prep_detail(slug):
    topic = PrepTopic.query.filter_by(slug=slug).first_or_404()
    related_questions = PrepQuestion.query.filter_by(sub_category=topic.sub_category).limit(5).all()
    other_topics = PrepTopic.query.filter(PrepTopic.category == topic.category, PrepTopic.id != topic.id).limit(4).all()
    return render_template('prep_detail.html', topic=topic, related_questions=related_questions, other_topics=other_topics)

@app.route('/companies')
def companies():
    category = request.args.get('category', '').strip()
    query = request.args.get('q', '').strip()

    q = Company.query
    if category:
        q = q.filter(Company.category == category)
    if query:
        q = q.filter(Company.name.ilike(f"%{query}%") | Company.tagline.ilike(f"%{query}%"))

    all_companies = q.all()
    categories = [c[0] for c in db.session.query(Company.category).distinct()]

    return render_template(
        'companies.html',
        companies=all_companies,
        categories=categories,
        selected_cat=category,
        query=query
    )

@app.route('/companies/<slug>')
def company_detail(slug):
    company = Company.query.filter_by(slug=slug).first_or_404()
    all_companies = Company.query.filter(Company.id != company.id).limit(3).all()
    return render_template('company_detail.html', company=company, other_companies=all_companies)

@app.route('/dsa')
def dsa():
    topics = [
        "Arrays",
        "Two Pointers & Sliding Window",
        "Strings",
        "Linked Lists",
        "Stacks & Queues",
        "Binary Search",
        "Trees & Binary Search Trees",
        "Graphs",
        "Dynamic Programming",
        "Greedy & Bit Manipulation",
        "Recursion & Backtracking",
        "Heaps & Priority Queues"
    ]
    
    # Load all problems and attach progress
    problems = DSAProblem.query.order_by(DSAProblem.order_index).all()
    progress_map = {p.problem_id: p for p in UserProgress.query.all()}

    # Compute overall statistics
    total_count = len(problems)
    solved_count = sum(1 for p in problems if progress_map.get(p.id) and progress_map[p.id].is_solved)
    percentage = round((solved_count / total_count * 100) if total_count > 0 else 0)

    # Compute topic stats
    topic_stats = {}
    for t in topics:
        probs = [p for p in problems if p.topic == t]
        tot = len(probs)
        sol = sum(1 for p in probs if progress_map.get(p.id) and progress_map[p.id].is_solved)
        topic_stats[t] = {
            'total': tot,
            'solved': sol,
            'percent': round((sol / tot * 100) if tot > 0 else 0)
        }

    # Clean JSON for client-side problem solution viewer & notes
    problems_dict = {p.id: p.to_dict(progress_map.get(p.id)) for p in problems}
    problems_json = json.dumps(problems_dict)

    return render_template(
        'dsa.html',
        topics=topics,
        problems=problems,
        progress_map=progress_map,
        total_count=total_count,
        solved_count=solved_count,
        percentage=percentage,
        topic_stats=topic_stats,
        problems_json=problems_json
    )

@app.route('/dashboard')
def dashboard():
    applications = Application.query.order_by(Application.created_at.desc()).all()
    
    total_dsa = DSAProblem.query.count()
    solved_dsa = UserProgress.query.filter_by(is_solved=True).count()
    revision_dsa = UserProgress.query.filter_by(is_revision=True).count()
    dsa_percent = round((solved_dsa / total_dsa * 100) if total_dsa > 0 else 0)

    quiz_attempts = QuizAttempt.query.order_by(QuizAttempt.created_at.desc()).limit(10).all()

    return render_template(
        'dashboard.html',
        applications=applications,
        total_dsa=total_dsa,
        solved_dsa=solved_dsa,
        revision_dsa=revision_dsa,
        dsa_percent=dsa_percent,
        quiz_attempts=quiz_attempts
    )

# ----------------- REST API ENDPOINTS ----------------- #

@app.route('/api/jobs', methods=['POST'])
def api_post_job():
    data = request.json or request.form
    try:
        new_job = Job(
            title=data.get('title'),
            company=data.get('company'),
            company_logo=data.get('company_logo', ''),
            location=data.get('location'),
            job_type=data.get('job_type', 'Full-Time'),
            experience=data.get('experience', 'Fresher (0-1 yrs)'),
            salary=data.get('salary', 'Competitive'),
            description=data.get('description', ''),
            requirements=data.get('requirements', ''),
            responsibilities=data.get('responsibilities', ''),
            skills=data.get('skills', ''),
            eligibility=data.get('eligibility', ''),
            deadline=data.get('deadline', 'Open until filled'),
            category=data.get('category', 'Software Development'),
            featured=bool(data.get('featured', False))
        )
        db.session.add(new_job)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Job posted successfully!', 'job': new_job.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def api_apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json or request.form
    try:
        app_entry = Application(
            job_id=job.id,
            applicant_name=data.get('applicant_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            college=data.get('college'),
            grad_year=data.get('grad_year'),
            experience=data.get('experience'),
            resume_link=data.get('resume_link'),
            github_url=data.get('github_url'),
            linkedin_url=data.get('linkedin_url'),
            cover_note=data.get('cover_note'),
            status='Applied'
        )
        db.session.add(app_entry)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Application for {job.title} at {job.company} submitted successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/dsa/toggle-solved', methods=['POST'])
def api_toggle_dsa_solved():
    data = request.json
    problem_id = data.get('problem_id')
    prob = DSAProblem.query.get_or_404(problem_id)
    
    prog = UserProgress.query.filter_by(problem_id=problem_id).first()
    if not prog:
        prog = UserProgress(problem_id=problem_id, is_solved=True)
        db.session.add(prog)
    else:
        prog.is_solved = not prog.is_solved
    
    db.session.commit()

    total_dsa = DSAProblem.query.count()
    solved_dsa = UserProgress.query.filter_by(is_solved=True).count()
    dsa_percent = round((solved_dsa / total_dsa * 100) if total_dsa > 0 else 0)

    return jsonify({
        'success': True,
        'is_solved': prog.is_solved,
        'total': total_dsa,
        'solved': solved_dsa,
        'percent': dsa_percent
    })

@app.route('/api/dsa/toggle-revision', methods=['POST'])
def api_toggle_dsa_revision():
    data = request.json
    problem_id = data.get('problem_id')
    prob = DSAProblem.query.get_or_404(problem_id)

    prog = UserProgress.query.filter_by(problem_id=problem_id).first()
    if not prog:
        prog = UserProgress(problem_id=problem_id, is_revision=True)
        db.session.add(prog)
    else:
        prog.is_revision = not prog.is_revision

    db.session.commit()
    return jsonify({'success': True, 'is_revision': prog.is_revision})

@app.route('/api/dsa/save-note', methods=['POST'])
def api_save_dsa_note():
    data = request.json
    problem_id = data.get('problem_id')
    note_text = data.get('note', '')

    prog = UserProgress.query.filter_by(problem_id=problem_id).first()
    if not prog:
        prog = UserProgress(problem_id=problem_id, notes=note_text)
        db.session.add(prog)
    else:
        prog.notes = note_text

    db.session.commit()
    return jsonify({'success': True, 'message': 'Personal notes updated!'})

@app.route('/api/quiz/questions', methods=['GET'])
def api_quiz_questions():
    category = request.args.get('category', 'aptitude')
    sub = request.args.get('sub_category')
    
    q = PrepQuestion.query.filter_by(category=category)
    if sub:
        q = q.filter_by(sub_category=sub)
    
    questions = q.all()
    return jsonify([q.to_dict() for q in questions])

@app.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    data = request.json
    answers = data.get('answers', {}) # {question_id: selected_option}
    category = data.get('category', 'General')
    sub_category = data.get('sub_category', 'General')

    score = 0
    total = len(answers)
    results = []

    for qid_str, selected in answers.items():
        qid = int(qid_str)
        question = PrepQuestion.query.get(qid)
        if question:
            is_correct = (selected == question.correct_option)
            if is_correct:
                score += 1
            results.append({
                'id': qid,
                'question': question.question,
                'selected': selected,
                'correct': question.correct_option,
                'is_correct': is_correct,
                'explanation': question.explanation
            })

    percent = round((score / total * 100), 1) if total > 0 else 0

    attempt = QuizAttempt(
        category=category,
        sub_category=sub_category,
        score=score,
        total=total,
        percentage=percent
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'success': True,
        'score': score,
        'total': total,
        'percentage': percent,
        'results': results
    })

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({'results': []})

    results = []
    # Search jobs
    jobs = Job.query.filter(Job.title.ilike(f"%{q}%") | Job.company.ilike(f"%{q}%")).limit(4).all()
    for j in jobs:
        results.append({
            'type': 'Job',
            'title': f"{j.title} at {j.company}",
            'url': url_for('job_detail', job_id=j.id),
            'badge': j.salary
        })

    # Search companies
    comps = Company.query.filter(Company.name.ilike(f"%{q}%")).limit(4).all()
    for c in comps:
        results.append({
            'type': 'Company',
            'title': f"{c.name} Hiring Process & Syllabus",
            'url': url_for('company_detail', slug=c.slug),
            'badge': c.category
        })

    # Search prep topics
    preps = PrepTopic.query.filter(PrepTopic.title.ilike(f"%{q}%")).limit(4).all()
    for p in preps:
        results.append({
            'type': 'Preparation',
            'title': p.title,
            'url': url_for('prep_detail', slug=p.slug),
            'badge': p.category.upper()
        })

    # Search DSA problems
    dsas = DSAProblem.query.filter(DSAProblem.title.ilike(f"%{q}%") | DSAProblem.topic.ilike(f"%{q}%")).limit(4).all()
    for d in dsas:
        results.append({
            'type': 'DSA Problem',
            'title': f"{d.title} ({d.topic})",
            'url': url_for('dsa') + f"#{d.id}",
            'badge': d.difficulty
        })

    return jsonify({'results': results})

if __name__ == '__main__':
    # Local development server
    app.run(debug=True, host='127.0.0.1', port=5000)
