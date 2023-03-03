# importing libraries
import numpy as np
import pandas as pd
import Airbnb as bnb
import streamlit as st

st.set_page_config(layout="wide")

# set the title of the application
st.title("Short Term Rental Evaluation App 🏠")

with st.sidebar:
    st.markdown("# Income Assumptions")
    Avg_daily_rate = st.number_input("💲Average daily rate ($)", value=450, step=1, help="This is the amount you will charge per night on average in a given year ex. $450 per night")
    Occupancy_rate = st.slider(label = "🏨 Occupancy rate (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0, help="Occupancy rate refers to the percentage of nights that are occupied by guests. In other words, it represents the utilization rate of a property at a given year")/100
    Ann_rent_growth = st.number_input("📈 Annual rent growth (%)", value=2.0, min_value=0.0, max_value=100.0, step=1.0, help= "By how much will your rent grow each year? ex. 2%")/100
    growth_rate = st.number_input("📊 Annual property appreciation rate (%)", value=2.0, step=1.0, help="By how much will your home appreciate in value annually? ex. 2%" )/100

    st.markdown("# Mortgage Assumptions")
    interest_rate = st.number_input("🏦 Interest rate (%)", value=5.25, step=0.01, help="What will the interest rate be on your mortgage?")/100
    purchase_price = st.number_input("🏡 Property purchase price ($)", value=320000.0, step=1.0, help= "How much will you pay for the home?")
    down_payment = st.slider("💰 Down payment (% of home price)", min_value = 0.0, max_value= 100.0, value=20.0, step=1.0, help= 'How much will you put down on this home? Typically lenders require 20 % down')/100
    closing_cost_pct = st.number_input('Closing costs (% of home price)', value=4.0, step=0.01, help='How much will closing costs be as a % of home price, ex. 4%')/100


    st.markdown("# Operating Assumptions")
    monthly_hoa = st.number_input("👨‍🔧 HOA ($ monthly)", step=1, help="How much will you pay each month for home owners association fee?")
    ann_repair_pct = st.slider(" 👨‍🔧 Annual repairs (% of rents)", min_value = 0.0, max_value = 50.0, value = 1.0, step=0.5, help='How much will you budget to annual home repair expenses as a % of revenue? ex. 10% of annual revenue')/100
    property_tax_rate = st.slider("🏛️ Property tax rate (% of home price)",min_value = 0.0, max_value = 5.0, value = 0.85, step=0.01, help="What is your property tax rate? ex. 1% of home price")/100
    monthly_utilities = st.number_input("🔌 Monthly utilities ($)", value=150.0,  step=1.0, help='How much will you pay for utilities (gas, water, electric) per month? ex. $150/mo')
    monthly_internet = st.number_input("🗼Monthly internet & cable ($)", value=100.0, step=1.0, help='How much will you pay for internet & cable servies per month? ex. $100/mo')
    home_insurance = st.number_input("🛡️ Monthly home insurance ($)", value=140.0, step=1.0, help="How much will you pay for home insurance?")
    hosting_fee_pct = st.number_input('Hosting fee (% of rents)', value=3.0,  step=0.1, help='How much will Airbnb charge you for each booking? Typically its 3%')/100
    # credit_card_processing_pct = st.number_input('Credit Card Processing Fee (% of rents)', value=3.0,  step=0.1, help='What is the credit card processing fee? ex. 3%')/100
    credit_card_processing_pct = 0 
    prop_management_fee_pct = st.number_input('Property management fee (% of rents)', value=10.0, step=0.1, help='If you hired a property manager, then put their rate (ex 10% of your revenue), if not, then add a percentage to reflect the replinishment costs related to things like toilteries, paper towels, etc' )/100

    st.markdown('# Other Assumptions')
    start_up_costs = st.number_input('Start up costs ($)', step=1, help='These are one time costs, that you will spend to get your Airbnb up and running, ex. new furniture, new bedsheets.etc')
    discount_rate = st.slider('Discount rate (%)', min_value=0.0, max_value=50.0, value=5.0,  step=0.1, help = 'Discount rate is the minimum rate of return that you require to accept an investment. For example, if you choose a 5% discount rate, it means that if the project returns less than 5% return you will reject the investment')/100


npv = (bnb.npv(purchase_price, growth_rate, interest_rate, down_payment, Avg_daily_rate, Occupancy_rate, Ann_rent_growth, 
monthly_hoa, ann_repair_pct, property_tax_rate, monthly_utilities, monthly_internet, home_insurance, hosting_fee_pct, 
credit_card_processing_pct, prop_management_fee_pct, discount_rate, closing_cost_pct, start_up_costs))

home_expenses= bnb.home_specific_costs(purchase_price, monthly_hoa, ann_repair_pct, property_tax_rate, 
                        monthly_utilities, monthly_internet, home_insurance)

st.caption("""The STR investment evaluation app helps you decide if a property is a good investment. 
           It analyzes your property and calculates key financial metrics like Net Present Value (NPV), 
           Internal Rate of Return (IRR), and Monthly Net Income. With this information, you can make better investment decisions. 
           """)


st.markdown("### 📊 Investment metrics:")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Net Present Value", value=round(npv[9],0), help="Net Present Value (NPV) is a way to see if an investment will make you money. It's like adding up all the money you'll get in the future from your investment, plus the money you'll get when you sell the investment at the end, and then subtracting the amount of money you originally put into the investment. If the number you get is positive, it means you'll make a profit on the investment. But if the number is negative, it means you won't make a profit and it might not be a good investment.")
with col2:
    st.metric(label="Internal Rate of Return % (IRR)", value=round(npv[11]*100,0), help="This is the rate of return you receive from your investment each year")
with col3:
    st.metric(label="First Year Monthly Net Income", value=round(npv[6][1]/12, 0), help="This is the first year net income you will receive from your property after all expenses are paid.")


st.markdown('### 💰 Annual Cashflows by Year:')
st.caption('This table shows the monthly cashflows from your property by year (assuming you hold the investment for 10 years). The cashflows include the income you will make from renting your property, the expenses you will pay, and the cash you will receive from the sale of your property in the final year. The sale of your property will include profit from your home appreciation and the built up equity in your property.')
            
cash_flows_df = pd.DataFrame((npv[6])[:10], columns=['Annual Net Cashflows'], index=[1,2,3,4,5,6,7,8,9,10])
cash_flows_df.reset_index(inplace=True)
cash_flows_df.rename(columns={'index':'Year'}, inplace=True)
st.dataframe(cash_flows_df.style.format("{:.0f}"), width=500)


st.markdown('### 🤓 Key Insights')
st.write('1. **Occupancy days** of', round(12.0*Occupancy_rate,0), 'months out of the year.')
st.write('6. **Occupancy rate** must be  :', np.round(((((npv[2]*-1)[0]) + ((home_expenses*-1)[0])) / (Avg_daily_rate))/365 * 100,0), " % to break even")
st.write('2. **Down payment** will be', round(down_payment*purchase_price,0), 'USD')
st.write('3. **Closing costs** will be', round(closing_cost_pct*purchase_price,0), 'USD')
st.write('4. **Monthly mortgage payment** (principal + interest) will be', np.round((npv[2]/12)[0]))
st.write('5. **Monthly Operating Expenses**', np.round((home_expenses/12)[0]), 'which includes HOA, internet, taxes, utilities, home insurance, and repairs')
st.write('6. **Profit from sale** of property at year 10',round(npv[1],0), 'USD')
