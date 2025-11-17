# matching_engine_alternative.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Any


class AlternativeMatchingEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.courses_df = None
        self.tfidf_matrix = None
        self.feature_names = None

    def load_courses(self, csv_path='courses.csv'):
        """Load course catalog from CSV"""
        self.courses_df = pd.read_csv(csv_path)

        # Convert list-like strings to actual lists
        for col in ['prerequisites', 'skill_tags']:
            self.courses_df[col] = self.courses_df[col].apply(
                lambda x: [item.strip() for item in x.strip('[]').replace("'", "").split(',')]
                if isinstance(x, str) else []
            )

        # Create combined text for TF-IDF
        self.courses_df['combined_text'] = self.courses_df.apply(
            lambda row: f"{row['title']} {row['provider']} {' '.join(row['skill_tags'])} {row['domain']}",
            axis=1
        )

        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.courses_df['combined_text'])
        self.feature_names = self.vectorizer.get_feature_names_out()

    def create_user_profile_text(self, user_profile):
        """Create combined text representation of user profile"""
        education = user_profile.get('education', '')
        technical_skills = ' '.join(user_profile.get('technical_skills', []))
        soft_skills = ' '.join(user_profile.get('soft_skills', []))
        interests = ' '.join(user_profile.get('interests', []))
        target_domain = user_profile.get('target_domain', '')
        career_goals = user_profile.get('career_goals', '')
        major = user_profile.get('major', '')

        return f"{education} {major} {technical_skills} {soft_skills} {interests} {target_domain} {career_goals}"

    def calculate_level_match(self, user_level, course_level):
        """Calculate level compatibility score"""
        level_mapping = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        user_lvl = level_mapping.get(user_level.lower(), 0)
        course_lvl = level_mapping.get(course_level.lower(), 0)

        # Penalize recommending advanced courses to beginners
        if course_lvl - user_lvl > 1:
            return 0.3  # Strong penalty
        elif course_lvl - user_lvl == 1:
            return 0.7  # Mild penalty
        else:
            return 1.0  # Good match

    def calculate_prerequisite_match(self, user_skills, course_prerequisites):
        """Calculate how well user meets course prerequisites"""
        if not course_prerequisites or course_prerequisites == ['none']:
            return 1.0

        user_skills_lower = [skill.lower() for skill in user_skills]
        prereq_met = 0

        for prereq in course_prerequisites:
            prereq_lower = prereq.lower().strip()
            # Check if user has this skill or a similar one
            if any(prereq_lower in skill or skill in prereq_lower for skill in user_skills_lower):
                prereq_met += 1
            elif any(self.skill_similarity(prereq_lower, skill) > 0.7 for skill in user_skills_lower):
                prereq_met += 1

        return prereq_met / len(course_prerequisites) if course_prerequisites else 1.0

    def skill_similarity(self, skill1, skill2):
        """Calculate similarity between two skills"""
        skill1 = skill1.lower()
        skill2 = skill2.lower()

        if skill1 == skill2:
            return 1.0

        # Check for partial matches
        if skill1 in skill2 or skill2 in skill1:
            return 0.8

        # Check for common words
        words1 = set(skill1.split())
        words2 = set(skill2.split())
        common_words = words1.intersection(words2)

        if common_words:
            return len(common_words) / max(len(words1), len(words2))

        return 0.0

    def recommend_courses(self, user_profile, top_k=10):
        """Generate course recommendations for user profile"""
        if self.courses_df is None:
            self.load_courses()

        user_text = self.create_user_profile_text(user_profile)
        user_vector = self.vectorizer.transform([user_text])

        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)[0]

        recommendations = []

        for idx, course in self.courses_df.iterrows():
            # Calculate various matching scores
            similarity_score = similarities[idx]
            level_score = self.calculate_level_match(
                user_profile.get('level', 'beginner'),
                course['level']
            )
            prerequisite_score = self.calculate_prerequisite_match(
                user_profile.get('technical_skills', []),
                course['prerequisites']
            )

            # Domain matching bonus
            domain_bonus = 1.2 if (user_profile.get('target_domain') and
                                   user_profile.get('target_domain').lower() in course['domain'].lower()) else 1.0

            # Combined score (weighted average)
            combined_score = (
                                     0.5 * similarity_score +
                                     0.25 * level_score +
                                     0.25 * prerequisite_score
                             ) * domain_bonus

            # Convert to 0-100 scale
            fit_score = min(100, int(combined_score * 100))

            if fit_score > 20:  # Minimum threshold
                recommendations.append({
                    'title': course['title'],
                    'provider': course['provider'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'fit_score': fit_score,
                    'link': course['link'],
                    'domain': course['domain'],
                    'cost': course['cost'],
                    'prerequisites': course['prerequisites'],
                    'skill_tags': course['skill_tags'],
                    'similarity_score': similarity_score,
                    'level_score': level_score,
                    'prerequisite_score': prerequisite_score
                })

        # Sort by fit score
        recommendations.sort(key=lambda x: x['fit_score'], reverse=True)

        return recommendations[:top_k]

    def generate_learning_timeline(self, recommendations, user_profile):
        """Generate short-term and long-term learning plan"""
        short_term = []
        long_term = []

        user_level = user_profile.get('level', 'beginner')
        user_skills = set(skill.lower() for skill in user_profile.get('technical_skills', []))

        for course in recommendations:
            course_level = course['level']
            prerequisites_met = all(
                any(self.skill_similarity(prereq, user_skill) > 0.7
                    for user_skill in user_skills)
                for prereq in course['prerequisites'] if prereq != 'none'
            )

            # Short-term: beginner level or prerequisites fully met
            if (course_level == 'beginner' or
                    (prerequisites_met and course_level in ['beginner', 'intermediate'])):
                short_term.append(course)
            else:
                long_term.append(course)

        return {
            'short_term': short_term[:3],  # Next 1-3 months
            'long_term': long_term[:5]  # Next 3-12 months
        }

    def generate_rationale(self, course, user_profile):
        """Generate explanation for why course is recommended"""
        user_skills = user_profile.get('technical_skills', [])
        course_skills = course['skill_tags']

        # Find matching skills
        matching_skills = []
        for user_skill in user_skills:
            for course_skill in course_skills:
                if self.skill_similarity(user_skill, course_skill) > 0.6:
                    matching_skills.append(course_skill)

        # Find missing prerequisites
        missing_prereqs = []
        user_skills_lower = [skill.lower() for skill in user_skills]
        for prereq in course['prerequisites']:
            if prereq != 'none' and not any(
                    self.skill_similarity(prereq, user_skill) > 0.7 for user_skill in user_skills_lower):
                missing_prereqs.append(prereq)

        rationale_parts = []

        if matching_skills:
            rationale_parts.append(f"Matches your skills in {', '.join(set(matching_skills[:2]))}")

        if missing_prereqs:
            rationale_parts.append(f"Will help you learn {', '.join(missing_prereqs[:2])}")
        else:
            rationale_parts.append("Builds directly on your current skills")

        rationale_parts.append(f"Level: {course['level'].title()}")
        rationale_parts.append(f"Duration: {course['duration']}")
        rationale_parts.append(f"Cost: {course['cost'].title()}")

        return ". ".join(rationale_parts) + "."