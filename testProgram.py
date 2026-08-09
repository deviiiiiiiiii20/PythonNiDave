def checkTotalBill():
    totalBill = input("Enter total bill: ")
    tipPercent = input("Enter tip percent: ")
    nPeople = input("Enter number of people: ")

    totalBill = float(totalBill)
    tipPercent = float(tipPercent)
    nPeople = int(nPeople)

    sumTip = totalBill * (tipPercent/100)
    superTotal = totalBill + sumTip
    perPerson = superTotal / nPeople

    print(f"Your total bill is {superTotal}")
    print(f"Each person pays {perPerson}")

    if perPerson > 50:
        print("Sorry wala akong pang bayad")
    else:
        print("sige g")

checkTotalBill()

