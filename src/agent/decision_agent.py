# def rank_insights(insights):
#     for ins in insights:

#         if ins.type == "anomaly":
#             if ins.value > 2:
#                 ins.priority = "high"
#                 ins.score = 10
#                 ins.action = "Investigate unusual transactions immediately"
#             else:
#                 ins.priority = "medium"
#                 ins.score = 6
#                 ins.action = "Monitor anomalies"

#         elif ins.type == "cluster":
#             ins.priority = "medium"
#             ins.score = 7
#             ins.action = "Target high-value customer segment"

#         elif ins.type == "trend":
#             if ins.value > 0.3:
#                 ins.priority = "high"
#                 ins.score = 9
#                 ins.action = "Analyze cause of sudden increase"
#             else:
#                 ins.priority = "low"
#                 ins.score = 5
#                 ins.action = "Track trend"

#     ranked = sorted(insights, key=lambda x: x.score, reverse=True)

#     return ranked[:5]





def rank_insights(insights):
    for ins in insights:

        if ins["type"] == "anomaly":
            if ins["value"] > 2:
                ins["priority"] = "high"
                ins["score"] = 10
                ins["action"] = "Investigate unusual transactions immediately"
            else:
                ins["priority"] = "medium"
                ins["score"] = 6
                ins["action"] = "Monitor anomalies"

        elif ins["type"] == "cluster":
            ins["priority"] = "medium"
            ins["score"] = 7
            ins["action"] = "Target high-value customer segment"

        elif ins["type"] == "trend":
            if ins["value"] > 0.3:
                ins["priority"] = "high"
                ins["score"] = 9
                ins["action"] = "Analyze cause of sudden increase"
            else:
                ins["priority"] = "low"
                ins["score"] = 5
                ins["action"] = "Track trend"

    ranked = sorted(
        insights,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:5]