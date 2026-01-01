from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from utils.text_extractor import extract_text
from models.resume_parser import ResumeParser
from models.jd_parser import JDParser
from models.matcher import Matcher
from models.gap_analyzer import GapAnalyzer
from models.interview_generator import InterviewGenerator

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize models
resume_parser = ResumeParser()
jd_parser = JDParser()
matcher = Matcher()
gap_analyzer = GapAnalyzer()
interview_generator = InterviewGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'service': 'AI Hiring Engine ML Service'})

@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    console.log("Received request to /parse-resume");
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'Resume file is required'}), 400

        file = request.files['resume']

        if file.filename == '':
            return jsonify({'error': 'Empty file'}), 400

        # Save file temporarily
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        # Extract text
        extracted_text = extract_text(file_path)

        if not extracted_text:
            return jsonify({'error': 'Failed to extract text'}), 400

        parsed_data = resume_parser.parse(extracted_text)

        return jsonify({
            'success': True,
            'extractedText': extracted_text[:500],
            'parsedData': parsed_data
        })

    except Exception as e:
        print(f"Error in parse_resume: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/parse-jd', methods=['POST'])
def parse_jd():
    try:
        data = request.json
        description = data.get('description')
        
        if not description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Parse job description
        parsed_data = jd_parser.parse(description)
        
        return jsonify({
            'success': True,
            'parsedData': parsed_data
        })
    
    except Exception as e:
        print(f"Error in parse_jd: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/match', methods=['POST'])
def match():
    try:
        data = request.json
        resume_data = data.get('resume')
        jd_data = data.get('jobDescription')
        
        if not resume_data or not jd_data:
            return jsonify({'error': 'Resume and job description data are required'}), 400
        
        # Calculate match
        match_result = matcher.calculate_fit_score(resume_data, jd_data)
        
        return jsonify({
            'success': True,
            'fitScore': match_result['fitScore'],
            'matchDetails': match_result['matchDetails']
        })
    
    except Exception as e:
        print(f"Error in match: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/improve', methods=['POST'])
def improve():
    try:
        data = request.json
        resume_data = data.get('resume')
        jd_data = data.get('jobDescription')
        match_details = data.get('matchDetails')
        
        if not all([resume_data, jd_data, match_details]):
            return jsonify({'error': 'Missing required data'}), 400
        
        # Analyze gaps
        gap_analysis = gap_analyzer.analyze(resume_data, jd_data, match_details)
        
        return jsonify({
            'success': True,
            'recommendations': gap_analysis['recommendations'],
            'improvementAreas': gap_analysis['improvementAreas']
        })
    
    except Exception as e:
        print(f"Error in improve: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/interview', methods=['POST'])
def interview():
    try:
        data = request.json
        resume_data = data.get('resume')
        jd_data = data.get('jobDescription')
        
        if not resume_data or not jd_data:
            return jsonify({'error': 'Resume and job description data are required'}), 400
        
        # Generate interview questions
        questions = interview_generator.generate(resume_data, jd_data)
        
        return jsonify({
            'success': True,
            'questions': questions
        })
    
    except Exception as e:
        print(f"Error in interview: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
