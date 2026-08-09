
import penalty_calculator as pc
from tuition_assessor import calculate_assessment

STUDENT_RECORDS = [
    {
        "name": "Juan Dela Cruz",
        "units": (3, 3, 4, 3, 2),
        "fees": {
            "rate_per_unit": 500.0,
            "lab_fee": 1200.0,
            "scholarship_discount": 0.15
        },
        "months_overdue": 3
    },
    {
        "name": "Maria Santos",
        "units": (3, 3, 3),
        "fees": {
            "rate_per_unit": 450.0
        },
        "months_overdue": 0
    }
]


def process_student(record):
    """Runs a single student through assessment + penalty calculation."""
    assessment = calculate_assessment(record["name"], *record["units"], **record["fees"])

    penalty = pc.calculate_compound_penalty(record["months_overdue"])
    pc.record_penalty(penalty)

    total_due = assessment["net_tuition"] + penalty

    return {
        "student": assessment["student"],
        "total_units": assessment["total_units"],
        "net_tuition": assessment["net_tuition"],
        "months_overdue": record["months_overdue"],
        "penalty": penalty,
        "total_due": total_due
    }


def print_billing_summary(results):
    """Prints a formatted billing summary report for all processed students."""
    width = 62
    print("=" * width)
    print("MCC STUDENT BILLING & ASSESSMENT SYSTEM".center(width))
    print("=" * width)

    for r in results:
        print(f"\nStudent Name       : {r['student']}")
        print(f"Total Units        : {r['total_units']}")
        print(f"Net Tuition         : PHP {r['net_tuition']:>12,.2f}")
        print(f"Months Overdue     : {r['months_overdue']}")
        print(f"Overdue Penalty     : PHP {r['penalty']:>12,.2f}")
        print("-" * width)
        print(f"TOTAL AMOUNT DUE    : PHP {r['total_due']:>12,.2f}")
        print("-" * width)

    print(f"\n{'TOTAL SYSTEM PENALTY COLLECTED (ALL STUDENTS)':<40}: PHP {pc.TOTAL_SYSTEM_PENALTY:>12,.2f}")
    print("=" * width)


def main():
    results = [process_student(record) for record in STUDENT_RECORDS]
    print_billing_summary(results)


if __name__ == "__main__":
    main()