import json
from models import db, Job, PrepTopic, PrepQuestion, Company, DSAProblem

def seed_database():
    # Check if database has jobs
    if not Job.query.first():
        print("Seeding initial Jobs...")
        seed_jobs()

    if not PrepTopic.query.first():
        print("Seeding Preparation Topics...")
        seed_prep_topics()

    if not PrepQuestion.query.first():
        print("Seeding Practice MCQs...")
        seed_questions()

    if not Company.query.first():
        print("Seeding Companies...")
        seed_companies()

    # Always ensure full set of DSA problems exist
    seed_dsa_problems()

    db.session.commit()
    print("Database seeding synchronization completed successfully!")

def seed_jobs():
    jobs_data = [
        {
            "title": "Software Development Engineer - I (SDE 1)",
            "company": "Amazon",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg",
            "location": "Bengaluru, Karnataka (Hybrid)",
            "job_type": "Full-Time",
            "experience": "Fresher (0-1 yrs)",
            "salary": "₹28,00,000 - ₹44,00,000 PA",
            "description": "Amazon is seeking exceptional Software Development Engineers (SDE I) to build massively scalable systems supporting millions of customers globally. You will design, build, and deploy high-concurrency microservices, optimize low-latency APIs, and collaborate with world-class engineering teams.",
            "requirements": "Proficiency in Java, C++, or Python\nStrong grasp of Data Structures, Algorithms, and Object-Oriented Design\nFamiliarity with distributed systems and AWS cloud primitives\nBachelor's or Master's degree in Computer Science or related engineering discipline\nDemonstrated problem-solving and clean coding skills",
            "responsibilities": "Design and implement scalable distributed services and customer-facing features\nWrite clean, well-tested, and maintainable production code\nParticipate in design reviews, sprint planning, and architectural discussions\nTroubleshoot production incidents and optimize operational performance",
            "skills": "Java, Python, C++, Data Structures, Algorithms, AWS, Distributed Systems, System Design",
            "eligibility": "B.Tech / B.E / M.Tech in CS/IT/ECE (2025/2026 Batch), 7.0+ CGPA",
            "deadline": "Nov 30, 2026",
            "category": "Software Development",
            "featured": True
        },
        {
            "title": "Graduate Software Engineer (TCS Digital / Prime)",
            "company": "Tata Consultancy Services (TCS)",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Tata_Consultancy_Services_Logo.svg",
            "location": "Multiple Locations (Pune, Chennai, Hyderabad, Bengaluru)",
            "job_type": "Full-Time",
            "experience": "Fresher (0 yrs)",
            "salary": "₹7,50,000 - ₹11,50,000 PA",
            "description": "TCS Digital and TCS Prime are elite engineering initiatives looking for next-generation talent passionate about Emerging Technologies like AI/ML, Cloud Native Architecture, Cyber Security, and Big Data Engineering.",
            "requirements": "Strong foundation in Core Java, Python, or C++\nSolid understanding of DBMS, SQL, and Operating Systems\nGood analytical thinking and problem-solving aptitude\nMinimum 60% or 6.0 CGPA throughout 10th, 12th, and Degree without active backlogs",
            "responsibilities": "Develop digital solutions utilizing modern web frameworks and cloud platforms\nCollaborate with international client teams on enterprise digital transformation projects\nWrite unit test suites and participate in code reviews",
            "skills": "Core Java, Python, SQL, Cloud Basics, Problem Solving, Data Structures",
            "eligibility": "B.E. / B.Tech / M.E. / M.Tech / MCA (2025 / 2026 batches)",
            "deadline": "Dec 15, 2026",
            "category": "Software Development",
            "featured": True
        },
        {
            "title": "Frontend React Developer",
            "company": "Zomato",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/7/75/Zomato_logo.png",
            "location": "Gurugram, Haryana (On-site)",
            "job_type": "Full-Time",
            "experience": "1-3 yrs",
            "salary": "₹16,00,000 - ₹24,00,000 PA",
            "description": "Join Zomato's consumer app web engineering team to craft blazing fast, responsive, and delightful user interfaces used by tens of millions of food lovers every day.",
            "requirements": "Strong mastery of JavaScript (ES6+), TypeScript, React.js, and Next.js\nDeep knowledge of State Management (Redux Toolkit, Zustand) and React Hooks\nProficiency in CSS3, Tailwind CSS, Web Performance Optimization, and Core Web Vitals\nExperience with RESTful APIs, WebSockets, and component testing (Jest/RTL)",
            "responsibilities": "Build and maintain responsive web pages and single-page applications\nImprove page load speeds, SEO performance, and responsive animations\nCollaborate closely with UI/UX designers and backend API engineers",
            "skills": "React.js, Next.js, TypeScript, Tailwind CSS, Redux, Performance Optimization, JavaScript",
            "eligibility": "Any Engineering Degree / BCA / MCA with strong React portfolio",
            "deadline": "Nov 20, 2026",
            "category": "Software Development",
            "featured": True
        },
        {
            "title": "Backend Engineer (Go / Python)",
            "company": "Razorpay",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/8/89/Razorpay_logo.svg",
            "location": "Bengaluru, Karnataka (Hybrid)",
            "job_type": "Full-Time",
            "experience": "1-3 yrs",
            "salary": "₹18,00,000 - ₹28,00,000 PA",
            "description": "Razorpay powers payments for millions of businesses. We are searching for backend engineers who enjoy building fault-tolerant transactional engines handling thousands of financial transactions per second.",
            "requirements": "Hands-on experience with Go (Golang) or Python/Django/FastAPI\nExperience with Relational Databases (PostgreSQL/MySQL) and Caching (Redis)\nGood understanding of message queues like Kafka or RabbitMQ\nSolid knowledge of Microservices, Docker, and Kubernetes",
            "responsibilities": "Design, develop, and maintain payment gateway pipelines and ledger systems\nEnsure 99.999% system availability and sub-100ms response times\nImplement automated integration and unit test coverage",
            "skills": "Go, Python, PostgreSQL, Redis, Kafka, Microservices, Docker, Docker/K8s",
            "eligibility": "B.Tech/B.E in CS/IT or relevant software engineering experience",
            "deadline": "Dec 05, 2026",
            "category": "Software Development",
            "featured": False
        },
        {
            "title": "AI & Machine Learning Engineering Intern",
            "company": "Microsoft",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
            "location": "Hyderabad / Bengaluru (Hybrid)",
            "job_type": "Internship",
            "experience": "Fresher (0 yrs)",
            "salary": "₹1,25,000 / month Stipend (PPO opportunity)",
            "description": "Microsoft Research and Azure AI teams are hiring AI/ML interns to explore foundational LLM fine-tuning, retrieval-augmented generation (RAG), and computer vision pipelines.",
            "requirements": "Solid math foundations in Linear Algebra, Calculus, and Probability\nProficiency in Python and deep learning libraries: PyTorch or TensorFlow\nUnderstanding of Transformer architectures, embeddings, and vector databases\nGood communication skills and ability to experiment quickly",
            "responsibilities": "Train and fine-tune machine learning and language models\nEvaluate model accuracy, benchmark inference latency, and optimize pipelines\nDocument findings and present experiments to senior research scientists",
            "skills": "Python, PyTorch, Transformers, LLMs, NLP, Vector DBs, Mathematics",
            "eligibility": "Pre-final and Final year B.Tech/M.Tech/MS students graduating in 2026/2027",
            "deadline": "Dec 20, 2026",
            "category": "AI & Machine Learning",
            "featured": True
        },
        {
            "title": "Cloud & DevOps Associate",
            "company": "Infosys",
            "company_logo": "https://upload.wikimedia.org/wikipedia/commons/9/95/Infosys_logo.svg",
            "location": "Bengaluru / Pune / Mysuru",
            "job_type": "Full-Time",
            "experience": "0-2 yrs",
            "salary": "₹6,25,000 - ₹9,50,000 PA",
            "description": "Infosys Cobalt team is looking for Cloud & DevOps professionals to automate continuous integration/continuous deployment (CI/CD) pipelines and manage AWS/Azure multi-cloud cloud infrastructure.",
            "requirements": "Working knowledge of Linux OS commands and shell scripting\nFamiliarity with CI/CD tools (Jenkins, GitHub Actions, GitLab CI)\nFoundational knowledge of AWS or Azure and containerization (Docker)\nBasic understanding of Infrastructure as Code (Terraform or Ansible)",
            "responsibilities": "Automate build, test, and release cycles across enterprise projects\nMonitor cloud infrastructure health using Prometheus, Grafana, and CloudWatch\nImplement cloud security best practices and IAM policies",
            "skills": "Linux, Bash, AWS, Docker, Kubernetes, Jenkins, Terraform, CI/CD",
            "eligibility": "B.E / B.Tech / MCA with minimum 65% across academics",
            "deadline": "Dec 10, 2026",
            "category": "Cloud & DevOps",
            "featured": False
        },
        {
            "title": "Data Analyst (SQL & Business Intelligence)",
            "company": "Swiggy",
            "company_logo": "https://upload.wikimedia.org/wikipedia/en/1/12/Swiggy_logo.svg",
            "location": "Bengaluru, Karnataka (On-site)",
            "job_type": "Full-Time",
            "experience": "0-2 yrs",
            "salary": "₹10,00,000 - ₹15,00,000 PA",
            "description": "Drive data-informed decision making across restaurant partner operations, customer delivery experience, and marketing efficiency at India's leading on-demand convenience platform.",
            "requirements": "Advanced SQL skills (window functions, complex joins, CTEs, query optimization)\nProficiency in Tableau, PowerBI, or Metabase for creating operational dashboards\nWorking knowledge of Python/Pandas for data wrangling\nStrong business intuition and analytical aptitude",
            "responsibilities": "Analyze consumer ordering patterns, delivery times, and cancellation rates\nBuild real-time BI dashboards for business unit heads\nDesign and analyze A/B test experiments to validate new app features",
            "skills": "SQL, Tableau, Power BI, Python, Pandas, A/B Testing, Excel",
            "eligibility": "B.E/B.Tech/B.Sc in Statistics/Mathematics/Economics or related discipline",
            "deadline": "Nov 28, 2026",
            "category": "Data Science & Analytics",
            "featured": False
        },
        {
            "title": "Software Development Engineer in Test (SDET)",
            "company": "Flipkart",
            "company_logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Flipkart_logo.svg",
            "location": "Bengaluru, Karnataka",
            "job_type": "Full-Time",
            "experience": "1-3 yrs",
            "salary": "₹15,00,000 - ₹22,00,000 PA",
            "description": "Flipkart's Quality Engineering team is looking for passionate SDETs to build automated test frameworks for massive e-commerce scale, ensuring zero downtime during Big Billion Days.",
            "requirements": "Strong coding ability in Java or Python\nExperience building automated testing frameworks using Selenium, Cypress, or Playwright\nHands-on experience with API automation using RestAssured or Postman\nKnowledge of Performance testing tools (JMeter/Gatling) is a plus",
            "responsibilities": "Develop scalable UI and API test automation suites\nIntegrate test suites into CI/CD pipelines for automated regression testing\nPerform root cause analysis on bug reports and lead quality governance",
            "skills": "Java, Selenium, RestAssured, TestNG, Playwright, CI/CD, JMeter",
            "eligibility": "B.Tech/B.E in Computer Science or equivalent",
            "deadline": "Dec 08, 2026",
            "category": "QA & Testing",
            "featured": False
        }
    ]
    for item in jobs_data:
        db.session.add(Job(**item))

