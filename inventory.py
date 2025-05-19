import json
import time
from fpdf import FPDF

# Load inventory
with open("Record.json", "r") as fd:
    record = json.load(fd)

# Display menu
print("--------------------MENU---------------------")
for key in record:
    print(key, record[key]["Name"], "Rs.", record[key]["Price"], "Qty:", record[key]["Qn"])
print("---------------------------------------------\n")

# User info
ui_name = input("Enter your name    : ")
ui_mail = input("Enter Mail ID      : ")
ui_ph = input("Enter Phone No     : ")

# Initialize total and sale list
total_amount = 0
sale_entries = []
purchased_items = []

while True:
    ui_pr = input("\nEnter product ID (or type 'done' to finish): ")
    if ui_pr.lower() == "done":
        break
    if ui_pr not in record:
        print("Invalid product ID!")
        continue

    ui_qn = int(input("Enter Quantity     : "))
    available_qn = record[ui_pr]["Qn"]

    if available_qn == 0:
        print("Sorry, this product is out of stock.")
        continue

    if ui_qn <= available_qn:
        billing = ui_qn * record[ui_pr]["Price"]
        record[ui_pr]["Qn"] -= ui_qn
        purchased_qn = ui_qn
    else:
        print(f"Only {available_qn} units available.")
        ch = input("Press Y to buy all available stock: ")
        if ch.lower() == "y":
            billing = available_qn * record[ui_pr]["Price"]
            purchased_qn = available_qn
            record[ui_pr]["Qn"] = 0
        else:
            continue

    total_amount += billing
    sale_entries.append(f"{ui_name},{ui_mail},{ui_ph},{ui_pr},{record[ui_pr]['Name']},{purchased_qn},{record[ui_pr]['Price']},{billing},{time.ctime()}\n")
    purchased_items.append((record[ui_pr]["Name"], purchased_qn, record[ui_pr]["Price"], billing))

# Apply 10% discount
discount = 0
if total_amount >= 5000:
    discount = total_amount * 0.10
    total_amount -= discount

# Save updated inventory
with open("Record.json", "w") as fd:
    json.dump(record, fd)

# Save transaction
with open("Sales.txt", "a") as fd:
    for entry in sale_entries:
        fd.write(entry)

# Generate PDF receipt
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Billing Receipt", ln=1, align="C")

pdf.set_font("Arial", "", 12)
pdf.cell(200, 10, f"Name: {ui_name}", ln=1)
pdf.cell(200, 10, f"Email: {ui_mail}", ln=1)
pdf.cell(200, 10, f"Phone: {ui_ph}", ln=1)
pdf.cell(200, 10, f"Date: {time.ctime()}", ln=1)
pdf.ln(10)

pdf.set_font("Arial", "B", 12)
pdf.cell(60, 10, "Product", 1)
pdf.cell(30, 10, "Qty", 1)
pdf.cell(40, 10, "Price", 1)
pdf.cell(40, 10, "Total", 1)
pdf.ln()

pdf.set_font("Arial", "", 12)
for name, qty, price, bill in purchased_items:
    pdf.cell(60, 10, name, 1)
    pdf.cell(30, 10, str(qty), 1)
    pdf.cell(40, 10, f"Rs. {price}", 1)
    pdf.cell(40, 10, f"Rs. {bill}", 1)
    pdf.ln()

pdf.ln(5)
pdf.cell(200, 10, f"Discount Applied: Rs. {discount:.2f}", ln=1)
pdf.cell(200, 10, f"Total Amount Payable: Rs. {total_amount:.2f}", ln=1)

pdf.output("receipt.pdf")

print("\n---------------------------------------------")
print("  Thanks for your order, Inventory Updated!  ")
print("  PDF Receipt saved as 'receipt.pdf'         ")
print("---------------------------------------------")
