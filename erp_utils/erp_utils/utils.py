import frappe
import pyqrcode
import math


@frappe.whitelist()
def generate_qrcode(text):
    data = pyqrcode.create(text)

    return f'data:image/pngbase64,{data.png_as_base64_str(scale=5)}'

def convert_block(number, numberWords, teenWords, tensWords):
    if (number == 0):
        return ""
    elif (number == 10): 
        return "Ten"
    elif (number < 10): 
        return numberWords[math.floor(number)]
    elif (number < 20): 
        return teenWords[math.floor(number - 10)]
    else:
        tens = math.floor(number / 10)
        ones = math.floor(number % 10)
        if (ones > 0):
            tens_val = tensWords[tens] + " " if tens > 0 else ""
            return tens_val + numberWords[ones]
        else:
            return tensWords[tens]
        
def convert_group(number, scale, numberWords, teenWords, tensWords):
        if (number == 0):
            return ""
        elif (number < 100):
            return convert_block(math.floor(number), numberWords, teenWords, tensWords) + (" " + scale + " " if scale and number > 0 else "")
        else:
            hundreds = numberWords[math.floor(number / 100)] + " Hundred"
            remainder = convert_block(math.floor(number % 100), numberWords, teenWords, tensWords)
            separator = " " if remainder and remainder != "" else ""
            return f'{hundreds}{separator}{remainder}{" " + scale + " " if scale and number > 0 else ""}'

def convert(amount, mainCurrency, fractionCurrency, numberWords, teenWords, tensWords):
        if (amount == 0):
            return "Zero"

        result = ""

        parts = str(round(amount, 2)).split('.')
        wholeNumber = int(parts[0], 10)
        decimalPart = int(parts[1], 10) if len(parts) > 1 else 0

        billion = math.floor(amount / 1000000000)
        million = math.floor((amount % 1000000000) / 1000000)
        thousand = math.floor((amount % 1000000) / 1000)
        remainder = math.floor(amount % 1000)
        
        result += convert_group(billion, "Billion", numberWords, teenWords, tensWords)
        result += convert_group(million, "Million", numberWords, teenWords, tensWords)
        result += convert_group(thousand, "Thousand", numberWords, teenWords, tensWords)
        result += convert_group(remainder, "", numberWords, teenWords, tensWords) + " " + mainCurrency + " "


        # Handle the decimal part if present
        if (decimalPart > 0):
            result += "and " + convert_block(decimalPart, numberWords, teenWords, tensWords) + " " + fractionCurrency

        return str(result).strip()
        
@frappe.whitelist()
def generate_amount_to_words(paidAmount, currency):
    numberWords = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teenWords = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tensWords = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    fractionCurrency = ""
    mainCurrency = ""

    if (currency == "USD"):
        mainCurrency = "Dollars"
        fractionCurrency = "Cents"
    elif (currency == "EUR"):
        mainCurrency = "Euros"
        fractionCurrency = "Cents"
    elif (currency == "GBP"):
        mainCurrency = "Pounds"
        fractionCurrency = "Pences"
    else:
        mainCurrency = "Ghana Cedis"
        fractionCurrency = "Pesewas"
    
    return convert(paidAmount, mainCurrency, fractionCurrency, numberWords, teenWords, tensWords)