def seed_prep_topics():
    topics_data = [
        {
            "category": "aptitude",
            "sub_category": "quantitative",
            "title": "Time and Work - Formulas, Concepts & Shortcuts",
            "slug": "time-and-work",
            "summary": "Master unit work method, LCM method, efficiency ratios, and pipes & cisterns problems asked in campus placement tests.",
            "read_time": "10 min read",
            "icon": "clock",
            "content": """
<h3>1. Fundamental Principle of Time & Work</h3>
<p>If a person can complete a piece of work in <strong>n days</strong>, then the work done by the person in <strong>1 day</strong> is:</p>
<div class="bg-slate-800 text-emerald-400 p-3 rounded font-mono text-sm my-2">1 Day's Work = 1 / n</div>
<p>Conversely, if a person's 1-day work is <strong>1 / n</strong>, the total time required to finish the entire work is <strong>n days</strong>.</p>

<h3>2. The LCM Method (Fastest Shortcut)</h3>
<p>Instead of working with fractions, assume total work = <strong>LCM of individual times</strong>.</p>
<ul>
    <li><strong>Step 1:</strong> Find the LCM of the days taken by each individual. Let this be the <em>Total Work Units</em>.</li>
    <li><strong>Step 2:</strong> Calculate individual efficiency (Units completed per day) = Total Work / Days taken.</li>
    <li><strong>Step 3:</strong> Sum the efficiencies when working together.</li>
    <li><strong>Step 4:</strong> Total Days = Total Work / Combined Efficiency.</li>
</ul>

<h4>Example:</h4>
<p><em>A can finish a task in 12 days, and B can finish it in 15 days. In how many days can they complete it working together?</em></p>
<div class="bg-slate-900 border border-slate-700 p-3 rounded my-2 text-sm">
    <p>• LCM(12, 15) = <strong>60 units</strong> (Total Work)</p>
    <p>• A's efficiency = 60 / 12 = <strong>5 units/day</strong></p>
    <p>• B's efficiency = 60 / 15 = <strong>4 units/day</strong></p>
    <p>• Combined efficiency (A + B) = 5 + 4 = <strong>9 units/day</strong></p>
    <p>• Total Time = 60 / 9 = <strong>20 / 3 days = 6.67 days</strong></p>
</div>

<h3>3. Important Formulas</h3>
<ul>
    <li><strong>Chain Rule:</strong> <code>(M1 × D1 × H1) / W1 = (M2 × D2 × H2) / W2</code></li>
    <li><strong>Pipes & Cisterns:</strong> Inlet pipe does positive work (+); Outlet / Leak does negative work (-). Net work in 1 hr = (1/A) - (1/B).</li>
</ul>
            """
        },
        {
            "category": "aptitude",
            "sub_category": "quantitative",
            "title": "Speed, Distance & Time - Relative Speed & Trains",
            "slug": "speed-distance-time",
            "summary": "Core concepts of average speed, relative speed in same & opposite directions, and problems on trains and boats.",
            "read_time": "12 min read",
            "icon": "zap",
            "content": """
<h3>1. Golden Rules of Speed & Distance</h3>
<div class="bg-slate-800 text-emerald-400 p-3 rounded font-mono text-sm my-2">
Speed = Distance / Time<br>
Distance = Speed × Time<br>
Time = Distance / Speed
</div>

<h3>2. Unit Conversions</h3>
<ul>
    <li>Convert km/hr to m/s: multiply by <strong>5 / 18</strong></li>
    <li>Convert m/s to km/hr: multiply by <strong>18 / 5</strong></li>
</ul>

<h3>3. Average Speed</h3>
<p><strong>Note:</strong> Average speed is NEVER the simple average of speeds!</p>
<div class="bg-slate-800 text-emerald-400 p-3 rounded font-mono text-sm my-2">
Average Speed = Total Distance Covered / Total Time Taken
</div>
<p>If a person travels equal distances at speeds <em>x</em> and <em>y</em>, then:</p>
<div class="bg-slate-800 text-cyan-400 p-3 rounded font-mono text-sm my-2">
Harmonic Mean = (2xy) / (x + y)
</div>

<h3>4. Relative Speed Concept</h3>
<ul>
    <li><strong>Moving in OPPOSITE directions:</strong> Relative Speed = S1 + S2 (Speeds add up)</li>
    <li><strong>Moving in SAME direction:</strong> Relative Speed = |S1 - S2| (Speeds subtract)</li>
</ul>
            """
        },
        {
            "category": "aptitude",
            "sub_category": "logical",
            "title": "Blood Relations & Family Tree Solving Techniques",
            "slug": "blood-relations",
            "summary": "Step-by-step family tree diagrams, generational notation, and coded relations shortcuts for placement exams.",
            "read_time": "8 min read",
            "icon": "users",
            "content": """
<h3>1. Standard Family Tree Symbols</h3>
<p>To avoid confusion in complex family puzzles, use standard drawing symbols:</p>
<ul>
    <li><strong>[Square]</strong> = Male member</li>
    <li><strong>(Circle)</strong> = Female member</li>
    <li><strong>Horizontal Double Line (=)</strong> = Married couple</li>
    <li><strong>Horizontal Single Line (—)</strong> = Siblings (Brother/Sister)</li>
    <li><strong>Vertical Line (|)</strong> = Generation gap (Parent to Child)</li>
</ul>

<h3>2. Golden Strategy for Pointing-Type Questions</h3>
<p>Start solving from the phrase <strong>"my..."</strong> or <strong>"his/her..."</strong> and work backward towards the speaker.</p>
            """
        },
        {
            "category": "technical",
            "sub_category": "os",
            "title": "Operating Systems: Process vs Thread & CPU Scheduling",
            "slug": "os-process-threads-scheduling",
            "summary": "Process Control Block (PCB), context switching, FCFS, SJF, Round Robin scheduling, and race condition basics.",
            "read_time": "15 min read",
            "icon": "cpu",
            "content": """
<h3>1. Process vs. Thread</h3>
<table class="w-full text-left text-sm border-collapse my-3">
    <thead>
        <tr class="border-b border-slate-700 bg-slate-800 text-slate-200">
            <th class="p-2">Feature</th>
            <th class="p-2">Process</th>
            <th class="p-2">Thread</th>
        </tr>
    </thead>
    <tbody class="divide-y divide-slate-800">
        <tr>
            <td class="p-2 font-semibold">Definition</td>
            <td class="p-2">An executing instance of a program in memory.</td>
            <td class="p-2">Lightweight unit of execution within a process.</td>
        </tr>
        <tr>
            <td class="p-2 font-semibold">Memory Space</td>
            <td class="p-2">Has its own independent address space (Code, Data, Heap, Stack).</td>
            <td class="p-2">Shares code, data, and heap with peer threads; has private stack & registers.</td>
        </tr>
        <tr>
            <td class="p-2 font-semibold">Context Switch</td>
            <td class="p-2">Heavy overhead (flushes TLB, swaps page tables).</td>
            <td class="p-2">Lightweight overhead (fast context switch).</td>
        </tr>
    </tbody>
</table>

<h3>2. Deadlocks & 4 Coffman Conditions</h3>
<ol class="list-decimal pl-5 space-y-1">
    <li><strong>Mutual Exclusion:</strong> Resources cannot be shared simultaneously.</li>
    <li><strong>Hold and Wait:</strong> Process holds a resource while waiting for others.</li>
    <li><strong>No Preemption:</strong> Resources cannot be forcibly seized.</li>
    <li><strong>Circular Wait:</strong> A closed chain of processes each waiting for a resource held by the next.</li>
</ol>
            """
        },
        {
            "category": "technical",
            "sub_category": "dbms",
            "title": "DBMS: ACID Properties, Normalization & Indexing",
            "slug": "dbms-acid-normalization-indexing",
            "summary": "Comprehensive guide to Database Transactions, 1NF to BCNF with examples, B-Tree indexes, and SQL query optimizations.",
            "read_time": "14 min read",
            "icon": "database",
            "content": """
<h3>1. ACID Properties in DBMS</h3>
<ul>
    <li><strong>Atomicity:</strong> All-or-Nothing execution. If any operation fails, the transaction is completely rolled back to the previous stable state.</li>
    <li><strong>Consistency:</strong> The database must remain in a valid state satisfying all integrity constraints (Foreign keys, Unique checks) before and after transaction.</li>
    <li><strong>Isolation:</strong> Concurrent transactions execute independently without interfering with each other's uncommitted data. (Levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable).</li>
    <li><strong>Durability:</strong> Once committed, changes are permanently written to persistent storage (Write-Ahead Logging / WAL) even during a power outage or system crash.</li>
</ul>

<h3>2. Normalization: 1NF to BCNF</h3>
<div class="space-y-3 my-3">
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-indigo-400">1NF (First Normal Form)</h4>
        <p class="text-sm">Eliminate repeating groups. Each column must contain atomic (indivisible) values, and each record must be unique.</p>
    </div>
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-indigo-400">2NF (Second Normal Form)</h4>
        <p class="text-sm">Must be in 1NF + <strong>No Partial Dependency</strong>. Every non-prime attribute must depend on the whole candidate key, not part of a composite key.</p>
    </div>
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-indigo-400">3NF (Third Normal Form)</h4>
        <p class="text-sm">Must be in 2NF + <strong>No Transitive Dependency</strong>. Non-key attributes must NOT depend on other non-key attributes (A → B and B → C is disallowed).</p>
    </div>
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-indigo-400">BCNF (Boyce-Codd Normal Form)</h4>
        <p class="text-sm">A stricter version of 3NF. For every non-trivial functional dependency <code>X → Y</code>, <strong>X must be a super key</strong>.</p>
    </div>
</div>
            """
        },
        {
            "category": "technical",
            "sub_category": "cn",
            "title": "Computer Networks: OSI Layers, TCP Handshake & DNS",
            "slug": "cn-osi-tcp-dns",
            "summary": "Deep dive into 7 OSI Layers, TCP 3-Way Handshake vs UDP, HTTP vs HTTPS, and what happens when you type a URL in the browser.",
            "read_time": "12 min read",
            "icon": "globe",
            "content": """
<h3>1. The 7 Layers of the OSI Model</h3>
<div class="space-y-1 text-sm bg-slate-900 p-3 rounded border border-slate-700 font-mono">
    <p>7. <strong>Application:</strong> HTTP, HTTPS, FTP, SMTP, DNS</p>
    <p>6. <strong>Presentation:</strong> Encryption, SSL/TLS, Data Compression</p>
    <p>5. <strong>Session:</strong> Session establishment, maintenance, token auth</p>
    <p>4. <strong>Transport:</strong> TCP, UDP, Port numbers, End-to-end segmentation</p>
    <p>3. <strong>Network:</strong> IP routing, Routers, Logical addressing (IPv4/IPv6)</p>
    <p>2. <strong>Data Link:</strong> MAC address, Switches, Framing, Error detection (CRC)</p>
    <p>1. <strong>Physical:</strong> Cables, Bits, Signals, Hubs</p>
</div>

<h3>2. TCP 3-Way Handshake</h3>
<ol class="list-decimal pl-5 space-y-1 text-sm">
    <li><strong>Client → Server:</strong> SYN (Synchronize Sequence Number: seq = x)</li>
    <li><strong>Server → Client:</strong> SYN-ACK (Server acknowledges: ack = x + 1, seq = y)</li>
    <li><strong>Client → Server:</strong> ACK (Client acknowledges: ack = y + 1)</li>
</ol>
            """
        },
        {
            "category": "technical",
            "sub_category": "oop",
            "title": "OOP & SOLID Principles with Code Examples",
            "slug": "oop-solid-principles",
            "summary": "The 4 pillars of Object-Oriented Programming and clean architecture SOLID design principles for high-impact interviews.",
            "read_time": "14 min read",
            "icon": "code",
            "content": """
<h3>1. The 4 Pillars of OOP</h3>
<ul>
    <li><strong>Encapsulation:</strong> Bundling data and methods together and hiding internal state.</li>
    <li><strong>Abstraction:</strong> Exposing essential interfaces while concealing implementation mechanics.</li>
    <li><strong>Inheritance:</strong> Reusing code by extending child classes from parents.</li>
    <li><strong>Polymorphism:</strong> Compile-time (Overloading) vs Run-time (Overriding).</li>
</ul>

<h3>2. SOLID Principles</h3>
<ul>
    <li><strong>S:</strong> Single Responsibility</li>
    <li><strong>O:</strong> Open/Closed Principle</li>
    <li><strong>L:</strong> Liskov Substitution Principle</li>
    <li><strong>I:</strong> Interface Segregation Principle</li>
    <li><strong>D:</strong> Dependency Inversion Principle</li>
</ul>
            """
        },
        {
            "category": "hr",
            "sub_category": "hr-common",
            "title": "Mastering 'Tell Me About Yourself' (The Present-Past-Future Model)",
            "slug": "hr-tell-me-about-yourself",
            "summary": "The definitive framework to deliver an impactful 90-second self-introduction tailored for software engineering interviews.",
            "read_time": "7 min read",
            "icon": "user-check",
            "content": """
<h3>The 90-Second Present-Past-Future Formula</h3>
<div class="space-y-3 my-3">
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-emerald-400">1. Present (30 Seconds)</h4>
        <p class="text-sm">State who you are today, current branch/role, and core tech domain.</p>
    </div>
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-cyan-400">2. Past (30 Seconds)</h4>
        <p class="text-sm">Highlight 1-2 major achievements: capstone project or internship outcome.</p>
    </div>
    <div class="p-3 bg-slate-900 border border-slate-700 rounded">
        <h4 class="font-bold text-amber-400">3. Future & Fit (30 Seconds)</h4>
        <p class="text-sm">Connect your passion directly to why you want this specific role and team.</p>
    </div>
</div>
            """
        },
        {
            "category": "hr",
            "sub_category": "hr-behavioral",
            "title": "The STAR Method for Behavioral & Situation Questions",
            "slug": "hr-star-methodology",
            "summary": "How to answer situational questions like 'Tell me about a time you handled a conflict' using Situation, Task, Action, Result.",
            "read_time": "9 min read",
            "icon": "award",
            "content": """
<h3>What is the STAR Framework?</h3>
<ul>
    <li><strong>S - Situation:</strong> Set the context and specify the challenge.</li>
    <li><strong>T - Task:</strong> What was your exact responsibility?</li>
    <li><strong>A - Action:</strong> What steps did YOU execute? Use 'I' instead of 'We'.</li>
    <li><strong>R - Result:</strong> What was the quantifiable outcome?</li>
</ul>
            """
        }
    ]
    for item in topics_data:
        db.session.add(PrepTopic(**item))

