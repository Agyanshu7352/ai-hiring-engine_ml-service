import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

class JDParser:
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'nodejs', 'sql', 'mongodb',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'machine learning', 'deep learning',
            'tensorflow', 'pytorch', 'git', 'agile', 'scrum', 'rest api', 'api',
            'html', 'css', 'typescript', 'angular', 'vue.js', 'vue', 'express',
            'django', 'flask', 'spring boot', 'spring', 'c++', 'c#', '.net', 'php'
        ]
    
    def extract_skills(self, text):
        """Extract skills from job description"""
        text_lower = text.lower()
        required = []
        optional = []
        
        # Split into sections if possible
        if 'required' in text_lower or 'must have' in text_lower:
            # Try to separate required and optional
            for skill in self.skill_keywords:
                if skill in text_lower:
                    # Simple heuristic: if mentioned in first half, likely required
                    if skill in text_lower[:len(text_lower)//2]:
                        required.append(skill.title())
                    else:
                        optional.append(skill.title())
        else:
            # All skills are required
            for skill in self.skill_keywords:
                if skill in text_lower:
                    required.append(skill.title())
        
        return required, optional
    
    def extract_keywords(self, text):
        """Extract important keywords"""
        if not nlp:
            return []
        
        doc = nlp(text[:5000])  # Limit text size
        keywords = []
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 3:
                keywords.append(token.text)
        return list(set(keywords))[:20]
    
    def detect_seniority(self, text):
        """Detect seniority level"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'staff', 'sr.']):
            return 'Senior'
        elif any(word in text_lower for word in ['junior', 'entry', 'associate', 'jr.']):
            return 'Junior'
        else:
            return 'Mid-Level'
    
    def parse(self, description):
        """Parse job description"""
        required_skills, optional_skills = self.extract_skills(description)
        
        return {
            'requiredSkills': required_skills,
            'optionalSkills': optional_skills,
            'keywords': self.extract_keywords(description),
            'seniority': self.detect_seniority(description),
            'experience': '3-5 years'
        }