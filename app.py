# app_simplified.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Any


class AllInOneCareerRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.courses_df = None
        self.tfidf_matrix = None

    def generate_sample_courses(self):
        """Generate course catalog directly (no separate CSV needed)"""
        courses = [
            {
                "title": "Python for Beginners",
                "provider": "Coursera",
                "duration": "6 weeks",
                "prerequisites": ["none"],
                "skill_tags": ["python", "programming", "basic coding"],
                "level": "beginner",
                "link": "https://coursera.org/learn/python-basics",
                "domain": "software development",
                "cost": "free"
            },
            {
                "title": "Advanced Python Programming",
                "provider": "edX",
                "duration": "8 weeks",
                "prerequisites": ["python", "basic programming"],
                "skill_tags": ["python", "OOP", "data structures", "algorithms"],
                "level": "intermediate",
                "link": "https://edx.org/learn/advanced-python",
                "domain": "software development",
                "cost": "paid"
            },
            {
                "title": "Data Science Fundamentals",
                "provider": "Coursera",
                "duration": "10 weeks",
                "prerequisites": ["python", "statistics"],
                "skill_tags": ["data science", "python", "pandas", "numpy", "data analysis"],
                "level": "beginner",
                "link": "https://coursera.org/learn/data-science",
                "domain": "data science",
                "cost": "free"
            },
            {
                "title": "Machine Learning Specialization",
                "provider": "Coursera",
                "duration": "16 weeks",
                "prerequisites": ["python", "linear algebra", "statistics"],
                "skill_tags": ["machine learning", "scikit-learn", "tensorflow", "deep learning"],
                "level": "intermediate",
                "link": "https://coursera.org/learn/machine-learning",
                "domain": "artificial intelligence",
                "cost": "paid"
            },
            {
                "title": "AWS Cloud Practitioner",
                "provider": "AWS Training",
                "duration": "4 weeks",
                "prerequisites": ["none"],
                "skill_tags": ["aws", "cloud computing", "devops"],
                "level": "beginner",
                "link": "https://aws.amazon.com/training/learn-about/cloud-practitioner",
                "domain": "cloud computing",
                "cost": "free"
            }
        ]

        # Add more courses to reach 25+
        additional_courses = [
            {
                "title": "JavaScript Modern Development",
                "provider": "FreeCodeCamp",
                "duration": "10 weeks",
                "prerequisites": ["html", "css"],
                "skill_tags": ["javascript", "es6", "frontend", "web development"],
                "level": "beginner",
                "link": "https://freecodecamp.org/javascript",
                "domain": "web development",
                "cost": "free"
            },
            {
                "title": "React Native Mobile Development",
                "provider": "Udemy",
                "duration": "8 weeks",
                "prerequisites": ["javascript", "react"],
                "skill_tags": ["react native", "mobile", "javascript", "ios", "android"],
                "level": "intermediate",
                "link": "https://udemy.com/react-native",
                "domain": "mobile development",
                "cost": "paid"
            },
            {
                "title": "Full Stack Web Development",
                "provider": "Udacity",
                "duration": "12 weeks",
                "prerequisites": ["javascript", "html", "css"],
                "skill_tags": ["javascript", "react", "node.js", "mongodb", "web development"],
                "level": "intermediate",
                "link": "https://udacity.com/full-stack",
                "domain": "web development",
                "cost": "paid"
            },
            {
                "title": "Deep Learning Advanced",
                "provider": "edX",
                "duration": "12 weeks",
                "prerequisites": ["machine learning", "python", "calculus"],
                "skill_tags": ["deep learning", "neural networks", "pytorch", "computer vision"],
                "level": "advanced",
                "link": "https://edx.org/learn/deep-learning",
                "domain": "artificial intelligence",
                "cost": "paid"
            },
            {
                "title": "Docker and Kubernetes",
                "provider": "Udemy",
                "duration": "6 weeks",
                "prerequisites": ["linux", "basic networking"],
                "skill_tags": ["docker", "kubernetes", "containers", "devops"],
                "level": "intermediate",
                "link": "https://udemy.com/docker-kubernetes",
                "domain": "devops",
                "cost": "paid"
            }
        ]

        courses.extend(additional_courses)
        self.courses_df = pd.DataFrame(courses)

        # Prepare data for matching
        self.courses_df['combined_text'] = self.courses_df.apply(
            lambda row: f"{row['title']} {row['provider']} {' '.join(row['skill_tags'])} {row['domain']}",
            axis=1
        )

        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.courses_df['combined_text'])

    def calculate_level_match(self, user_level, course_level):
        level_mapping = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        user_lvl = level_mapping.get(user_level.lower(), 0)
        course_lvl = level_mapping.get(course_level.lower(), 0)

        if course_lvl - user_lvl > 1:
            return 0.3
        elif course_lvl - user_lvl == 1:
            return 0.7
        else:
            return 1.0

    def recommend_courses(self, user_profile, top_k=10):
        if self.courses_df is None:
            self.generate_sample_courses()

        # Create user profile text
        user_text = f"{user_profile['education']} {user_profile['major']} {' '.join(user_profile['technical_skills'])} {' '.join(user_profile['soft_skills'])} {' '.join(user_profile['interests'])} {user_profile.get('target_domain', '')} {user_profile.get('career_goals', '')}"

        user_vector = self.vectorizer.transform([user_text])
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)[0]

        recommendations = []

        for idx, course in self.courses_df.iterrows():
            level_score = self.calculate_level_match(
                user_profile.get('level', 'beginner'),
                course['level']
            )

            # Combined score
            combined_score = (0.7 * similarities[idx] + 0.3 * level_score)
            fit_score = min(100, int(combined_score * 100))

            if fit_score > 20:
                recommendations.append({
                    'title': course['title'],
                    'provider': course['provider'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'fit_score': fit_score,
                    'link': course['link'],
                    'domain': course['domain'],
                    'cost': course['cost'],
                    'skill_tags': course['skill_tags']
                })

        recommendations.sort(key=lambda x: x['fit_score'], reverse=True)
        return recommendations[:top_k]

    def generate_rationale(self, course, user_profile):
        user_skills = user_profile.get('technical_skills', [])
        matching_skills = [skill for skill in user_skills if any(skill in tag for tag in course['skill_tags'])]

        if matching_skills:
            rationale = f"Matches your skills in {', '.join(matching_skills[:2])}. "
        else:
            rationale = "Aligns with your career interests. "

        rationale += f"Level: {course['level'].title()}. Duration: {course['duration']}. Cost: {course['cost'].title()}."
        return rationale


def main():
    st.set_page_config(
        page_title="Smart Career AI Recommender",
        page_icon="🎓",
        layout="wide"
    )

    st.markdown("""
    <style>
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎓 Smart Career AI Recommender")

    # Initialize recommender
    if 'recommender' not in st.session_state:
        st.session_state.recommender = AllInOneCareerRecommender()

    # Sidebar - User Input
    st.sidebar.header("👤 Your Profile")

    education = st.sidebar.selectbox(
        "Education Level",
        ["High School", "Associate's", "Bachelor's", "Master's", "PhD"]
    )

    major = st.sidebar.text_input("Major/Degree", "Computer Science")

    technical_skills = st.sidebar.text_area(
        "Technical Skills (comma-separated)",
        "python, javascript, html"
    ).split(',')
    technical_skills = [skill.strip() for skill in technical_skills if skill.strip()]

    soft_skills = st.sidebar.text_area(
        "Soft Skills (comma-separated)",
        "communication, problem solving"
    ).split(',')
    soft_skills = [skill.strip() for skill in soft_skills if skill.strip()]

    interests = st.sidebar.text_area(
        "Interests (comma-separated)",
        "web development, data science"
    ).split(',')
    interests = [interest.strip() for interest in interests if interest.strip()]

    target_domain = st.sidebar.selectbox(
        "Target Domain",
        ["", "software development", "data science", "web development", "cloud computing"]
    )

    level = st.sidebar.selectbox("Your Level", ["beginner", "intermediate", "advanced"])

    # Generate recommendations
    if st.sidebar.button("🎯 Get Recommendations", type="primary"):
        user_profile = {
            'education': education,
            'major': major,
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'interests': interests,
            'target_domain': target_domain,
            'level': level
        }

        with st.spinner("🤖 Finding your perfect learning path..."):
            recommendations = st.session_state.recommender.recommend_courses(user_profile)

        # Display results
        st.header("📚 Your Personalized Learning Path")

        for i, course in enumerate(recommendations, 1):
            rationale = st.session_state.recommender.generate_rationale(course, user_profile)

            st.markdown(f"""
            <div class="recommendation-card">
                <h3>{i}. {course['title']}</h3>
                <p><strong>Provider:</strong> {course['provider']} | 
                   <strong>Fit Score:</strong> {course['fit_score']}% | 
                   <strong>Level:</strong> {course['level'].title()}</p>
                <p><strong>Duration:</strong> {course['duration']} | 
                   <strong>Domain:</strong> {course['domain']} | 
                   <strong>Cost:</strong> {course['cost'].title()}</p>
                <p><strong>Why this course?</strong> {rationale}</p>
                <p><a href="{course['link']}" target="_blank">🔗 Learn More</a></p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()