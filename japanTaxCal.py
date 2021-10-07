import sys
# configurable
ANUAL_SALARY = 12345678
BONUS = 1234

# only if you use company benefit
monthly_rent = 1234


# please check https://taxsummaries.pwc.com/japan/individual/deductions 
# in Personal exemptions section
PERSONAL_EXEMPTION_NATIONAL = 480000 + 380000*2
PERSONAL_EXEMPTION_LOCAL = 430000 + 330000*2




# const data
ALLOWANCE_RATE = [
        {"LOWER" : 0, "UPPER": 1625000, "RATE": 1, "DEDUCTION": 0},
        {"LOWER" : 1625000, "UPPER": 1800000, "RATE": 0.4, "DEDUCTION": -100000},
        {"LOWER": 1800000, "UPPER": 3600000, "RATE": 0.3, "DEDUCTION": 80000},
        {"LOWER": 3600000, "UPPER": 6600000, "RATE": 0.2, "DEDUCTION": 440000},
        {"LOWER": 6600000, "UPPER": 8500000, "RATE": 0.1,  "DEDUCTION": 1100000},
        {"LOWER": 8500000, "UPPER": sys.maxsize, "RATE": 0, "DEDUCTION": 1950000}]


HEALTH_TAX_MONTHLY = {"RATE": 4.92/100, "CAP": 68597}
HEALTH_TAX_BONUS = {"RATE": 4.92/100, "CAP": 282776}

WELFARE_TAX_MONTHLY = {"RATE": 9.15/100, "CAP": 56730}
WELFARE_TAX_BONUS = {"RATE": 9.15/100, "CAP": 137250}

EMPLOYMENT_INSURANCE_RATE = 0.3/100

LOCAL_TAX_RATE = 0.1

TAX_RATE = [
        {"LOWER" : 0, "UPPER": 1950000, "RATE": 0.05, "DEDUCTION": 0},
        {"LOWER" : 1950000, "UPPER": 3300000, "RATE": 0.1, "DEDUCTION": 97500},
        {"LOWER": 3300000, "UPPER": 6950000, "RATE": 0.2, "DEDUCTION": 427500},
        {"LOWER": 6950000, "UPPER": 9000000, "RATE": 0.23, "DEDUCTION": 636000},
        {"LOWER": 9000000, "UPPER": 18000000, "RATE": 0.33,  "DEDUCTION": 1536000},
        {"LOWER": 18000000, "UPPER": 40000000, "RATE": 0.40, "DEDUCTION": 2796000},
        {"LOWER": 40000000, "UPPER": sys.maxsize, "RATE": 0.45, "DEDUCTION": 4796000}]

def calSocialTax(income, taxRate):
    tax = taxRate['CAP'] if income*taxRate['RATE'] > taxRate['CAP'] else income*taxRate['RATE']
    return tax

def getRate(income, taxRate):
    for rate in taxRate:
        if income >= rate["LOWER"] and income <= rate["UPPER"]:
            return rate;

def getAllowance(income):
    allowanceRate = getRate(income, ALLOWANCE_RATE)
    return income * allowanceRate["RATE"] + allowanceRate["DEDUCTION"]


def calTax(anual_salary, bonus):
    print(f'original salary: {anual_salary:,}, bonus: {bonus:,}, total: {(anual_salary + bonus):,}')
    
    total = anual_salary + bonus
    employment_insurance = total * EMPLOYMENT_INSURANCE_RATE
    bonus_percent = bonus/total
    salary_percent = anual_salary/total
    # welfare
    salary_welfare_monthly = calSocialTax(anual_salary/12, WELFARE_TAX_MONTHLY)
    bonus_welfare = calSocialTax(bonus, WELFARE_TAX_BONUS)

    salary_health_monthly = calSocialTax(anual_salary/12, HEALTH_TAX_MONTHLY)
    bonus_health = calSocialTax(bonus, HEALTH_TAX_BONUS)
    
    social_tax_salary = int(salary_welfare_monthly*12 + salary_health_monthly*12 + employment_insurance*salary_percent)
    social_tax_bonus = int(bonus_welfare + bonus_health + employment_insurance*bonus_percent)
    
    after_social_tax = total - social_tax_salary - social_tax_bonus
    after_allowance_deduction = after_social_tax - getAllowance(after_social_tax)

    #print("allowance: ", getAllowance(after_social_tax))
    
    # national tax
    taxable_national = after_allowance_deduction - PERSONAL_EXEMPTION_NATIONAL
    tax_range = getRate(taxable_national, TAX_RATE)
    #print(tax_range, " taxable_national", taxable_national)    
    tax_national = taxable_national * tax_range["RATE"] - tax_range["DEDUCTION"]
    tax_national = int(tax_national * 1.021)

    # local tax
    taxable_local = after_allowance_deduction - PERSONAL_EXEMPTION_LOCAL
    tax_local = int(taxable_local * LOCAL_TAX_RATE)

    total_tax = tax_national + tax_local + social_tax_salary + social_tax_bonus
    
    tax_salary = int(total_tax * salary_percent)
    tax_bonus = int(total_tax * bonus_percent)

    taxed_salary = anual_salary - tax_salary
    taxed_bonus = bonus - tax_bonus

    print(f'tax on basis salary = {tax_salary:,}, monthly={int(tax_salary/12):,}, bonus = {tax_bonus:,}, total = {total_tax:,}')
    print(f'after tax, basis salary = {taxed_salary:,}, monthly={int(taxed_salary/12):,}, bonus = {taxed_bonus:,}, total = {(taxed_bonus + taxed_salary):,}')
    print(f'tax rate in total {(tax_salary+ tax_bonus)/(ANUAL_SALARY + BONUS):,}')
    print('\n')
    return int(taxed_salary/12)

sa = calTax(ANUAL_SALARY, BONUS)

print(f'with monthly rent {monthly_rent}')
sa1 = calTax(ANUAL_SALARY-monthly_rent*12, BONUS)








