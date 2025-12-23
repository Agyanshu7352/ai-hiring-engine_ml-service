import numpy as np

class Matcher:
    def __init__(self):
        pass
    
    def calculate_fit_score(self, resume_data, jd_data):
        """Calculate fit score between resume and job description"""
        # Extract skills
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        required_skills = set([s.lower() for s in jd_data.get('requiredSkills', [])])
        optional_skills = set([s.lower() for s in jd_data.get('optionalSkills', [])])
        
        all_jd_skills = required_skills.union(optional_skills)
        
        # Calculate matches
        matched_skills = resume_skills.intersection(all_jd_skills)
        missing_skills = required_skills - resume_skills
        
        # Calculate skill overlap
        if len(required_skills) > 0:
            skill_overlap = (len(matched_skills) / len(required_skills)) * 100
        else:
            skill_overlap = 50
        
        # Seniority matching
        resume_seniority = resume_data.get('seniority', 'Mid-Level')
        jd_seniority = jd_data.get('seniority', 'Mid-Level')
        seniority_match = 1.0 if resume_seniority == jd_seniority else 0.5
        
        # Calculate final fit score (weighted)
        fit_score = (skill_overlap * 0.7) + (seniority_match * 30)
        fit_score = min(100, max(0, fit_score))  # Ensure between 0-100
        
        return {
            'fitScore': round(fit_score, 2),
            'matchDetails': {
                'matchedSkills': list(matched_skills),
                'missingSkills': list(missing_skills),
                'skillOverlap': round(skill_overlap, 2),
                'experienceMatch': 'Good' if seniority_match == 1.0 else 'Partial'
            }
        }