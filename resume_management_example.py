"""
Practical Example: Building a Resume Management System
Using the extracted JSON data from your API
"""

import requests
import json
import sqlite3
from datetime import datetime
import pandas as pd

class ResumeManager:
    def __init__(self, api_url="http://127.0.0.1:9002"):
        self.api_url = api_url
        self.setup_database()
    
    def setup_database(self):
        """Create SQLite database to store processed resumes"""
        conn = sqlite3.connect('resume_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                profession TEXT,
                specialty TEXT,
                skills TEXT,
                education TEXT,
                context TEXT,
                processed_date TIMESTAMP,
                raw_json TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def process_resume(self, file_path):
        """Upload resume to API and get structured data"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.api_url}/upload", files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return None
    
    def save_candidate(self, resume_data):
        """Save processed resume data to database"""
        if not resume_data or resume_data.get('status') != 'success':
            return False
        
        try:
            # Parse the JSON response from Gemini
            gemini_response = resume_data['gemini_response']
            if isinstance(gemini_response, str):
                # Extract JSON from markdown code block
                start = gemini_response.find('```json') + 7
                end = gemini_response.rfind('```')
                gemini_response = json.loads(gemini_response[start:end])
            
            conn = sqlite3.connect('resume_database.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO candidates 
                (name, phone, profession, specialty, skills, education, context, processed_date, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                gemini_response.get('fullname', ''),
                gemini_response.get('phone', ''),
                gemini_response.get('profession', ''),
                gemini_response.get('specialty', ''),
                json.dumps(gemini_response.get('skill', [])),
                json.dumps(gemini_response.get('education', [])),
                gemini_response.get('context', ''),
                datetime.now(),
                json.dumps(resume_data)
            ))
            
            conn.commit()
            conn.close()
            print(f"✅ Saved candidate: {gemini_response.get('fullname', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving candidate: {e}")
            return False
    
    def search_candidates(self, **criteria):
        """Search candidates by various criteria"""
        conn = sqlite3.connect('resume_database.db')
        
        query = "SELECT * FROM candidates WHERE 1=1"
        params = []
        
        if criteria.get('name'):
            query += " AND name LIKE ?"
            params.append(f"%{criteria['name']}%")
        
        if criteria.get('profession'):
            query += " AND profession LIKE ?"
            params.append(f"%{criteria['profession']}%")
        
        if criteria.get('skill'):
            query += " AND skills LIKE ?"
            params.append(f"%{criteria['skill']}%")
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_skill_analytics(self):
        """Generate analytics on skills from all candidates"""
        conn = sqlite3.connect('resume_database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT skills FROM candidates")
        all_skills = []
        
        for row in cursor.fetchall():
            try:
                skills = json.loads(row[0])
                all_skills.extend(skills)
            except:
                continue
        
        conn.close()
        
        # Count skill frequency
        skill_count = {}
        for skill in all_skills:
            skill_count[skill] = skill_count.get(skill, 0) + 1
        
        # Sort by frequency
        return sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
    
    def export_candidates(self, filename="candidates_export.xlsx"):
        """Export all candidates to Excel"""
        conn = sqlite3.connect('resume_database.db')
        df = pd.read_sql_query("SELECT * FROM candidates", conn)
        conn.close()
        
        df.to_excel(filename, index=False)
        print(f"✅ Exported {len(df)} candidates to {filename}")
    
    def match_job_requirements(self, job_requirements):
        """Find candidates matching job requirements"""
        required_skills = job_requirements.get('skills', [])
        required_profession = job_requirements.get('profession', '')
        
        candidates = self.search_candidates()
        matched_candidates = []
        
        for _, candidate in candidates.iterrows():
            try:
                candidate_skills = json.loads(candidate['skills'])
                
                # Calculate skill match percentage
                matches = sum(1 for skill in required_skills 
                             if any(skill.lower() in cs.lower() for cs in candidate_skills))
                skill_match_percent = (matches / len(required_skills)) * 100 if required_skills else 0
                
                # Check profession match
                profession_match = required_profession.lower() in candidate['profession'].lower()
                
                if skill_match_percent > 0 or profession_match:
                    matched_candidates.append({
                        'candidate': candidate,
                        'skill_match_percent': skill_match_percent,
                        'profession_match': profession_match
                    })
            except:
                continue
        
        # Sort by match score
        return sorted(matched_candidates, 
                     key=lambda x: x['skill_match_percent'], reverse=True)

# Example usage
if __name__ == "__main__":
    # Initialize the resume manager
    manager = ResumeManager()
    
    print("🚀 Resume Management System")
    print("=" * 50)
    
    # Example 1: Process a single resume
    print("\n1. Processing a resume...")
    # Uncomment to process an actual file:
    # result = manager.process_resume("path/to/your/resume.pdf")
    # if result:
    #     manager.save_candidate(result)
    
    # Example 2: Search candidates
    print("\n2. Searching candidates...")
    java_developers = manager.search_candidates(skill="Java")
    print(f"Found {len(java_developers)} Java developers")
    
    # Example 3: Get skill analytics
    print("\n3. Skill Analytics...")
    top_skills = manager.get_skill_analytics()[:10]
    print("Top 10 skills:")
    for skill, count in top_skills:
        print(f"  {skill}: {count} candidates")
    
    # Example 4: Match job requirements
    print("\n4. Job Matching...")
    job_req = {
        'skills': ['Java', 'Spring Boot', 'React'],
        'profession': 'Software Engineer'
    }
    matches = manager.match_job_requirements(job_req)
    print(f"Found {len(matches)} matching candidates")
    
    # Example 5: Export data
    print("\n5. Exporting data...")
    manager.export_candidates("all_candidates.xlsx")
    
    print("\n✅ Resume Management System Demo Complete!")
    print("\nNext steps:")
    print("- Add more resumes using: manager.process_resume('file.pdf')")
    print("- Search candidates using: manager.search_candidates(name='John')")
    print("- Generate reports using: manager.get_skill_analytics()")
