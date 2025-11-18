# app_simple.py
import streamlit as st
import pandas as pd
import numpy as np
import re

# Set page config first
st.set_page_config(
    page_title="Smart Career AI Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .fit-score {
        font-weight: bold;
        color: #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

class SimpleCareerRecommender:
    def __init__(self):
        self.courses_df = self.generate_courses()
    
    def generate_courses(self):
        """Generate course catalog"""
        courses = [
            # Programming & Development
            {"title": "Python for Beginners", "provider": "Coursera", "duration": "6 weeks", 
             "prerequisites": ["none"], "skill_tags": ["python", "programming", "basic coding"], "level": "beginner", 
             "link": "https://coursera.org/learn/python-basics", "domain": "software development", "cost": "free"},
            
            {"title": "Web Development Bootcamp", "provider": "Udemy", "duration": "12 weeks", 
             "prerequisites": ["html", "css"], "skill_tags": ["javascript", "react", "node.js", "web development"], "level": "beginner", 
             "link": "https://udemy.com/web-dev", "domain": "web development", "cost": "paid"},
            
            {"title": "JavaScript Fundamentals", "provider": "FreeCodeCamp", "duration": "8 weeks", 
             "prerequisites": ["html", "css"], "skill_tags": ["javascript", "frontend", "web development"], "level": "beginner", 
             "link": "https://freecodecamp.org/javascript", "domain": "web development", "cost": "free"},
            
            # Data Science
            {"title": "Data Science Fundamentals", "provider": "Coursera", "duration": "10 weeks", 
             "prerequisites": ["python", "statistics"], "skill_tags": ["data science", "python", "pandas", "data analysis"], "level": "intermediate", 
             "link": "https://coursera.org/data-science", "domain": "data science", "cost": "free"},
            
            {"title": "Machine Learning Specialization", "provider": "Coursera", "duration": "16 weeks", 
             "prerequisites": ["python", "linear algebra"], "skill_tags": ["machine learning", "python", "scikit-learn"], "level": "intermediate", 
             "link": "https://coursera.org/machine-learning", "domain": "artificial intelligence", "cost": "paid"},
            
            # Cloud & DevOps
            {"title": "AWS Cloud Practitioner", "provider": "AWS", "duration": "4 weeks", 
             "prerequisites": ["none"], "skill_tags": ["aws", "cloud computing"], "level": "beginner", 
             "link": "https://aws.amazon.com/training", "domain": "cloud computing", "cost": "free"},
            
            {"title": "Docker and Kubernetes", "provider": "Udemy", "duration": "6 weeks", 
             "prerequisites": ["linux"], "skill_tags": ["docker", "kubernetes", "containers"], "level": "intermediate", 
             "link": "https://udemy.com/docker-kubernetes", "domain": "devops", "cost": "paid"},
            
            # Mobile Development
            {"title": "React Native Mobile Development", "provider": "Udemy", "duration": "10 weeks", 
             "prerequisites": ["javascript"], "skill_tags": ["react native", "mobile", "javascript"], "level": "intermediate", 
             "link": "https://udemy.com/react-native", "domain": "mobile development", "cost": "paid"},
            
            # Cybersecurity
            {"title": "Cybersecurity Fundamentals", "provider": "edX", "duration": "6 weeks", 
             "prerequisites": ["none"], "skill_tags": ["cybersecurity", "security", "networking"], "level": "beginner", 
             "link": "https://edx.org/cybersecurity", "domain": "cybersecurity", "cost": "free"},
            
            # Business & Soft Skills
            {"title": "Project Management Professional", "provider": "PMI", "duration": "8 weeks", 
             "prerequisites": ["project experience"], "skill_tags": ["project management", "leadership"], "level": "intermediate", 
             "link": "https://pmi.org/pmp", "domain": "business", "cost": "paid"},
        ]
        
        return pd.DataFrame(courses)
    
    def calculate_similarity(self, user_skills, course_skills):
        """Simple keyword-based similarity calculation"""
        user_skills_lower = [skill.lower() for skill in user_skills]
        course_skills_lower = [skill.lower() for skill in course_skills]
        
        matches = 0
        for user_skill in user_skills_lower:
            for course_skill in course_skills_lower:
                if user_skill in course_skill or course_skill in user_skill:
                    matches += 1
                    break
        
        return matches / len(user_skills_lower) if user_skills_lower else 0
    
    def calculate_level_match(self, user_level, course_level):
        """Calculate level compatibility"""
        level_scores = {
            'beginner': {'beginner': 1.0, 'intermediate': 0.7, 'advanced': 0.3},
            'intermediate': {'beginner': 0.8, 'intermediate': 1.0, 'advanced': 0.7},
            'advanced': {'beginner': 0.5, 'intermediate': 0.8, 'advanced': 1.0}
        }
        return level_scores.get(user_level, {}).get(course_level, 0.5)
    
    def recommend_courses(self, user_profile, top_k=8):
        """Generate recommendations using simple matching"""
        user_skills = user_profile.get('technical_skills', [])
        user_level = user_profile.get('level', 'beginner')
        user_interests = user_profile.get('interests', [])
        target_domain = user_profile.get('target_domain', '')
        
        recommendations = []
        
        for _, course in self.courses_df.iterrows():
            # Convert string representations to lists
            skill_tags = course['skill_tags'] if isinstance(course['skill_tags'], list) else eval(course['skill_tags'])
            
            # Calculate similarity scores
            skill_similarity = self.calculate_similarity(user_skills, skill_tags)
            level_score = self.calculate_level_match(user_level, course['level'])
            
            # Domain bonus
            domain_bonus = 1.5 if target_domain and target_domain.lower() in course['domain'].lower() else 1.0
            
            # Interest matching
            interest_match = any(interest.lower() in course['domain'].lower() for interest in user_interests)
            interest_bonus = 1.2 if interest_match else 1.0
            
            # Combined score
            combined_score = (skill_similarity * 0.6 + level_score * 0.4) * domain_bonus * interest_bonus
            fit_score = min(100, int(combined_score * 100))
            
            if fit_score > 15:  # Minimum threshold
                recommendations.append({
                    'title': course['title'],
                    'provider': course['provider'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'fit_score': fit_score,
                    'link': course['link'],
                    'domain': course['domain'],
                    'cost': course['cost'],
                    'skill_tags': skill_tags
                })
        
        # Sort by fit score
        recommendations.sort(key=lambda x: x['fit_score'], reverse=True)
        return recommendations[:top_k]
    
    def generate_rationale(self, course, user_profile):
        """Generate explanation for recommendation"""
        user_skills = user_profile.get('technical_skills', [])
        matching_skills = []
        
        for user_skill in user_skills:
            if any(user_skill.lower() in tag.lower() for tag in course['skill_tags']):
                matching_skills.append(user_skill)
        
        rationale_parts = []
        
        if matching_skills:
            rationale_parts.append(f"Builds on your skills in {', '.join(matching_skills[:2])}")
        else:
            rationale_parts.append("Great starting point for your interests")
        
        rationale_parts.append(f"Perfect for {course['level']} level learners")
        rationale_parts.append(f"Duration: {course['duration']}")
        rationale_parts.append(f"Cost: {course['cost'].title()}")
        
        return ". ".join(rationale_parts) + "."

def main():
    st.markdown('<div class="main-header">🎓 Smart Career AI Recommender</div>', unsafe_allow_html=True)
    
    # Initialize recommender
    if 'recommender' not in st.session_state:
        st.session_state.recommender = SimpleCareerRecommender()
    
    # Sample profiles for quick testing
    sample_profiles = {
        "CS Student": {
            "education": "Bachelor's", "major": "Computer Science",
            "technical_skills": ["python", "java", "html", "css"],
            "interests": ["web development", "software engineering"],
            "level": "beginner", "target_domain": "software development"
        },
        "Data Analyst": {
            "education": "Bachelor's", "major": "Statistics",
            "technical_skills": ["python", "excel", "sql", "statistics"],
            "interests": ["data science", "machine learning"],
            "level": "intermediate", "target_domain": "data science"
        },
        "Career Switcher": {
            "education": "Bachelor's", "major": "Business",
            "technical_skills": ["excel", "powerpoint"],
            "interests": ["technology", "project management"],
            "level": "beginner", "target_domain": "tech management"
        }
    }
    
    # Sidebar
    with st.sidebar:
        st.header("👤 Your Profile")
        
        # Quick profile selection
        selected_sample = st.selectbox("Try sample profiles:", 
                                     ["Custom Profile"] + list(sample_profiles.keys()))
        
        if selected_sample != "Custom Profile":
            sample_profile = sample_profiles[selected_sample]
            education = sample_profile["education"]
            major = sample_profile["major"]
            technical_skills = sample_profile["technical_skills"]
            interests = sample_profile["interests"]
            level = sample_profile["level"]
            target_domain = sample_profile["target_domain"]
        else:
            education = st.selectbox("Education Level", 
                                   ["High School", "Bachelor's", "Master's", "PhD", "Other"])
            major = st.text_input("Major/Degree", "Computer Science")
            
            tech_input = st.text_area("Technical Skills (comma separated)", 
                                    "python, javascript, html, css")
            technical_skills = [skill.strip() for skill in tech_input.split(',') if skill.strip()]
            
            interests_input = st.text_area("Interests (comma separated)", 
                                         "web development, data science")
            interests = [interest.strip() for interest in interests_input.split(',') if interest.strip()]
            
            target_domain = st.selectbox("Target Domain", 
                                       ["", "software development", "data science", "web development", 
                                        "cloud computing", "cybersecurity", "mobile development"])
            
            level = st.selectbox("Your Experience Level", ["beginner", "intermediate", "advanced"])
        
        if st.button("🎯 Get Recommendations", type="primary", use_container_width=True):
            user_profile = {
                'education': education,
                'major': major,
                'technical_skills': technical_skills,
                'interests': interests,
                'target_domain': target_domain,
                'level': level
            }
            st.session_state.user_profile = user_profile
    
    # Main content
    if hasattr(st.session_state, 'user_profile'):
        st.header("📚 Your Personalized Learning Path")
        
        with st.spinner("🤖 Finding your perfect courses..."):
            recommendations = st.session_state.recommender.recommend_courses(st.session_state.user_profile)
        
        if recommendations:
            for i, course in enumerate(recommendations, 1):
                rationale = st.session_state.recommender.generate_rationale(course, st.session_state.user_profile)
                
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{i}. {course['title']}</h4>
                    <p><strong>Provider:</strong> {course['provider']} | 
                       <strong>Fit Score:</strong> <span class="fit-score">{course['fit_score']}%</span> | 
                       <strong>Level:</strong> {course['level'].title()}</p>
                    <p><strong>Duration:</strong> {course['duration']} | 
                       <strong>Domain:</strong> {course['domain']} | 
                       <strong>Cost:</strong> {course['cost'].title()}</p>
                    <p><strong>Why this course?</strong> {rationale}</p>
                    <p><a href="{course['link']}" target="_blank">🔗 Learn More & Enroll</a></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show JSON output
            with st.expander("📋 JSON Output (for developers)"):
                output_data = {
                    "recommendations": recommendations,
                    "user_profile": st.session_state.user_profile,
                    "total_recommendations": len(recommendations)
                }
                st.json(output_data)
        else:
            st.warning("No suitable courses found. Try adjusting your skills or interests.")
            
        # Reset button
        if st.button("🔄 Start Over"):
            if hasattr(st.session_state, 'user_profile'):
                del st.session_state.user_profile
            st.rerun()
            
    else:
        # Welcome message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
            st.subheader("Welcome to Smart Career AI Recommender!")
            st.write("""
            **Discover your perfect learning path!**
            
            This AI-powered system will:
            - 📊 Analyze your skills and interests
            - 🎯 Recommend relevant courses and certifications  
            - 📅 Suggest a personalized learning timeline
            - 💡 Explain why each course is right for you
            
            **Get started by filling out your profile in the sidebar!**
            """)

if __name__ == "__main__":
    main()
