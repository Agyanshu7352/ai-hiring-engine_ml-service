import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

class ResumeParser:
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'nodejs', 'sql', 'mongodb',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'machine learning', 'deep learning',
            'tensorflow', 'pytorch', 'git', 'agile', 'scrum', 'rest api', 'api',
            'html', 'css', 'typescript', 'angular', 'vue.js', 'vue', 'express',
            'django', 'flask', 'spring boot', 'spring', 'c++', 'c#', '.net', 'php',
            'mysql', 'postgresql', 'redis', 'elasticsearch', 'jenkins', 'ci/cd',
            'linux', 'bash', 'shell', 'microservices', 'graphql', 'redux'
        ]
    
    def extract_email(self, text):
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone number from text"""
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def extract_skills(self, text):
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill.title())
        
        # Use NER for additional skill extraction
        if nlp:
            doc = nlp(text[:10000])  # Limit text size
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT']:
                    skill_candidate = ent.text
                    if len(skill_candidate) > 2 and skill_candidate.lower() not in [s.lower() for s in found_skills]:
                        found_skills.append(skill_candidate)
        
        return list(set(found_skills))[:30]  # Limit to 30 skills
    
    def extract_name(self, text):
        """Extract name from text (first non-empty line often contains name)"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line) > 2 and len(line) < 50 and not '@' in line:
                return line
        return "Candidate Name"
    
    def predict_seniority(self, text):
        """Predict seniority level"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect', 'staff']):
            return 'Senior'
        elif any(word in text_lower for word in ['junior', 'entry', 'associate', 'intern']):
            return 'Junior'
        else:
            return 'Mid-Level'
    
    def estimate_experience(self, text):
        """Estimate years of experience"""
        text_lower = text.lower()
        # Look for patterns like "5 years", "5+ years"
        exp_pattern = r'(\d+)\+?\s*years?'
        matches = re.findall(exp_pattern, text_lower)
        if matches:
            years = [int(m) for m in matches]
            return max(years) if years else 3
        return 3
    
    def parse(self, text):
        """Parse resume text and extract structured data"""
        return {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'experience': [],
            'education': [],
            'seniority': self.predict_seniority(text),
            'totalYearsExperience': self.estimate_experience(text)
        }