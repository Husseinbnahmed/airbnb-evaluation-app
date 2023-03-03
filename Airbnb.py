#required libraries
import numpy as np
import pandas as pd
# import numpy_financial as npf

import numpy_financial as npf
import matplotlib.pyplot as plt

def future_rents(Avg_daily_rate, Occupancy_rate, Ann_rent_growth):
    
    """
    Calculates the annual rents for the next 10 years. 
    Args:
    Avg_daily_rate -----> The average daily rate you will charge on Airbnb
    Occupancy_rate -----> The rate of occupancy ex. an occ. rate of 0.70 means 70% of a year is occupied by renters. 
    Annual_rent_growth --> Ann. rent growth is the annual growth in rent. 
    """
    future_rents = np.zeros(10) 
    future_rents[0] = (Avg_daily_rate * 365) * Occupancy_rate
    for i in range(len(future_rents)):
        if i > 0:
            future_rents[i] = future_rents[i-1] * (1+Ann_rent_growth)
    return future_rents

def ann_payment(interest_rate, purchase_price, down_payment, pmi=0):
    """
    Calculates the annual mortgage payment which includes interest and principal
    
    Args:
    interest_rate ---> The interest rate charged by the bank
    purchase price --> agreed upon price
    down payment --> your down payment
    pmi --> mortgage insurance, only paid when down payment is less than 20% 
    """
    
    # Calculate the loan amount using the purchase price and down payment
    loan_amount = purchase_price * (1-down_payment)
    
    # Calculate monthly mortgage payment
    pmt = npf.pmt(interest_rate/12, nper=12*30, pv = loan_amount)
    
    # Initialize the annual mortgage payment array
    ann_pmt = np.zeros(10)
    
    # Check if down payment is greater than 20%
    if down_payment >=0.20:
        # If so, multiply monthly mortgage payment by 12
        for i in range(len(ann_pmt)):
            ann_pmt[i] = pmt * 12
    else:
        # If not, subtract the mortgage insurance (pmi) from the monthly mortgage payment
        # Then multiply by 12
        for i in range(len(ann_pmt)):
            ann_pmt[i] = (pmt+(pmi*-1)) * 12
            
    return ann_pmt 

def home_specific_costs(purchase_price, monthly_hoa, ann_repair_pct, property_tax_rate, 
                        monthly_utilities, monthly_internet, home_insurance):
    
    """
    Calculates the annual fixed costs related to a property such as the tax rate, 
    hoa fees, utilities and monthly internet fees. 
    """
    
    # Calculate the annual HOA fees
    hoa_array = np.full(10, monthly_hoa*12)
    
    # Calculate the annual repair costs
    ann_repair_amount = ann_repair_pct * purchase_price
    repairs_array = np.full(10, ann_repair_amount)
    
    # Calculate the annual property tax costs
    property_tax_amount = purchase_price * property_tax_rate
    tax_array = np.full(10, property_tax_amount)
    
    # Calculate the annual cost of monthly utilities
    monthly_utilities_array = np.full(10, monthly_utilities*12)
    
    # Calculate the annual cost of monthly internet
    monthly_internet_array = np.full(10, monthly_internet *12)
    
    # Calculate the annual cost of home insurance
    home_insurance_array = np.full(10, home_insurance * 12)
    
    # Calculate the total annual home specific costs
    tot_home_specific_costs = (hoa_array + repairs_array + tax_array + monthly_internet_array  + home_insurance_array) * -1 
    
    # Return the total annual home specific costs
    return tot_home_specific_costs

