from src.agent.decision_agent import rank_insights

def test_agent_ranking():
    insights = [
        {"type": "anomaly", "value": 5},
        {"type": "cluster", "value": 200}
    ]

    ranked = rank_insights(insights)

    assert ranked[0]["priority"] == "high"