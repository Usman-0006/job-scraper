#!/usr/bin/env python3
"""
Generate realistic sample job data for testing and demonstration
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def generate_sample_jobs():
    """Generate 10 realistic diverse sample jobs with real data"""
    
    jobs = [
        {
            'job_title': 'Senior Python Developer',
            'company_name': 'TechCorp',
            'location': 'San Francisco, CA',
            'department': 'Engineering',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-15',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/senior-python-developer',
            'job_description': 'We are looking for a senior Python developer with 5+ years of experience in building scalable web applications. Must be proficient in Django, FastAPI, and PostgreSQL. You will lead a team of engineers and mentor junior developers. Experience with AWS and Docker is critical.',
            'required_skills': 'Python, Django, FastAPI, PostgreSQL, Docker, Git, AWS, Microservices',
            'experience_level': 'Senior',
            'salary': '150000-200000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Junior JavaScript Developer',
            'company_name': 'WebDev Inc',
            'location': 'Remote',
            'department': 'Frontend',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-17',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/junior-javascript',
            'job_description': 'Excellent opportunity for junior developers to learn React and modern JavaScript. We provide comprehensive mentoring and training programs. Work on real products with experienced engineers. Remote work with flexible hours and team collaboration.',
            'required_skills': 'JavaScript, React, HTML, CSS, Git, Node.js, REST APIs',
            'experience_level': 'Entry-level',
            'salary': '50000-70000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Data Analyst Intern',
            'company_name': 'DataTech Solutions',
            'location': 'New York, NY',
            'department': 'Analytics',
            'employment_type': 'Internship',
            'posted_date': '2026-03-19',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/data-analyst-intern',
            'job_description': 'Internship program for aspiring data analysts. Work with SQL, Python, and Tableau to analyze business data and create meaningful insights. Learn from experienced data scientists and business analysts. 3-month program with potential for full-time conversion.',
            'required_skills': 'SQL, Python, Tableau, Excel, Statistics, Business Analysis',
            'experience_level': 'Intern',
            'salary': '15-20/hour',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'DevOps Engineer',
            'company_name': 'CloudOps',
            'location': 'Seattle, WA',
            'department': 'Infrastructure',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-13',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/devops-engineer',
            'job_description': 'Looking for experienced DevOps engineer to manage our Kubernetes infrastructure on AWS. You will be responsible for CI/CD pipelines, infrastructure automation, monitoring, and incident response. Experience with IaC tools like Terraform is essential.',
            'required_skills': 'Kubernetes, Docker, AWS, Terraform, Bash, Jenkins, Prometheus, ELK, Linux',
            'experience_level': 'Mid-level',
            'salary': '100000-140000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Product Manager',
            'company_name': 'Startup XYZ',
            'location': 'Remote',
            'department': 'Product',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-18',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/product-manager',
            'job_description': 'We are seeking an experienced PM to lead product strategy and roadmap for our growing SaaS platform. 3+ years PM experience in B2B SaaS required. You will work closely with engineering, design, and marketing teams to drive product innovation and user growth.',
            'required_skills': 'Product Strategy, Data Analytics, SQL, Communication, Figma, JIRA, User Research',
            'experience_level': 'Mid-level',
            'salary': '120000-160000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Data Scientist - Machine Learning',
            'company_name': 'AI Labs',
            'location': 'San Francisco, CA',
            'department': 'ML/AI',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-16',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/data-scientist-ml',
            'job_description': 'Build and deploy production ML models to improve our recommendation engine and user experience. PhD in ML/Computer Science or 5+ years industry experience in production ML systems preferred. Experience with PyTorch, TensorFlow, and cloud ML platforms required.',
            'required_skills': 'Python, Machine Learning, TensorFlow, PyTorch, Statistics, SQL, Pandas, MLOps',
            'experience_level': 'Senior',
            'salary': '140000-200000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Senior QA Automation Engineer',
            'company_name': 'Quality First',
            'location': 'Austin, TX',
            'department': 'QA',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-14',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/qa-automation',
            'job_description': 'Senior test automation engineer needed for our growing agile team. Lead QA strategy and mentor junior QA engineers. Selenium and Python experience required. Experience with CI/CD integration, performance testing, and test frameworks essential.',
            'required_skills': 'Selenium, Python, JavaScript, Test Automation, Jira, Jenkins, Performance Testing, API Testing',
            'experience_level': 'Mid-level',
            'salary': '80000-110000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Backend Developer - TypeScript/Node.js',
            'company_name': 'Modern Stack Inc',
            'location': 'Remote',
            'department': 'Backend',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-12',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/backend-typescript',
            'job_description': 'Build scalable backend services using Node.js and TypeScript for millions of users. 3+ years experience with modern backend development. Experience with REST APIs, GraphQL, and microservices architecture required. Work with PostgreSQL and Redis for data persistence.',
            'required_skills': 'TypeScript, Node.js, Express, GraphQL, REST APIs, PostgreSQL, Redis, Docker, Microservices',
            'experience_level': 'Mid-level',
            'salary': '90000-130000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Cloud Solutions Architect',
            'company_name': 'CloudTech Solutions',
            'location': 'Boston, MA',
            'department': 'Engineering',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-10',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/cloud-architect',
            'job_description': 'Design and implement cloud solutions for enterprise clients. 7+ years experience with AWS, Azure, and/or GCP required. Lead cloud transformation initiatives and migrations. Work with stakeholders to define architecture, security, and best practices for scalable systems.',
            'required_skills': 'AWS, Azure, GCP, Kubernetes, Terraform, Python, System Design, Security, Compliance',
            'experience_level': 'Senior',
            'salary': '150000-200000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Frontend Engineer - React',
            'company_name': 'UI Masters',
            'location': 'Denver, CO',
            'department': 'Frontend',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-11',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/frontend-react',
            'job_description': 'Build beautiful, responsive, and performant user interfaces using React. 2+ years experience with modern frontend tools and best practices. Knowledge of state management, testing, and accessibility standards required. Work in agile scrum environment with cross-functional teams.',
            'required_skills': 'React, TypeScript, CSS, Redux, Jest, Webpack, Responsive Design, Accessibility, Git',
            'experience_level': 'Mid-level',
            'salary': '80000-120000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        },
        {
            'job_title': 'Security Engineer',
            'company_name': 'SecureNet',
            'location': 'Arlington, VA',
            'department': 'Security',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-09',
            'job_url': 'https://jobs.punjab.gov.pk/job_detail/security-engineer',
            'job_description': 'Join our security team to protect infrastructure and applications from cyber threats. 4+ years in security engineering or related field. Experience with penetration testing, vulnerability assessment, and security tools required. Knowledge of OWASP Top 10 and secure coding practices essential.',
            'required_skills': 'Security, Penetration Testing, Network Security, Cloud Security, Cryptography, SIEM, Firewalls',
            'experience_level': 'Mid-level',
            'salary': '110000-150000',
            'source_board': 'punjab_gov',
            'scrape_date': datetime.now().isoformat()
        }
    ]
    
    return jobs


def save_to_csv(jobs, filename):
    """Save jobs to CSV file"""
    if not jobs:
        print("No jobs to save")
        return False
    
    try:
        # Create directory if it doesn't exist
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        # Define CSV columns
        fieldnames = [
            'job_title', 'company_name', 'location', 'department',
            'employment_type', 'posted_date', 'job_url', 'job_description',
            'required_skills', 'experience_level', 'salary', 'source_board',
            'scrape_date'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for job in jobs:
                writer.writerow(job)
        
        print(f"✓ Saved {len(jobs)} jobs to {filename}")
        return True
    
    except Exception as e:
        print(f"✗ Error saving to CSV: {e}")
        return False


def save_to_json(jobs, filename):
    """Save jobs to JSON file"""
    if not jobs:
        print("No jobs to save")
        return False
    
    try:
        # Create directory if it doesn't exist
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(jobs)} jobs to {filename}")
        return True
    
    except Exception as e:
        print(f"✗ Error saving to JSON: {e}")
        return False


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SAMPLE JOB DATA GENERATOR")
    print("=" * 70)
    
    # Generate sample jobs
    print("\nGenerating 10 sample jobs...")
    jobs = generate_sample_jobs()
    
    # Save to CSV
    csv_path = '../data/final/jobs.csv'
    print(f"\nSaving to CSV: {csv_path}")
    csv_success = save_to_csv(jobs, csv_path)
    
    # Save to JSON
    json_path = '../data/final/jobs.json'
    print(f"Saving to JSON: {json_path}")
    json_success = save_to_json(jobs, json_path)
    
    if csv_success and json_success:
        print("\n" + "=" * 70)
        print("✓ SAMPLE DATA GENERATION COMPLETE!")
        print("=" * 70)
        print(f"\nGenerated {len(jobs)} realistic job postings:")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['job_title']} at {job['company_name']} ({job['experience_level']})")
        print("\n✓ Ready for analysis and visualization!")
        print("=" * 70 + "\n")
    else:
        print("\n✗ Error during sample data generation")
