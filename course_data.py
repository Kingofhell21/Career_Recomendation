import pandas as pd
import json


def generate_course_catalog():
    courses = [
        # Programming & Software Development
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

        # Data Science & AI
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

        # Cloud & DevOps
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
        },

        # Business & Soft Skills
        {
            "title": "Project Management Professional",
            "provider": "PMI",
            "duration": "8 weeks",
            "prerequisites": ["project experience"],
            "skill_tags": ["project management", "leadership", "communication"],
            "level": "intermediate",
            "link": "https://pmi.org/pmp",
            "domain": "business",
            "cost": "paid"
        },
        {
            "title": "Effective Communication",
            "provider": "LinkedIn Learning",
            "duration": "3 weeks",
            "prerequisites": ["none"],
            "skill_tags": ["communication", "presentation", "soft skills"],
            "level": "beginner",
            "link": "https://linkedin.com/learning/communication",
            "domain": "soft skills",
            "cost": "paid"
        }
    ]

    # Add more courses to reach 25+
    additional_courses = [
        # Add 15+ more diverse courses here
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
        # ... add more courses as needed
    ]

    courses.extend(additional_courses)

    df = pd.DataFrame(courses)
    df.to_csv('courses.csv', index=False)
    print(f"Generated course catalog with {len(courses)} courses")

    return courses


if __name__ == "__main__":
    generate_course_catalog()