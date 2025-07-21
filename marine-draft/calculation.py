def calculate_draft_summary(draft_points, density=None):
    mean_draft = sum(draft_points) / len(draft_points)
    return {
        "mean_draft": round(mean_draft, 3)
    }
