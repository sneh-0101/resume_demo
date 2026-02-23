
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from flask_app.ai_engine.core import InterviewPrep, SkillRecommender

def test_interview_prep():
    print("\n--- Testing Interview Prep ---")
    skills = ["python", "docker", "unknown_skill"]
    print(f"Input skills: {skills}")
    
    questions = InterviewPrep.generate_questions(skills)
    
    if questions:
        print(f"[OK] Generated {len(questions)} questions:")
        for q in questions:
            print(f"  - {q}")
    else:
        print("[FAIL] No questions generated")

def test_skill_recommender():
    print("\n--- Testing Skill Recommender ---")
    skills = ["python", "react", "unknown_skill"]
    print(f"Input skills: {skills}")
    
    resources = SkillRecommender.get_resources(skills)
    
    if resources:
        print(f"[OK] Generated {len(resources)} resources:")
        for r in resources:
            print(f"  - {r['skill']}: {r['name']} ({r['url']})")
    else:
        print("[FAIL] No resources generated")

if __name__ == "__main__":
    try:
        test_interview_prep()
        test_skill_recommender()
        print("\n[OK] Verification Script Completed Successfully")
    except Exception as e:
        print(f"\n[FAIL] Error during verification: {e}")