def airbnb_specific_costs(hosting_fee_pct, credit_card_processing_pct, prop_management_fee_pct, Avg_daily_rate, 
                         Occupancy_rate, Ann_rent_growth):
    """
    Calculates the airbnb specific annual costs such as hosting fee, credit card processing and property mgt fees. 
    Property management fees in this function can have two meanings, it can be the amount paid to a third party company or
    can represent expenses of ongoing costs such as toiltery, cleaning supplies, paper towels, batteries or coffee pods. 
    
    Note that those expenses are revenue driven. 
    """
    # Calculate the future rents
    rents = future_rents(Avg_daily_rate, Occupancy_rate, Ann_rent_growth)
    
    # Calculate the hosting fee as a % of the rent
    hosting_fee_array = rents * hosting_fee_pct
    
    # Calculate the credit card processing fee as a % of the rent
    credit_card_processing_array = rents * credit_card_processing_pct 
    
    # Calculate the property management fee as a % of the rent
    prop_management_fee_array = rents * prop_management_fee_pct
    
    # Calculate the total airbnb costs as the sum of the fees
    total_airbnb_costs = (hosting_fee_array + credit_card_processing_array + prop_management_fee_array) * -1
    
    # Return the total costs
    return total_airbnb_costs

#calculate the price of the home at terminal value
def property_price_at_ty(purchase_price, growth_rate):
    home_value_at_terminal_year = purchase_price * (1 + growth_rate ) ** 10
    return home_value_at_terminal_year
    
# Calculate the principal
def remaining_loan_at_ty(interest_rate, purchase_price, down_payment):
    
    # Calculate the home loan amount by subtracting the down payment from the purchase price
    home_loan = purchase_price * (1-down_payment)
    
    # Calculate the cumulative principal paid over 10 years
    cum_principal = 0
    for i in range(121):
        ppmt = npf.ppmt(interest_rate/12, i, 360, home_loan) #calculates principal payment
        cum_principal+=ppmt
    
    # Calculate the remaining loan in 10 years by adding the cumulative principal to the home loan which is in negative
    remaining_loan_in_10_years = home_loan + cum_principal
    
    return remaining_loan_in_10_years
        

# calculate the initial outlay
def initial_investment(purchase_price, down_payment, closing_cost_pct, start_up_costs):
    """
    Calculates the initial investment which includes the down payment, closing costs and start up costs such as furniture
    and other things needed to run an airbnb
    """
    
    dwn_pmt = down_payment * purchase_price
    closing_cost = closing_cost_pct * purchase_price
    initial_investment = closing_cost + dwn_pmt + start_up_costs
    
    return initial_investment

def npv(purchase_price, growth_rate, interest_rate, down_payment,
                     Avg_daily_rate, Occupancy_rate, Ann_rent_growth, monthly_hoa, ann_repair_pct,
                     property_tax_rate, monthly_utilities, monthly_internet,
                     home_insurance,  hosting_fee_pct, credit_card_processing_pct, 
                     prop_management_fee_pct, discount_rate, closing_cost_pct, start_up_costs, pmi=0):
    
    """
    Calculates the NPV of an investment
    """
    
    #profit on sale
    profit_on_sale = property_price_at_ty(purchase_price, growth_rate) - remaining_loan_at_ty(interest_rate, purchase_price, down_payment)
    # rents 
    rents = future_rents(Avg_daily_rate, Occupancy_rate, Ann_rent_growth)
    #expenses
    payments = ann_payment(interest_rate, purchase_price, down_payment, pmi=0)
    fixed_cost = home_specific_costs(purchase_price, monthly_hoa, ann_repair_pct, property_tax_rate,
                                     monthly_utilities, monthly_internet, home_insurance)
    var_cost = airbnb_specific_costs(hosting_fee_pct, credit_card_processing_pct,
                                     prop_management_fee_pct, Avg_daily_rate, Occupancy_rate, Ann_rent_growth)
    tot_exp = payments + fixed_cost + var_cost
    #cashflows
    cf = rents + tot_exp
    #terminal casfhlows
    cf[9] = cf[9] + profit_on_sale
    #pv 
    pv = round(npf.npv(discount_rate, cf),2)
    initial_outlay =initial_investment(purchase_price, down_payment, closing_cost_pct, start_up_costs)
    npv = pv - initial_outlay
    ## ALL Cashflows laid out
    all_cf = np.zeros(11)
    all_cf[0] = initial_outlay * -1
    all_cf[1:] = cf
    
    #IRR
    irr = round(npf.irr(all_cf),2)
    return [rents, profit_on_sale, payments, fixed_cost, var_cost, tot_exp, cf, pv, initial_outlay, npv, all_cf, irr]
