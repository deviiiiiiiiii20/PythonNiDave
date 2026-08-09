
def calculate_assessment(student_name, *subject_units, **fee_options):

    rate_per_unit = fee_options.get("rate_per_unit", 450.00)
    lab_fee = fee_options.get("lab_fee", 0.00)
    scholarship_discount = fee_options.get("scholarship_discount", 0.00)

    total_units = sum(subject_units)
    gross_tuition = total_units * rate_per_unit
    discounted_tuition = gross_tuition * (1 - scholarship_discount)
    net_tuition = discounted_tuition + lab_fee

    return {
        "student": student_name,
        "total_units": total_units,
        "net_tuition": net_tuition
    }