def seed_questions():
    questions_data = [
        {
            "category": "aptitude",
            "sub_category": "quantitative",
            "question": "A can complete a project in 10 days, while B can complete it in 15 days. They work together for 4 days, then A leaves. How many days will B take to finish the remaining work?",
            "option_a": "2 days",
            "option_b": "3 days",
            "option_c": "5 days",
            "option_d": "6 days",
            "correct_option": "C",
            "explanation": "Total Work = LCM(10, 15) = 30 units. A's efficiency = 3 units/day, B's efficiency = 2 units/day. Combined efficiency = 5 units/day. In 4 days, together they complete 4 × 5 = 20 units. Remaining work = 30 - 20 = 10 units. Time taken by B alone = 10 / 2 = 5 days.",
            "difficulty": "Medium"
        },
        {
            "category": "aptitude",
            "sub_category": "quantitative",
            "question": "A train 180 meters long is traveling at 72 km/hr. How long will it take to completely pass a platform of length 220 meters?",
            "option_a": "15 seconds",
            "option_b": "18 seconds",
            "option_c": "20 seconds",
            "option_d": "25 seconds",
            "correct_option": "C",
            "explanation": "Speed in m/s = 72 × (5/18) = 20 m/s. Total distance to cross = Length of train + Length of platform = 180 + 220 = 400 meters. Time = Distance / Speed = 400 / 20 = 20 seconds.",
            "difficulty": "Easy"
        },
        {
            "category": "aptitude",
            "sub_category": "logical",
            "question": "Pointing to a photograph of a boy, Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
            "option_a": "Brother",
            "option_b": "Uncle",
            "option_c": "Father",
            "option_d": "Grandfather",
            "correct_option": "C",
            "explanation": "Break it down: 'My mother' = Suresh's mother. 'The only son of my mother' = Suresh himself (since Suresh is male and there is only one son). 'The son of Suresh' = Suresh's son. Therefore, Suresh is the father of the boy.",
            "difficulty": "Easy"
        },
        {
            "category": "technical",
            "sub_category": "os",
            "question": "Which of the following conditions is NOT required for a deadlock to occur in an operating system?",
            "option_a": "Mutual Exclusion",
            "option_b": "Preemption of resources",
            "option_c": "Hold and Wait",
            "option_d": "Circular Wait",
            "correct_option": "B",
            "explanation": "The 4 Coffman conditions for deadlock are: 1. Mutual Exclusion, 2. Hold and Wait, 3. NO preemption, and 4. Circular Wait. 'Preemption of resources' actually breaks deadlocks.",
            "difficulty": "Medium"
        },
        {
            "category": "technical",
            "sub_category": "dbms",
            "question": "In relational databases, which normal form strictly guarantees that there are no partial dependencies on candidate keys?",
            "option_a": "1NF",
            "option_b": "2NF",
            "option_c": "3NF",
            "option_d": "BCNF",
            "correct_option": "B",
            "explanation": "Second Normal Form (2NF) mandates that the table is in 1NF and no non-prime attribute is functionally dependent on any proper subset of any candidate key (eliminates Partial Dependency).",
            "difficulty": "Easy"
        },
        {
            "category": "technical",
            "sub_category": "cn",
            "question": "During the TCP 3-way handshake, what is the exact packet sequence sent between Client (C) and Server (S)?",
            "option_a": "C->S: ACK | S->C: SYN | C->S: FIN",
            "option_b": "C->S: SYN | S->C: SYN-ACK | C->S: ACK",
            "option_c": "C->S: SYN | S->C: ACK | C->S: SYN-ACK",
            "option_d": "C->S: DATA | S->C: ACK | C->S: CLOSE",
            "correct_option": "B",
            "explanation": "TCP establishes a reliable connection in three steps: 1. Client sends SYN, 2. Server responds with SYN-ACK, 3. Client acknowledges with ACK.",
            "difficulty": "Easy"
        },
        {
            "category": "technical",
            "sub_category": "oop",
            "question": "Which SOLID design principle asserts that high-level modules should not depend on low-level modules, but rather both should depend on abstractions?",
            "option_a": "Single Responsibility Principle",
            "option_b": "Open/Closed Principle",
            "option_c": "Liskov Substitution Principle",
            "option_d": "Dependency Inversion Principle",
            "correct_option": "D",
            "explanation": "The Dependency Inversion Principle (DIP) states that high-level modules should depend upon abstraction interfaces rather than concrete low-level implementations.",
            "difficulty": "Medium"
        },
        {
            "category": "hr",
            "sub_category": "hr-common",
            "question": "When an interviewer asks: 'What is your biggest weakness?', what is the most professional strategy to answer?",
            "option_a": "Claim you have no weaknesses and work 16 hours a day.",
            "option_b": "State a genuine non-fatal developmental area and provide the concrete action plan you are actively taking to improve.",
            "option_c": "Tell them you often miss deadlines.",
            "option_d": "Politely decline to answer.",
            "correct_option": "B",
            "explanation": "Interviewers evaluate self-awareness and your ability to seek feedback and self-correct. Admitting a genuine weakness coupled with proactive improvement steps shows maturity and growth mindset.",
            "difficulty": "Easy"
        }
    ]
    for item in questions_data:
        db.session.add(PrepQuestion(**item))

