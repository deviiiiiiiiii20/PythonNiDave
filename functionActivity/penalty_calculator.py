
TOTAL_SYSTEM_PENALTY = 0.0


def calculate_compound_penalty(months_overdue, monthly_rate=50.0):
    if months_overdue == 0:
        return 0.0
    return monthly_rate + (calculate_compound_penalty(months_overdue - 1, monthly_rate) * 1.05)

def record_penalty(amount):
    global TOTAL_SYSTEM_PENALTY
    TOTAL_SYSTEM_PENALTY += amount
    return TOTAL_SYSTEM_PENALTY