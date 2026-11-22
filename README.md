
<div align="center">

# 🛡️ NEXUS
### Cybersecurity Training & Simulation Portal

**Learn. Investigate. Defend.**

A hands-on cybersecurity training environment designed to help learners develop practical skills in phishing awareness, security analysis, incident response, and Security Operations Center (SOC) investigations.

<br>

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?logo=linux&logoColor=white)
![Status](https://img.shields.io/badge/Status-Under%20Development-orange)

</div>

---

## 📌 Overview

NEXUS is a web-based cybersecurity training portal built with Python and Flask. It provides a simulated environment where users can explore cybersecurity concepts, complete security assessments, and practice investigation techniques through structured training scenarios.

The platform focuses on defensive security, cybersecurity awareness, and foundational Security Operations Center (SOC) skills.

This project is being developed as a hands-on learning and portfolio project.

---

## 🎯 Project Objectives

- Develop practical cybersecurity investigation skills.
- Improve phishing detection and security awareness.
- Introduce Linux log analysis and network investigation.
- Understand incident response procedures.
- Learn the fundamentals of SOC operations and SIEM.
- Provide an interactive environment for cybersecurity assessments.
- Explore authentication and user management in Flask applications.

---

## ✨ Features

### 🔐 User Authentication
- User registration and sign-in.
- Password hashing.
- Session-based authentication.
- Simulated login attempt restrictions.
- Sign-out functionality.

### 🎣 Phishing Awareness Assessment
- Interactive phishing assessment.
- Multiple-choice security questions.
- Automated scoring.
- Feedback and explanations.
- Results summary.

### 🔎 Practical Training Modules

| Module | Description |
|---|---|
| Phishing Assessment | Identify phishing indicators and suspicious messages. |
| Suspicious URL Analysis | Investigate domains, URLs, and social engineering indicators. |
| Linux Log Investigation | Analyze authentication events and suspicious login activity. |
| Network Traffic Analysis | Understand network connections, DNS, TCP, and traffic analysis. |
| Incident Response | Practice incident triage, containment, and evidence preservation. |
| SIEM & SOC Operations | Explore alert investigation and event correlation. |
| Vulnerability Assessment | Understand vulnerabilities, risk prioritization, and remediation. |

### 📊 Training Environment
- Interactive training dashboard.
- Scenario-based exercises.
- Structured learning objectives.
- Practical investigation tasks.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend application development |
| Flask | Web framework and routing |
| SQLite | Local database storage |
| HTML5 | Web page structure |
| CSS3 | User interface styling |
| Jinja2 | Dynamic HTML templating |
| Git | Version control |
| GitHub | Source code hosting |
| Kali Linux | Development environment |

---

## 📂 Project Structure

```text
NEXUS/
│
├── app.py
├── assessments.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── challenge.html
│   ├── assessment.html
│   ├── results.html
│   ├── module.html
│   ├── recovery.html
│   └── sso.html
│
└── nexus_users.db
```

> The SQLite database is generated locally when the application runs. It is excluded from version control.

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3 installed.
- Git installed.
- Kali Linux or another Linux distribution.
- Basic knowledge of terminal commands.

### 1. Clone the repository

```bash
git clone https://github.com/Esco-bit/NEXUS-Cybersecurity-Training-Portal.git
```

### 2. Navigate to the project directory

```bash
cd NEXUS-Cybersecurity-Training-Portal
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python3 app.py
```

### 7. Access the portal

Open your browser and navigate to:

```text
http://127.0.0.1:5002
```

Register a training account to access the training environment.

---

## 📸 Screenshots

Screenshots of the application will be added here as development progresses.

Planned screenshots:

- Sign-in page
- Registration page
- Training dashboard
- Phishing assessment
- Assessment results
- Practical training modules

---

## 🔒 Security Notice

NEXUS is an educational cybersecurity project intended for local testing and authorized training.

- Use fictional training accounts.
- Never enter real personal credentials.
- Never use real email or external account passwords.
- Do not expose the development server to public networks.
- The application uses a development configuration and is not production-ready.
- Authentication, session management, and security controls require further hardening before deployment.

---

## 🗺️ Future Development

- [ ] Professional dashboard UI improvements.
- [ ] Admin dashboard with restricted access.
- [ ] Persistent assessment history.
- [ ] User progress tracking.
- [ ] Additional cybersecurity scenarios.
- [ ] Interactive log analysis exercises.
- [ ] Simulated SIEM alert investigation.
- [ ] Improved authentication security.
- [ ] Responsive mobile interface.
- [ ] Deployment in a controlled environment.

---

## 👨‍💻 Developer

**Esco-bit**

Cybersecurity student and aspiring Security Operations Center (SOC) Analyst, interested in defensive security, threat detection, Linux, network security, and incident response.

GitHub: [@Esco-bit](https://github.com/Esco-bit)

---

## 📄 License

This project is currently intended for educational and portfolio purposes. A formal open-source license may be added in a future release.

---

<div align="center">

**NEXUS — Learn to Detect. Practice to Defend.**

</div>
