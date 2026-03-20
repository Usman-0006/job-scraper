"""
Data Visualization Script
Creates charts for job data analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobDataVisualizer:
    """Create visualizations of job data"""
    
    def __init__(self, csv_file='../data/final/jobs.csv', output_dir='../data/final'):
        self.csv_file = csv_file
        self.output_dir = Path(output_dir)
        self.df = None
    
    def load_data(self):
        """Load job data from CSV"""
        try:
            csv_path = Path(self.csv_file)
            if not csv_path.exists():
                logger.error(f"Job data file not found: {self.csv_file}")
                return False
            
            self.df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(self.df)} job records for visualization")
            return True
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def create_visualizations(self):
        """Create all visualizations"""
        if not self.load_data():
            return False
        
        logger.info("Creating visualizations...")
        
        try:
            self._plot_companies()
            self._plot_locations()
            self._plot_employment_types()
            self._plot_top_titles()
            
            logger.info("✓ All visualizations created successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            return False
    
    def _plot_companies(self):
        """Plot top hiring companies"""
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            company_counts = self.df['company_name'].value_counts().head(15)
            company_counts.plot(kind='barh', ax=ax, color='steelblue')
            
            ax.set_xlabel('Number of Job Listings')
            ax.set_ylabel('Company')
            ax.set_title('Top 15 Companies by Job Listings')
            ax.invert_yaxis()
            
            plt.tight_layout()
            output_file = self.output_dir / 'top_companies.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Saved: {output_file}")
            plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting companies: {e}")
    
    def _plot_locations(self):
        """Plot job distribution by location"""
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            location_counts = self.df['location'].value_counts().head(15)
            location_counts.plot(kind='barh', ax=ax, color='forestgreen')
            
            ax.set_xlabel('Number of Job Listings')
            ax.set_ylabel('Location')
            ax.set_title('Top 15 Job Locations')
            ax.invert_yaxis()
            
            plt.tight_layout()
            output_file = self.output_dir / 'top_locations.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Saved: {output_file}")
            plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting locations: {e}")
    
    def _plot_employment_types(self):
        """Plot employment type distribution"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            employment_counts = self.df['employment_type'].value_counts()
            
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700', '#FF99CC']
            employment_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors[:len(employment_counts)])
            
            ax.set_ylabel('')
            ax.set_title('Job Distribution by Employment Type')
            
            plt.tight_layout()
            output_file = self.output_dir / 'employment_types.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Saved: {output_file}")
            plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting employment types: {e}")
    
    def _plot_top_titles(self):
        """Plot top job titles"""
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            title_counts = self.df['job_title'].value_counts().head(12)
            title_counts.plot(kind='barh', ax=ax, color='coral')
            
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Job Title')
            ax.set_title('Top 12 Most Common Job Titles')
            ax.invert_yaxis()
            
            plt.tight_layout()
            output_file = self.output_dir / 'top_titles.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Saved: {output_file}")
            plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting titles: {e}")


def main():
    """Main entry point"""
    visualizer = JobDataVisualizer()
    return 0 if visualizer.create_visualizations() else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
