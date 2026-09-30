def make_plan(subjects, hours):
    subjects = [s.strip() for s in subjects if s.strip()]
    if not subjects or hours <= 0:
        return "Please provide at least one subject and positive study hours."

    share = hours / len(subjects)
    lines = [f"Daily study plan ({hours:g} hours):"]

    for subject in subjects:
        lines.append(f"- {subject}: {share:.2f} hour(s)")

    lines.append("- Keep the final 10-15 minutes for revision/self-testing.")
    return "\n".join(lines)
