"""
Data Analysis Script
Analyzes scraped job data to extract insights:
- Most common skills
- Top hiring companies
- Most active locations
- Job types distribution
- Experience levels
- Salary statistics
"""

import pandas as pd
import logging
from pathlib import Path
from collections import Counter
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobDataAnalyzer:
    """Analyze scraped job data"""
    
    def __init__(self, csv_file='../data/final/jobs.csv'):
        self.csv_file = csv_file
        self.df = None
        self.stats = {}
    
    def load_data(self):
        """Load job data from CSV"""
        try:
            csv_path = Path(self.csv_file)
            if not csv_path.exists():
                logger.error(f"Job data file not found: {self.csv_file}")
                return False
            
            self.df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(self.df)} job records")
            
            if len(self.df) == 0:
                logger.warning("No job records found in CSV")
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def analyze(self):
        """Run all analyses"""
        if not self.load_data():
            return False
        
        logger.info("=" * 70)
        logger.info("STARTING JOB DATA ANALYSIS")
        logger.info("=" * 70)
        
        self._basic_statistics()
        self._analyze_skills()
        self._analyze_companies()
        self._analyze_locations()
        self._analyze_employment_types()
        self._analyze_titles()
        self._analyze_salary()
        
        self._print_summary()
        self._save_stats()
        
        return True
    
    def _basic_statistics(self):
        """Calculate basic statistics"""
        logger.info("\n--- BASIC STATISTICS ---")
        
        total_jobs = len(self.df)
        unique_companies = self.df['company_name'].nunique()
        unique_locations = self.df['location'].nunique()
        
        logger.info(f"Total job listings: {total_jobs}")
        logger.info(f"Unique companies: {unique_companies}")
        logger.info(f"Unique locations: {unique_locations}")
        
        self.stats['total_jobs'] = total_jobs
        self.stats['unique_companies'] = unique_companies
        self.stats['unique_locations'] = unique_locations
    
    def _analyze_skills(self):
        """Analyze most common required skills"""
        logger.info("\n--- TOP 20 MOST REQUIRED SKILLS ---")
        
        # Extract all skills
        all_skills = []
        for skills_str in self.df['required_skills'].dropna():
            if isinstance(skills_str, str):
                # Handle different formats
                if ',' in skills_str:
                    skills = [s.strip() for s in skills_str.split(',')]
                else:
                    skills = skills_str.split()
                all_skills.extend(skills)
        
        # Count skill frequency
        skill_counter = Counter(all_skills)
        top_skills = skill_counter.most_common(20)
        
        if top_skills:
            logger.info("\nSkill Frequency:")
            for i, (skill, count) in enumerate(top_skills, 1):
                percentage = (count / len(self.df)) * 100
                logger.info(f"{i:2}. {skill:30} - {count:4} jobs ({percentage:5.1f}%)")
            
            self.stats['top_skills'] = {skill: count for skill, count in top_skills}
        else:
            logger.warning("No skills data found")
    
    def _analyze_companies(self):
        """Analyze top hiring companies"""
        logger.info("\n--- TOP 20 HIRING COMPANIES ---")
        
        company_counts = self.df['company_name'].value_counts().head(20)
        
        if len(company_counts) > 0:
            logger.info("\nCompany Job Listings:")
            for i, (company, count) in enumerate(company_counts.items(), 1):
                percentage = (count / len(self.df)) * 100
                logger.info(f"{i:2}. {company:40} - {count:3} jobs ({percentage:5.1f}%)")
            
            self.stats['top_companies'] = company_counts.to_dict()
        else:
            logger.warning("No company data found")
    
    def _analyze_locations(self):
        """Analyze job distribution by location"""
        logger.info("\n--- TOP 20 JOB LOCATIONS ---")
        
        location_counts = self.df['location'].value_counts().head(20)
        
        if len(location_counts) > 0:
            logger.info("\nLocation Distribution:")
            for i, (location, count) in enumerate(location_counts.items(), 1):
                percentage = (count / len(self.df)) * 100
                logger.info(f"{i:2}. {location:40} - {count:3} jobs ({percentage:5.1f}%)")
            
            self.stats['top_locations'] = location_counts.to_dict()
        else:
            logger.warning("No location data found")
    
    def _analyze_employment_types(self):
        """Analyze employment type distribution"""
        logger.info("\n--- EMPLOYMENT TYPE DISTRIBUTION ---")
        
        # Count valid employment types
        valid_types = self.df[self.df['employment_type'].notna()]['employment_type'].value_counts()
        unknown_count = len(self.df[self.df['employment_type'].isna()])
        
        logger.info("\nEmployment Types:")
        for emp_type, count in valid_types.items():
            percentage = (count / len(self.df)) * 100
            logger.info(f"  {emp_type:30} - {count:3} jobs ({percentage:5.1f}%)")
        
        if unknown_count > 0:
            percentage = (unknown_count / len(self.df)) * 100
            logger.info(f"  {'Unknown':30} - {unknown_count:3} jobs ({percentage:5.1f}%)")
        
        self.stats['employment_types'] = valid_types.to_dict()
        if unknown_count > 0:
            self.stats['employment_types']['Unknown'] = unknown_count
    
    def _analyze_titles(self):
        """Analyze job title patterns"""
        logger.info("\n--- TOP 20 JOB TITLES ---")
        
        title_counts = self.df['job_title'].value_counts().head(20)
        
        if len(title_counts) > 0:
            logger.info("\nMost Common Job Titles:")
            for i, (title, count) in enumerate(title_counts.items(), 1):
                percentage = (count / len(self.df)) * 100
                logger.info(f"{i:2}. {title:50} - {count:2} ({percentage:5.1f}%)")
            
            # Extract role patterns
            self._analyze_role_patterns()
            
            self.stats['top_titles'] = title_counts.to_dict()
        else:
            logger.warning("No job title data found")
    
    def _analyze_role_patterns(self):
        """Analyze role patterns (Intern, Junior, Senior, etc.)"""
        logger.info("\n--- ROLE LEVEL DISTRIBUTION ---")
        
        titles = self.df['job_title'].str.lower()
        
        patterns = {
            'Intern': len(titles[titles.str.contains('intern', na=False)]),
            'Entry-Level/Junior': len(titles[titles.str.contains('junior|entry|entry-level|associate|graduate', na=False)]),
            'Mid-Level': len(titles[titles.str.contains('mid|mid-level|senior engineer(?!.*staff)|developer|engineer(?!.*staff)', na=False)]),
            'Senior/Staff': len(titles[titles.str.contains('senior|staff|principal|lead', na=False)]),
        }
        
        logger.info("\nRole Levels:")
        for role, count in patterns.items():
            if count > 0:
                percentage = (count / len(self.df)) * 100
                logger.info(f"  {role:30} - {count:3} jobs ({percentage:5.1f}%)")
        
        self.stats['role_levels'] = patterns
    
    def _analyze_salary(self):
        """Analyze salary information"""
        logger.info("\n--- SALARY INFORMATION ---")
        
        salary_data = self.df[self.df['salary'].notna()]['salary']
        
        if len(salary_data) == 0:
            logger.warning("No salary data available")
            self.stats['salary_info'] = "No salary data found"
            return
        
        logger.info(f"Jobs with salary info: {len(salary_data)} ({(len(salary_data)/len(self.df)*100):.1f}%)")
        logger.info(f"Jobs without salary info: {len(self.df) - len(salary_data)} ({((len(self.df)-len(salary_data))/len(self.df)*100):.1f}%)")
        
        # Try to extract numeric salary values
        try:
            salary_values = pd.to_numeric(salary_data, errors='coerce')
            valid_salaries = salary_values.dropna()
            
            if len(valid_salaries) > 0:
                logger.info(f"\nSalary Statistics (where available):")
                logger.info(f"  Average: ${valid_salaries.mean():,.0f}")
                logger.info(f"  Median:  ${valid_salaries.median():,.0f}")
                logger.info(f"  Min:     ${valid_salaries.min():,.0f}")
                logger.info(f"  Max:     ${valid_salaries.max():,.0f}")
                
                self.stats['salary_info'] = {
                    'average': float(valid_salaries.mean()),
                    'median': float(valid_salaries.median()),
                    'min': float(valid_salaries.min()),
                    'max': float(valid_salaries.max()),
                    'count': len(valid_salaries)
                }
        except Exception as e:
            logger.debug(f"Could not parse salary values: {e}")
            logger.info("Sample salary entries:")
            for salary in salary_data.head(5):
                logger.info(f"  - {salary}")
    
    def _print_summary(self):
        """Print final summary"""
        logger.info("\n" + "=" * 70)
        logger.info("ANALYSIS SUMMARY")
        logger.info("=" * 70)
        
        logger.info(f"\nAnalysis covered {len(self.df)} job listings")
        logger.info(f"From {self.stats['unique_companies']} different companies")
        logger.info(f"Across {self.stats['unique_locations']} different locations")
        
        logger.info("\nTop 5 Most In-Demand Skills:")
        if 'top_skills' in self.stats:
            for i, (skill, count) in enumerate(list(self.stats['top_skills'].items())[:5], 1):
                logger.info(f"  {i}. {skill}")
        
        logger.info("\nTop 5 Hiring Companies:")
        if 'top_companies' in self.stats:
            for i, (company, count) in enumerate(list(self.stats['top_companies'].items())[:5], 1):
                logger.info(f"  {i}. {company} ({count} jobs)")
        
        logger.info("\nTop 5 Job Locations:")
        if 'top_locations' in self.stats:
            for i, (location, count) in enumerate(list(self.stats['top_locations'].items())[:5], 1):
                logger.info(f"  {i}. {location} ({count} jobs)")
        
        logger.info("\n" + "=" * 70)
    
    def _save_stats(self):
        """Save analysis statistics to JSON"""
        try:
            output_file = Path('../data/final/analysis_stats.json')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(self.stats, f, indent=2, default=str)
            
            logger.info(f"\n✓ Analysis statistics saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")


def main():
    """Main entry point"""
    analyzer = JobDataAnalyzer(csv_file='../data/final/jobs.csv')
    if analyzer.analyze():
        logger.info("\n✓ Analysis completed successfully")
        return 0
    else:
        logger.error("\n✗ Analysis failed")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
