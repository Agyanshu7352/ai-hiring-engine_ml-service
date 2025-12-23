class GapAnalyzer:
    def analyze(self, resume_data, jd_data, match_details):
        """Analyze gaps and provide recommendations"""
        missing_skills = match_details.get('missingSkills', [])
        
        recommendations = []
        improvement_areas = []
        
        if missing_skills:
            top_missing = missing_skills[:5]
            recommendations.append(f"Learn the following key skills: {', '.join(top_missing)}")
            improvement_areas.extend(missing_skills)
        
        if match_details.get('experienceMatch') != 'Good':
            recommendations.append("Gain more experience in relevant projects or roles")
            improvement_areas.append("Experience Level")
        
        if len(match_details.get('matchedSkills', [])) < 3:
            recommendations.append("Expand your skill set to better match job requirements")
            recommendations.append("Consider taking online courses or certifications")
        
        if not recommendations:
            recommendations.append("You're a great fit! Focus on interview preparation")
        
        return {
            'recommendations': recommendations,
            'improvementAreas': improvement_areas[:10]
        }