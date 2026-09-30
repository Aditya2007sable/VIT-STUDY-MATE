from database.database import get_connection

def show_performance():
    conn = get_connection()
    rows = conn.execute("""
        SELECT module, COUNT(*) AS attempts,
               AVG(percentage) AS average_percentage,
               MAX(percentage) AS best_percentage
        FROM quiz_results
        GROUP BY module
        ORDER BY average_percentage ASC
    """).fetchall()
    conn.close()

    print("\n--- Performance & Weak Topic Analyzer ---")

    if not rows:
        print("No quiz results yet. Attempt a quiz first.")
        return

    for row in rows:
        print(
            f"{row['module']}: attempts={row['attempts']}, "
            f"average={row['average_percentage']:.1f}%, "
            f"best={row['best_percentage']:.1f}%"
        )

    weakest = rows[0]
    print(f"\nRecommendation: Spend additional practice time on {weakest['module']}.")
