# backend_alternative.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from matching_engine import AlternativeMatchingEngine

app = FastAPI(title="Smart Career AI Recommender")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class UserProfile(BaseModel):
    education: str
    major: str
    technical_skills: List[str]
    soft_skills: List[str]
    interests: List[str]
    target_domain: Optional[str] = None
    career_goals: Optional[str] = None
    level: Optional[str] = "beginner"
    preferred_duration: Optional[str] = None


class CourseRecommendation(BaseModel):
    title: str
    provider: str
    duration: str
    level: str
    fit_score: int
    link: str
    domain: str
    cost: str
    rationale: str


class RecommendationResponse(BaseModel):
    recommendations: List[CourseRecommendation]
    timeline: Dict[str, List[CourseRecommendation]]
    user_profile: Dict[str, Any]


# Initialize matching engine
matching_engine = AlternativeMatchingEngine()


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(user_profile: UserProfile):
    try:
        # Convert to dict
        profile_dict = user_profile.dict()

        # Get recommendations
        recommendations = matching_engine.recommend_courses(profile_dict)

        # Generate timeline
        timeline_data = matching_engine.generate_learning_timeline(recommendations, profile_dict)

        # Add rationales
        final_recommendations = []
        for course in recommendations:
            rationale = matching_engine.generate_rationale(course, profile_dict)
            course_recommendation = CourseRecommendation(
                **course,
                rationale=rationale
            )
            final_recommendations.append(course_recommendation)

        # Prepare timeline with rationales
        timeline_with_rationales = {}
        for period, courses in timeline_data.items():
            timeline_courses = []
            for course in courses:
                rationale = matching_engine.generate_rationale(course, profile_dict)
                timeline_courses.append(CourseRecommendation(
                    **course,
                    rationale=rationale
                ))
            timeline_with_rationales[period] = timeline_courses

        return RecommendationResponse(
            recommendations=final_recommendations,
            timeline=timeline_with_rationales,
            user_profile=profile_dict
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Smart Career AI Recommender API"}


@app.get("/courses")
async def get_courses():
    try:
        matching_engine.load_courses()
        courses = matching_engine.courses_df.to_dict('records')
        return {"courses": courses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading courses: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)