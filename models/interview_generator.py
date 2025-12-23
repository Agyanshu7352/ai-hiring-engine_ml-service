class InterviewGenerator:
    def __init__(self):
        self.technical_questions = {
            'Python': [
                "Explain the difference between list and tuple in Python",
                "What are Python decorators and how do you use them?",
                "Explain GIL in Python and its impact on multithreading"
            ],
            'JavaScript': [
                "What is the difference between let, var, and const?",
                "Explain closures in JavaScript with an example",
                "What is event delegation and why is it useful?"
            ],
            'React': [
                "What is the virtual DOM and how does it work?",
                "Explain the difference between useEffect and useLayoutEffect",
                "What are React hooks and why were they introduced?"
            ],
            'Node.Js': [
                "Explain the event loop in Node.js",
                "What is middleware in Express.js?",
                "How do you handle asynchronous operations in Node.js?"
            ],
            'Sql': [
                "Explain the difference between INNER JOIN and LEFT JOIN",
                "What are indexes and how do they improve performance?",
                "Explain database normalization"
            ],
            'Machine Learning': [
                "Explain the bias-variance tradeoff",
                "What is overfitting and how do you prevent it?",
                "Explain the difference between supervised and unsupervised learning"
            ]
        }
        
        self.behavioral_questions = [
            "Tell me about a challenging project you worked on",
            "How do you handle tight deadlines?",
            "Describe a time when you had to learn a new technology quickly",
            "How do you approach debugging complex issues?",
            "Tell me about a time you worked in a team"
        ]
    
    def generate(self, resume_data, jd_data):
        """Generate interview questions"""
        questions = []
        
        # Add behavioral questions
        questions.extend(self.behavioral_questions[:2])
        
        # Add technical questions based on skills
        matched_skills = resume_data.get('skills', [])
        required_skills = jd_data.get('requiredSkills', [])
        
        for skill in required_skills[:5]:
            skill_title = skill.title()
            if skill_title in self.technical_questions:
                questions.extend(self.technical_questions[skill_title][:2])
        
        # Add general questions
        questions.append("Walk me through your most recent project")
        questions.append("How do you stay updated with the latest technologies?")
        
        # Add seniority-specific questions
        seniority = jd_data.get('seniority', '')
        if seniority == 'Senior':
            questions.append("Describe your experience mentoring junior developers")
            questions.append("How do you make architectural decisions?")
        
        return questions[:12]  # Return top 12 questions