def seed_companies():
    companies_data = [
        {
            "name": "Tata Consultancy Services (TCS)",
            "slug": "tcs",
            "category": "Service Based",
            "logo_color": "bg-blue-600",
            "tagline": "Building on belief - India's premier IT services & consulting giant",
            "ctc_range": "₹3.36 LPA - ₹11.5 LPA",
            "eligibility_summary": "60% or 6.0 CGPA throughout 10th, 12th, and Degree. Max 1 active backlog.",
            "difficulty_level": "Medium",
            "packages_json": json.dumps([
                {"role": "TCS Ninja", "ctc": "₹3.36 - ₹3.6 LPA", "desc": "Entry-level development and system maintenance role."},
                {"role": "TCS Digital", "ctc": "₹7.0 - ₹7.5 LPA", "desc": "High-velocity role focusing on Cloud, Full Stack, and AI/ML."},
                {"role": "TCS Prime", "ctc": "₹9.0 - ₹11.5 LPA", "desc": "Elite cadre tackling advanced software architecture, system R&D, and algorithms."}
            ]),
            "eligibility_json": json.dumps({
                "cgpa_percentage": "Minimum 60% or 6.0 CGPA throughout 10th, 12th, Diploma, and Undergrad/Postgrad",
                "backlogs": "Maximum 1 active backlog permitted at the time of appearing (must be cleared before joining)",
                "academic_gap": "Overall gap in academics should not exceed 24 months",
                "eligible_degrees": "B.E. / B.Tech / M.E. / M.Tech / MCA / M.Sc (CS/IT)"
            }),
            "exam_pattern_json": json.dumps([
                {
                    "section": "Part A: Foundation Section",
                    "duration": "75 mins",
                    "subsections": "Numerical Ability (20 Qs), Verbal Ability (25 Qs), Reasoning Ability (20 Qs)",
                    "marking": "No negative marking"
                },
                {
                    "section": "Part B: Advanced Section (For Digital / Prime)",
                    "duration": "90 mins",
                    "subsections": "Advanced Quantitative (15 Qs), Advanced Reasoning (10 Qs), Advanced Hands-on Coding (2 Questions)",
                    "marking": "Strict evaluation on test cases"
                }
            ]),
            "syllabus_json": json.dumps({
                "Aptitude": "Number systems, percentages, ratios, time & work, permutations, probability, blood relations, syllogisms, seating arrangements.",
                "Technical / Coding": "Arrays, Strings, HashMaps, Recursion, Dynamic Programming basics, Sorting, Searching.",
                "CS Fundamentals": "OOP concepts, SQL queries & normalization, OS memory management, Computer networks basics."
            }),
            "rounds_json": json.dumps([
                {"round_num": "Round 1", "name": "National Qualifier Test (TCS NQT)", "type": "Online Assessment (Foundation + Advanced)"},
                {"round_num": "Round 2", "name": "Technical Interview", "type": "Live Coding, DSA, Resume Projects, DBMS, OOP"},
                {"round_num": "Round 3", "name": "Managerial & HR Interview", "type": "Behavioral scenarios, relocation, communication & cultural fit"}
            ]),
            "interview_tips": json.dumps([
                "Practice both coding questions in the NQT; solving at least 1 fully and 1 partially is often needed for Digital, while solving both with optimal complexity opens TCS Prime.",
                "Be ready to explain every single project listed on your resume in depth, including architecture diagrams and SQL schema.",
                "Revise OOP pillars with code syntax in your preferred language (Java/C++/Python)."
            ]),
            "sample_questions": json.dumps([
                "Write a program to find the equilibrium index of an array.",
                "Explain the difference between primary key, unique key, and candidate key.",
                "How does garbage collection work in Java?",
                "What is virtual memory and why is it needed?"
            ])
        },
        {
            "name": "Amazon",
            "slug": "amazon",
            "category": "Tech Giant",
            "logo_color": "bg-amber-600",
            "tagline": "Earth's most customer-centric company - Software Development Engineer I",
            "ctc_range": "₹30.0 LPA - ₹45.0 LPA",
            "eligibility_summary": "B.Tech/M.Tech in CS/IT/ECE or related; 7.0+ CGPA preferred; exceptional DSA mastery.",
            "difficulty_level": "Hard",
            "packages_json": json.dumps([
                {"role": "SDE Intern", "ctc": "₹1,10,000 / month Stipend", "desc": "6-month internship with high Pre-Placement Offer (PPO) conversion."},
                {"role": "SDE I (Full Time)", "ctc": "₹32.0 - ₹44.0 LPA (Base ~₹16-18L + Stocks + Sign-on)", "desc": "Full-time software engineering role in Amazon AWS, Retail, or Logistics."}
            ]),
            "eligibility_json": json.dumps({
                "cgpa_percentage": "Generally 6.5+ CGPA or equivalent with no active backlogs",
                "degrees": "B.Tech/B.E, M.Tech, Dual Degree in Computer Science, IT, Mathematics, or Electronics",
                "experience": "0 to 2 years for SDE-1"
            }),
            "exam_pattern_json": json.dumps([
                {
                    "section": "Online Assessment (OA 1 - Code Debugging)",
                    "duration": "20 mins",
                    "subsections": "7 debugging questions in C/C++/Java",
                    "marking": "Fix bugs within time limit"
                },
                {
                    "section": "Online Assessment (OA 2 - Coding & Work Style)",
                    "duration": "90 mins",
                    "subsections": "2 Medium-Hard LeetCode style problems + 15 mins Work Style Assessment based on Amazon Leadership Principles",
                    "marking": "All test cases + behavioral consistency"
                },
                {
                    "section": "Online Assessment (OA 3 - Work Simulation)",
                    "duration": "120 mins",
                    "subsections": "Simulated day-in-the-life scenarios, video messages, prioritizing tasks, and critical problem solving",
                    "marking": "Leadership Principles alignment"
                }
            ]),
            "syllabus_json": json.dumps({
                "DSA": "Trees, Binary Search Trees, Graphs (BFS/DFS, Dijkstra), Dynamic Programming, Heaps, Sliding Window, Tries.",
                "Design": "Low-Level Design (LLD), Object-Oriented Design patterns (Factory, Singleton, Observer), Concurrency basics.",
                "Leadership Principles": "Customer Obsession, Ownership, Bias for Action, Earn Trust, Dive Deep, Deliver Results."
            }),
            "rounds_json": json.dumps([
                {"round_num": "Round 1", "name": "Online Assessment (OA)", "type": "Coding, Debugging & Work Simulation"},
                {"round_num": "Round 2", "name": "Technical Round 1", "type": "DSA Problem Solving + 1 Leadership Principle Question"},
                {"round_num": "Round 3", "name": "Technical Round 2", "type": "Data Structures & Algorithms + 1 Leadership Principle Question"},
                {"round_num": "Round 4", "name": "Technical Round 3 / LLD", "type": "Object Oriented Design / System Logic + LP"},
                {"round_num": "Round 5", "name": "Bar Raiser Round", "type": "Senior Engineering Manager testing cultural fit, deep technical push, and LP scenarios"}
            ]),
            "interview_tips": json.dumps([
                "Crucial: Every single round at Amazon allocates 15-20 minutes to Amazon Leadership Principles! Prepare 2 STAR-method stories per principle.",
                "Always communicate your thought process aloud before writing code. Analyze time and space complexity upfront.",
                "Test your solution with edge cases (empty inputs, negative values, duplicates, large bounds) without being prompted."
            ]),
            "sample_questions": json.dumps([
                "Given a binary tree, find the maximum path sum between any two nodes.",
                "Design an LRU Cache with O(1) get and put operations.",
                "Word Ladder problem (shortest transformation sequence using BFS).",
                "Tell me about a time when you took a calculated risk and failed. What did you learn?"
            ])
        },
        {
            "name": "Infosys",
            "slug": "infosys",
            "category": "Service Based",
            "logo_color": "bg-indigo-600",
            "tagline": "Navigate your next - Specialist Programmer & Digital Specialist",
            "ctc_range": "₹3.6 LPA - ₹9.5 LPA",
            "eligibility_summary": "60% or 65% in 10th, 12th, and B.Tech. Max 1 active backlog allowed.",
            "difficulty_level": "Medium",
            "packages_json": json.dumps([
                {"role": "System Engineer (SE)", "ctc": "₹3.6 LPA", "desc": "Standard campus recruitment profile."},
                {"role": "Digital Specialist Engineer (DSE)", "ctc": "₹6.25 LPA", "desc": "Advanced coding profile for full-stack and cloud delivery."},
                {"role": "Specialist Programmer (SP)", "ctc": "₹9.5 LPA", "desc": "High-tier algorithmic coding specialist profile via HackWithInfy / InfyTQ."}
            ]),
            "eligibility_json": json.dumps({
                "cgpa_percentage": "60% or 65% throughout 10th, 12th, and Undergrad",
                "backlogs": "0 or 1 active backlog permitted depending on campus drive terms",
                "education": "B.E./B.Tech/M.E./M.Tech/MCA/M.Sc in eligible streams"
            }),
            "exam_pattern_json": json.dumps([
                {
                    "section": "System Engineer Assessment",
                    "duration": "100 mins",
                    "subsections": "Mathematical Ability (10 Qs), Reasoning Ability (15 Qs), Verbal Ability (20 Qs), Pseudocode (5 Qs), Puzzle Solving (4 Qs)",
                    "marking": "No negative marking"
                },
                {
                    "section": "SP / DSE Coding Round",
                    "duration": "180 mins",
                    "subsections": "3 algorithmic coding questions (1 Medium, 1 Medium-Hard, 1 Hard)",
                    "marking": "Strict evaluation across all test cases"
                }
            ]),
            "syllabus_json": json.dumps({
                "Aptitude": "Permutations, probability, speed distance time, data sufficiency, syllogisms, reading comprehension.",
                "Pseudocode": "Loop tracing, bitwise operations, recursion outputs, pointer syntax in C.",
                "Algorithmic Coding": "Greedy algorithms, dynamic programming, tree traversals, graph algorithms."
            }),
            "rounds_json": json.dumps([
                {"round_num": "Round 1", "name": "Online Test / HackWithInfy", "type": "Aptitude + Pseudocode or Algorithmic Coding"},
                {"round_num": "Round 2", "name": "Technical Interview", "type": "Core CS subjects, project review, DSA coding"},
                {"round_num": "Round 3", "name": "HR Interview", "type": "Communication, willingness to relocate, bond/policy acknowledgement"}
            ]),
            "interview_tips": json.dumps([
                "For SP and DSE roles, solve past HackWithInfy problems focusing on dynamic programming and graph traversals.",
                "For SE, pay strong attention to Pseudocode questions; they test edge condition logic in loops and bitwise logic."
            ]),
            "sample_questions": json.dumps([
                "Write a query to find the Nth highest salary from an Employee table.",
                "Explain the difference between compile-time polymorphism and runtime polymorphism.",
                "Reverse a linked list in groups of given size K."
            ])
        },
        {
            "name": "Microsoft",
            "slug": "microsoft",
            "category": "Tech Giant",
            "logo_color": "bg-sky-600",
            "tagline": "Empowering every person and organization on the planet to achieve more",
            "ctc_range": "₹24.0 LPA - ₹42.0 LPA",
            "eligibility_summary": "7.0+ CGPA; B.Tech/M.Tech in CS/IT/ECE; strong problem-solving in DSA.",
            "difficulty_level": "Hard",
            "packages_json": json.dumps([
                {"role": "Software Engineering Intern", "ctc": "₹1,25,000 / month Stipend", "desc": "Summer internship with high Pre-Placement Offer rates."},
                {"role": "Software Engineer (SDE 1)", "ctc": "₹28.0 - ₹42.0 LPA (Base ~₹16-18L + RSUs + Bonus)", "desc": "Core engineering in Azure, Teams, Office 365, or Windows."}
            ]),
            "eligibility_json": json.dumps({
                "cgpa_percentage": "7.0+ CGPA with no active backlogs",
                "degrees": "B.Tech/B.E, M.Tech, Dual Degree, MS in CS/IT/ECE"
            }),
            "exam_pattern_json": json.dumps([
                {
                    "section": "Codility Online Assessment",
                    "duration": "90 mins",
                    "subsections": "2 to 3 coding problems (String manipulation, Graph / Tree traversal, Matrix DP)",
                    "marking": "Correctness + Performance (Time & Space complexity score)"
                }
            ]),
            "syllabus_json": json.dumps({
                "DSA": "Binary Trees, BST, Linked Lists, Graphs, Dynamic Programming, Backtracking.",
                "System & CS Fundamentals": "Memory management, multi-threading, concurrency, low-level design."
            }),
            "rounds_json": json.dumps([
                {"round_num": "Round 1", "name": "Online Assessment (Codility)", "type": "2-3 algorithmic problems"},
                {"round_num": "Round 2", "name": "Technical Round 1", "type": "Data structures & problem solving on virtual whiteboard"},
                {"round_num": "Round 3", "name": "Technical Round 2", "type": "Complex algorithms, system design primitives, edge-case testing"},
                {"round_num": "Round 4", "name": "Director / AA Round", "type": "As Appropriate (AA) round evaluating culture, growth mindset & technical depth"}
            ]),
            "interview_tips": json.dumps([
                "Microsoft interviewers place heavy emphasis on code cleanliness, meaningful variable names, and structured modular design.",
                "Demonstrate a 'Growth Mindset': if you receive a hint, acknowledge it enthusiastically and incorporate it directly into your solution."
            ]),
            "sample_questions": json.dumps([
                "Serialize and Deserialize a Binary Tree.",
                "Find the minimum number of platforms required for a railway station given train arrival and departure times.",
                "Clone a graph with undirected nodes."
            ])
        },
        {
            "name": "Accenture",
            "slug": "accenture",
            "category": "Service Based",
            "logo_color": "bg-purple-600",
            "tagline": "Let there be change - Global professional services & enterprise digital solutions",
            "ctc_range": "₹4.5 LPA - ₹6.5 LPA",
            "eligibility_summary": "65% or 6.5 CGPA in B.Tech/MCA/M.Tech. No active backlogs.",
            "difficulty_level": "Medium",
            "packages_json": json.dumps([
                {"role": "Associate Software Engineer (ASE)", "ctc": "₹4.5 LPA", "desc": "Full-time software engineering and cloud implementation."},
                {"role": "Advanced Associate Software Engineer (AASE)", "ctc": "₹6.5 LPA", "desc": "High-complexity software engineering, microservices, and AI integrations."}
            ]),
            "eligibility_json": json.dumps({
                "cgpa_percentage": "65% or 6.5 CGPA aggregate throughout graduation",
                "backlogs": "Zero active backlogs at the time of appearing"
            }),
            "exam_pattern_json": json.dumps([
                {
                    "section": "Stage 1: Cognitive & Technical Assessment",
                    "duration": "90 mins",
                    "subsections": "English Ability (17 Qs), Critical Thinking & Problem Solving (18 Qs), Abstract Reasoning (15 Qs), Common Apps & MS Office (12 Qs), Pseudocode (18 Qs), Networking, Security & Cloud (10 Qs)",
                    "marking": "Elimination round. Total 90 questions."
                },
                {
                    "section": "Stage 2: Technical Coding Assessment",
                    "duration": "45 mins",
                    "subsections": "2 Coding Questions (Strings, Arrays, Basic Math)",
                    "marking": "Mandatory clearance for AASE consideration"
                }
            ]),
            "syllabus_json": json.dumps({
                "Cognitive": "English grammar, logical deductives, arrangements, series completion.",
                "Technical": "Pseudocode execution, cloud computing basics (IaaS/PaaS/SaaS), security encryption fundamentals."
            }),
            "rounds_json": json.dumps([
                {"round_num": "Stage 1", "name": "Cognitive & Technical Assessment", "type": "Online MCQ (90 Qs)"},
                {"round_num": "Stage 2", "name": "Coding Assessment", "type": "2 Hands-on Coding questions"},
                {"round_num": "Stage 3", "name": "Communication Assessment", "type": "Automated voice & spoken English test"},
                {"round_num": "Stage 4", "name": "Virtual Interview", "type": "Combined Technical and HR interview"}
            ]),
            "interview_tips": json.dumps([
                "Stage 1 has sectional cutoffs; practice Pseudocode questions carefully as they carry significant weight.",
                "For the Communication test, use a high quality headset in a completely quiet room."
            ]),
            "sample_questions": json.dumps([
                "Count the number of set bits in an integer.",
                "What is the difference between SaaS, PaaS, and IaaS with real-world examples?"
            ])
        }
    ]
    for item in companies_data:
        db.session.add(Company(**item))

