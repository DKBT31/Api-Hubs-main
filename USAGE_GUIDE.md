# How to Use the Extracted JSON Resume Data

The API now successfully extracts structured information from resumes. Here are practical ways to use this data:

## 🎯 **Practical Use Cases:**

### 1. **HR/Recruitment System Integration**
```python
# Example: Filter candidates by skills
def filter_by_skills(resume_data, required_skills):
    candidate_skills = resume_data["gemini_response"]["skill"]
    matches = [skill for skill in required_skills if skill in candidate_skills]
    return len(matches) / len(required_skills) * 100  # Match percentage

# Example usage:
required_skills = ["Java", "Spring Boot", "React"]
match_percentage = filter_by_skills(resume_data, required_skills)
print(f"Skill match: {match_percentage}%")
```

### 2. **Candidate Database Storage**
```python
# Example: Store in database
import sqlite3

def store_candidate(resume_data):
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    
    data = resume_data["gemini_response"]
    cursor.execute('''
        INSERT INTO candidates (name, phone, profession, skills, context)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data["fullname"],
        data["phone"], 
        data["profession"],
        ",".join(data["skill"]),
        data["context"]
    ))
    conn.commit()
    conn.close()
```

### 3. **Resume Scoring/Ranking**
```python
# Example: Score resumes based on criteria
def score_resume(resume_data, job_requirements):
    data = resume_data["gemini_response"]
    score = 0
    
    # Skill matching (40% weight)
    skill_match = len([s for s in job_requirements["skills"] if s in data["skill"]])
    score += (skill_match / len(job_requirements["skills"])) * 40
    
    # Experience level (30% weight) 
    if job_requirements["profession"].lower() in data["profession"].lower():
        score += 30
        
    # Education (30% weight)
    if any("University" in edu["institution"] for edu in data["education"]):
        score += 30
        
    return min(score, 100)
```

### 4. **Export to Different Formats**
```python
# Export to CSV
import csv

def export_to_csv(resume_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Phone', 'Profession', 'Skills', 'Education'])
        
        for resume in resume_list:
            data = resume["gemini_response"] 
            writer.writerow([
                data["fullname"],
                data["phone"],
                data["profession"], 
                "; ".join(data["skill"]),
                "; ".join([edu["institution"] for edu in data["education"]])
            ])

# Export to Excel
import pandas as pd

def export_to_excel(resume_list, filename):
    df_data = []
    for resume in resume_list:
        data = resume["gemini_response"]
        df_data.append({
            'Name': data["fullname"],
            'Phone': data["phone"],
            'Profession': data["profession"],
            'Skills': ", ".join(data["skill"]),
            'Education': "; ".join([edu["institution"] for edu in data["education"]]),
            'Context': data["context"]
        })
    
    df = pd.DataFrame(df_data)
    df.to_excel(filename, index=False)
```

### 5. **Search and Filter System**
```python
# Advanced search functionality
def search_candidates(resume_database, search_criteria):
    results = []
    
    for resume in resume_database:
        data = resume["gemini_response"]
        match_score = 0
        
        # Search by name
        if search_criteria.get("name"):
            if search_criteria["name"].lower() in data["fullname"].lower():
                match_score += 1
                
        # Search by skills
        if search_criteria.get("skills"):
            for skill in search_criteria["skills"]:
                if skill.lower() in [s.lower() for s in data["skill"]]:
                    match_score += 1
                    
        # Search by profession
        if search_criteria.get("profession"):
            if search_criteria["profession"].lower() in data["profession"].lower():
                match_score += 1
                
        if match_score > 0:
            results.append((resume, match_score))
    
    # Sort by match score
    return sorted(results, key=lambda x: x[1], reverse=True)
```

### 6. **Integration with Frontend Applications**
```javascript
// Example: React component to display candidate info
function CandidateCard({ resumeData }) {
  const candidate = resumeData.gemini_response;
  
  return (
    <div className="candidate-card">
      <h3>{candidate.fullname}</h3>
      <p><strong>Profession:</strong> {candidate.profession}</p>
      <p><strong>Phone:</strong> {candidate.phone}</p>
      <p><strong>Specialty:</strong> {candidate.specialty}</p>
      
      <div className="skills">
        <h4>Skills:</h4>
        {candidate.skill.map(skill => (
          <span key={skill} className="skill-tag">{skill}</span>
        ))}
      </div>
      
      <div className="education">
        <h4>Education:</h4>
        {candidate.education.map(edu => (
          <div key={edu.institution}>
            <strong>{edu.institution}</strong>
            {edu.gpa && ` - GPA: ${edu.gpa}`}
            {edu.period && ` (${edu.period})`}
          </div>
        ))}
      </div>
      
      <p className="context">{candidate.context}</p>
    </div>
  );
}
```

### 7. **API Integration Examples**
```python
# Example: Webhook to external systems
import requests

def send_to_ats_system(resume_data):
    """Send processed resume to Applicant Tracking System"""
    ats_endpoint = "https://your-ats-system.com/api/candidates"
    
    payload = {
        "candidate_name": resume_data["gemini_response"]["fullname"],
        "contact_info": {
            "phone": resume_data["gemini_response"]["phone"]
        },
        "skills": resume_data["gemini_response"]["skill"],
        "profession": resume_data["gemini_response"]["profession"],
        "education": resume_data["gemini_response"]["education"],
        "summary": resume_data["gemini_response"]["context"]
    }
    
    response = requests.post(ats_endpoint, json=payload)
    return response.status_code == 200
```

## 🔧 **Next Steps - Choose Your Use Case:**

1. **Build a Candidate Database** - Store and search resumes
2. **Create Matching System** - Match candidates to job requirements  
3. **Develop Analytics** - Generate insights from resume data
4. **Frontend Integration** - Build a web interface
5. **Enterprise Integration** - Connect to existing HR systems

## 📊 **API Endpoints You Can Build:**

- `GET /candidates` - List all processed candidates
- `GET /candidates/search?skills=Java,Python` - Search by skills
- `GET /candidates/{id}` - Get specific candidate details
- `POST /candidates/bulk-upload` - Process multiple resumes
- `GET /analytics/skills` - Get skill distribution analytics

Would you like me to help you implement any of these specific use cases?
