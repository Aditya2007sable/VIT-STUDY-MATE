from modules.study_planner import make_plan

def test_plan_contains_subjects():
    result = make_plan(["Python", "Calculus"], 2)
    assert "Python" in result
    assert "Calculus" in result