def seed_dsa_problems():
    existing_titles = {p.title for p in DSAProblem.query.all()}
    
    problems = [
        # 1. Arrays
        {
            "topic": "Arrays",
            "title": "Two Sum",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/two-sum/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/key-pair5616/1",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "approach": "Use a Hash Map to store previously visited elements and their indices. For each element num, check if (target - num) exists in the map. Time: O(N), Space: O(N).",
            "time_complexity": "O(N)",
            "space_complexity": "O(N)",
            "code_python": """def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []""",
            "code_cpp": """vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int diff = target - nums[i];
        if (seen.count(diff)) return {seen[diff], i};
        seen[nums[i]] = i;
    }
    return {};
}""",
            "code_java": """public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int diff = target - nums[i];
        if (map.containsKey(diff)) return new int[]{map.get(diff), i};
        map.put(nums[i], i);
    }
    return new int[]{};
}""",
            "order_index": 1
        },
        {
            "topic": "Arrays",
            "title": "Maximum Subarray (Kadane's Algorithm)",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/maximum-subarray/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/kadanes-algorithm-1587115620/1",
            "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
            "approach": "Kadane's Algorithm: Maintain current_sum and max_sum. Iterate through the array; add current element to current_sum. If current_sum becomes negative, reset it to 0. Update max_sum at each step.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def maxSubArray(nums):
    max_sum = float('-inf')
    curr_sum = 0
    for num in nums:
        curr_sum += num
        max_sum = max(max_sum, curr_sum)
        if curr_sum < 0:
            curr_sum = 0
    return max_sum""",
            "code_cpp": """int maxSubArray(vector<int>& nums) {
    int maxSum = INT_MIN, currSum = 0;
    for (int num : nums) {
        currSum += num;
        maxSum = max(maxSum, currSum);
        if (currSum < 0) currSum = 0;
    }
    return maxSum;
}""",
            "code_java": """public int maxSubArray(int[] nums) {
    int maxSum = Integer.MIN_VALUE, currSum = 0;
    for (int num : nums) {
        currSum += num;
        maxSum = Math.max(maxSum, currSum);
        if (currSum < 0) currSum = 0;
    }
    return maxSum;
}""",
            "order_index": 2
        },
        {
            "topic": "Arrays",
            "title": "Sort Colors (0s, 1s, and 2s - Dutch National Flag)",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/sort-colors/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/sort-an-array-of-0s-1s-and-2s4231/1",
            "description": "Given an array nums with n objects colored red, white, or blue (represented by 0, 1, 2), sort them in-place so that objects of the same color are adjacent.",
            "approach": "Dutch National Flag Algorithm using 3 pointers: low = 0, mid = 0, high = n - 1. If nums[mid] == 0: swap(nums[low], nums[mid]), low++, mid++. If nums[mid] == 1: mid++. If nums[mid] == 2: swap(nums[mid], nums[high]), high--.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1""",
            "code_cpp": """void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) swap(nums[low++], nums[mid++]);
        else if (nums[mid] == 1) mid++;
        else swap(nums[mid], nums[high--]);
    }
}""",
            "code_java": """public void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            int t = nums[low]; nums[low++] = nums[mid]; nums[mid++] = t;
        } else if (nums[mid] == 1) mid++;
        else {
            int t = nums[mid]; nums[mid] = nums[high]; nums[high--] = t;
        }
    }
}""",
            "order_index": 3
        },
        {
            "topic": "Arrays",
            "title": "Merge Intervals",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/merge-intervals/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/overlapping-intervals--170633/1",
            "description": "Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals.",
            "approach": "Sort intervals based on start time. If current interval overlaps with previous merged interval, extend previous end time. Otherwise append current.",
            "time_complexity": "O(N log N)",
            "space_complexity": "O(N)",
            "code_python": """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for iv in intervals:
        if not merged or merged[-1][1] < iv[0]:
            merged.append(iv)
        else:
            merged[-1][1] = max(merged[-1][1], iv[1])
    return merged""",
            "code_cpp": """vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> res;
    for (auto& iv : intervals) {
        if (res.empty() || res.back()[1] < iv[0]) res.push_back(iv);
        else res.back()[1] = max(res.back()[1], iv[1]);
    }
    return res;
}""",
            "code_java": """public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> res = new ArrayList<>();
    for (int[] iv : intervals) {
        if (res.isEmpty() || res.get(res.size() - 1)[1] < iv[0]) res.add(iv);
        else res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], iv[1]);
    }
    return res.toArray(new int[res.size()][]);
}""",
            "order_index": 4
        },
        # 2. Two Pointers & Sliding Window
        {
            "topic": "Two Pointers & Sliding Window",
            "title": "3Sum",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/3sum/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/triplet-sum-in-array-1587115621/1",
            "description": "Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]] such that i != j != k and nums[i] + nums[j] + nums[k] == 0.",
            "approach": "Sort array. Loop through elements and use two pointers (left and right) to find matching pairs that sum to -nums[i]. Skip duplicate elements.",
            "time_complexity": "O(N^2)",
            "space_complexity": "O(1) auxiliary",
            "code_python": """def threeSum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif s < 0: l += 1
            else: r -= 1
    return res""",
            "code_cpp": """vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> res;
    for (int i = 0; i < (int)nums.size() - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = nums.size() - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s == 0) {
                res.push_back({nums[i], nums[l], nums[r]});
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (s < 0) l++;
            else r--;
        }
    }
    return res;
}""",
            "code_java": """public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s == 0) {
                res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (s < 0) l++;
            else r--;
        }
    }
    return res;
}""",
            "order_index": 5
        },
        {
            "topic": "Two Pointers & Sliding Window",
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/length-of-the-longest-substring3036/1",
            "description": "Given a string s, find the length of the longest substring without repeating characters.",
            "approach": "Sliding window with two pointers left and right, maintaining the last seen index of each character in a hash map.",
            "time_complexity": "O(N)",
            "space_complexity": "O(min(N, M))",
            "code_python": """def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = 0; max_len = 0
    for right, ch in enumerate(s):
        if ch in char_map and char_map[ch] >= left:
            left = char_map[ch] + 1
        char_map[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
            "code_cpp": """int lengthOfLongestSubstring(string s) {
    vector<int> charIndex(128, -1);
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        if (charIndex[s[right]] >= left) left = charIndex[s[right]] + 1;
        charIndex[s[right]] = right;
        maxLen = max(maxLen, right - left + 1);
    }
    return maxLen;
}""",
            "code_java": """public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> map = new HashMap<>();
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (map.containsKey(c) && map.get(c) >= left) left = map.get(c) + 1;
        map.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}""",
            "order_index": 6
        },
        # 3. Strings
        {
            "topic": "Strings",
            "title": "Valid Anagram",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/valid-anagram/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/anagram-1587115620/1",
            "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.",
            "approach": "Count character frequencies using an array of size 26 or a hash map. Increment for string s and decrement for string t. If all counts are zero, they are anagrams.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t): return False
    count = [0] * 26
    for c1, c2 in zip(s, t):
        count[ord(c1) - ord('a')] += 1
        count[ord(c2) - ord('a')] -= 1
    return all(x == 0 for x in count)""",
            "code_cpp": """bool isAnagram(string s, string t) {
    if (s.length() != t.length()) return false;
    vector<int> count(26, 0);
    for (int i = 0; i < s.length(); i++) {
        count[s[i] - 'a']++;
        count[t[i] - 'a']--;
    }
    for (int c : count) if (c != 0) return false;
    return true;
}""",
            "code_java": """public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i) - 'a']++;
        count[t.charAt(i) - 'a']--;
    }
    for (int c : count) if (c != 0) return false;
    return true;
}""",
            "order_index": 7
        },
        {
            "topic": "Strings",
            "title": "Group Anagrams",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/group-anagrams/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/print-anagrams-together/1",
            "description": "Given an array of strings strs, group the anagrams together in any order.",
            "approach": "Use a Hash Map where the key is the sorted character array and value is the list of matching anagrams.",
            "time_complexity": "O(N × K log K)",
            "space_complexity": "O(N × K)",
            "code_python": """from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[''.join(sorted(s))].append(s)
    return list(groups.values())""",
            "code_cpp": """vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) {
        string key = s; sort(key.begin(), key.end());
        groups[key].push_back(s);
    }
    vector<vector<string>> res;
    for (auto& p : groups) res.push_back(p.second);
    return res;
}""",
            "code_java": """public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] ca = s.toCharArray(); Arrays.sort(ca);
        String key = String.valueOf(ca);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}""",
            "order_index": 8
        },
        # 4. Linked Lists
        {
            "topic": "Linked Lists",
            "title": "Reverse Linked List",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/reverse-linked-list/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/reverse-a-linked-list/1",
            "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
            "approach": "Iterative 3-pointer technique: maintain prev = null, curr = head. Save next = curr.next, point curr.next = prev, advance prev = curr, curr = next.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev""",
            "code_cpp": """ListNode* reverseList(ListNode* head) {
    ListNode *prev = nullptr, *curr = head;
    while (curr) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}""",
            "code_java": """public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode nxt = curr.next;
        curr.next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}""",
            "order_index": 9
        },
        {
            "topic": "Linked Lists",
            "title": "Linked List Cycle (Floyd's Tortoise and Hare)",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/linked-list-cycle/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/detect-loop-in-linked-list/1",
            "description": "Given head, the head of a linked list, determine if the linked list has a cycle in it.",
            "approach": "Slow pointer moves 1 step, fast pointer moves 2 steps. If they meet, a cycle exists. If fast reaches null, no cycle exists.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False""",
            "code_cpp": """bool hasCycle(ListNode *head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next; fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}""",
            "code_java": """public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next; fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}""",
            "order_index": 10
        },
        # 5. Stacks & Queues
        {
            "topic": "Stacks & Queues",
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/parenthesis-checker2744/1",
            "description": "Given a string s containing '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "approach": "Push opening brackets onto stack. For closing brackets, check if stack is non-empty and top matches the closing bracket type.",
            "time_complexity": "O(N)",
            "space_complexity": "O(N)",
            "code_python": """def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return len(stack) == 0""",
            "code_cpp": """bool isValid(string s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') st.push(c);
        else {
            if (st.empty()) return false;
            char top = st.top(); st.pop();
            if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) return false;
        }
    }
    return st.empty();
}""",
            "code_java": """public boolean isValid(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '{' || c == '[') stack.push(c);
        else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) return false;
        }
    }
    return stack.isEmpty();
}""",
            "order_index": 11
        },
        # 6. Binary Search
        {
            "topic": "Binary Search",
            "title": "Search in Rotated Sorted Array",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/search-in-a-rotated-array4618/1",
            "description": "Given sorted and rotated array nums and an integer target, return index of target, or -1 if not found. Must run in O(log n).",
            "approach": "In any rotated sorted array, at least one half (left or right) is strictly sorted. Check if target lies within the sorted half; adjust low/high accordingly.",
            "time_complexity": "O(log N)",
            "space_complexity": "O(1)",
            "code_python": """def search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target: return mid
        if nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]: high = mid - 1
            else: low = mid + 1
        else:
            if nums[mid] < target <= nums[high]: low = mid + 1
            else: high = mid - 1
    return -1""",
            "code_cpp": """int search(vector<int>& nums, int target) {
    int low = 0, high = nums.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return mid;
        if (nums[low] <= nums[mid]) {
            if (nums[low] <= target && target < nums[mid]) high = mid - 1;
            else low = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[high]) low = mid + 1;
            else high = mid - 1;
        }
    }
    return -1;
}""",
            "code_java": """public int search(int[] nums, int target) {
    int low = 0, high = nums.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return mid;
        if (nums[low] <= nums[mid]) {
            if (nums[low] <= target && target < nums[mid]) high = mid - 1;
            else low = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[high]) low = mid + 1;
            else high = mid - 1;
        }
    }
    return -1;
}""",
            "order_index": 12
        },
        # 7. Trees & BST
        {
            "topic": "Trees & Binary Search Trees",
            "title": "Lowest Common Ancestor of a Binary Tree",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/lowest-common-ancestor-in-a-binary-tree/1",
            "description": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.",
            "approach": "Post-order recursive traversal: If current node is null or matches p or q, return node. If both left and right calls return non-null, current node is the LCA.",
            "time_complexity": "O(N)",
            "space_complexity": "O(H)",
            "code_python": """def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q: return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right: return root
    return left if left else right""",
            "code_cpp": """TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}""",
            "code_java": """public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;
    return left != null ? left : right;
}""",
            "order_index": 13
        },
        # 8. Graphs
        {
            "topic": "Graphs",
            "title": "Number of Islands",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/number-of-islands/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/find-the-number-of-islands/1",
            "description": "Given an m x n 2D binary grid grid where '1' represents land and '0' represents water, return the number of islands.",
            "approach": "Traverse each cell. When an unvisited '1' is found, increment island count and initiate BFS or DFS to sink all connected land ('1' -> '0').",
            "time_complexity": "O(M × N)",
            "space_complexity": "O(M × N)",
            "code_python": """def numIslands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1': return
        grid[r][c] = '0'
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count""",
            "code_cpp": """int numIslands(vector<vector<char>>& grid) {
    int count = 0, m = grid.size(), n = grid[0].size();
    function<void(int, int)> dfs = [&](int r, int c) {
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') return;
        grid[r][c] = '0';
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1);
    };
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] == '1') { count++; dfs(i, j); }
    return count;
}""",
            "code_java": """public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') { count++; dfs(grid, i, j); }
        }
    }
    return count;
}
private void dfs(char[][] g, int r, int c) {
    if (r < 0 || r >= g.length || c < 0 || c >= g[0].length || g[r][c] != '1') return;
    g[r][c] = '0';
    dfs(g, r+1, c); dfs(g, r-1, c); dfs(g, r, c+1); dfs(g, r, c-1);
}""",
            "order_index": 14
        },
        # 9. Dynamic Programming
        {
            "topic": "Dynamic Programming",
            "title": "Coin Change",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/coin-change/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/coin-change2448/1",
            "description": "Given coins array and amount, return the fewest number of coins needed to make up that amount.",
            "approach": "Bottom-up 1D DP: dp[i] = min(dp[i], dp[i - coin] + 1) for all valid coin denominations.",
            "time_complexity": "O(Amount × N)",
            "space_complexity": "O(Amount)",
            "code_python": """def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
            "code_cpp": """int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) dp[i] = min(dp[i], dp[i - coin] + 1);
    }
    return dp[amount] > amount ? -1 : dp[amount];
}""",
            "code_java": """public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) dp[i] = Math.min(dp[i], dp[i - coin] + 1);
    }
    return dp[amount] > amount ? -1 : dp[amount];
}""",
            "order_index": 15
        },
        # 10. Greedy & Bit Manipulation
        {
            "topic": "Greedy & Bit Manipulation",
            "title": "Single Number",
            "difficulty": "Easy",
            "leetcode_url": "https://leetcode.com/problems/single-number/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/find-the-element-that-appears-once-in-sorted-array0624/1",
            "description": "Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.",
            "approach": "Use Bitwise XOR (^). Duplicate numbers XOR to 0, leaving only the unique element.",
            "time_complexity": "O(N)",
            "space_complexity": "O(1)",
            "code_python": """def singleNumber(nums):
    res = 0
    for num in nums: res ^= num
    return res""",
            "code_cpp": """int singleNumber(vector<int>& nums) {
    int res = 0;
    for (int n : nums) res ^= n;
    return res;
}""",
            "code_java": """public int singleNumber(int[] nums) {
    int res = 0;
    for (int n : nums) res ^= n;
    return res;
}""",
            "order_index": 16
        },
        # 11. Recursion & Backtracking
        {
            "topic": "Recursion & Backtracking",
            "title": "Subsets (Power Set)",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/subsets/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/subsets-1613027340/1",
            "description": "Given an integer array nums of unique elements, return all possible subsets (the power set).",
            "approach": "Backtracking: At each index, either include nums[index] in current subset and recurse, then backtrack (pop), or skip nums[index] and recurse.",
            "time_complexity": "O(2^N)",
            "space_complexity": "O(N)",
            "code_python": """def subsets(nums):
    res = []
    def backtrack(start, path):
        res.append(list(path))
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return res""",
            "code_cpp": """vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> res; vector<int> path;
    function<void(int)> backtrack = [&](int start) {
        res.push_back(path);
        for (int i = start; i < nums.size(); i++) {
            path.push_back(nums[i]); backtrack(i + 1); path.pop_back();
        }
    };
    backtrack(0); return res;
}""",
            "code_java": """public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    backtrack(0, nums, new ArrayList<>(), res);
    return res;
}
private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {
    res.add(new ArrayList<>(path));
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]); backtrack(i + 1, nums, path, res); path.remove(path.size() - 1);
    }
}""",
            "order_index": 17
        },
        # 12. Heaps & Priority Queues
        {
            "topic": "Heaps & Priority Queues",
            "title": "Kth Largest Element in an Array",
            "difficulty": "Medium",
            "leetcode_url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
            "gfg_url": "https://practice.geeksforgeeks.org/problems/k-largest-elements3736/1",
            "description": "Given an integer array nums and an integer k, return the kth largest element in the array.",
            "approach": "Use a Min-Heap of size K. When heap size exceeds K, pop the smallest element. Top of min-heap will be the kth largest.",
            "time_complexity": "O(N log K)",
            "space_complexity": "O(K)",
            "code_python": """import heapq
def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k: heapq.heappop(heap)
    return heap[0]""",
            "code_cpp": """int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int num : nums) {
        minHeap.push(num);
        if (minHeap.size() > k) minHeap.pop();
    }
    return minHeap.top();
}""",
            "code_java": """public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.add(num);
        if (minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek();
}""",
            "order_index": 18
        }
    ]

    for p in problems:
        if p["title"] not in existing_titles:
            db.session.add(DSAProblem(**p))
