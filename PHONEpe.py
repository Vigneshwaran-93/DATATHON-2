import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Write a page title
st. set_page_config(layout="wide")

st.title('DATATHON 2.0')
st.title("Phone-Pe Transaction Geo-Visualization")

st.header("Select one Option from below")


opt1=st.checkbox("National Data", key="opt1", help="National Wise Summary of Data")
opt2=st.checkbox("State Wise Data", key="opt2", help="National Wise Summary of Data")

#Reading Files
df_t=pd.read_csv("Transaction Data.csv")
df_u=pd.read_csv("User Data.csv")
df_pop=pd.read_csv("data3.csv")
df_cat=pd.read_csv("cat.csv")
df_brd=pd.read_csv("data4.csv")
STATES2=["andaman-_-nicobar-islands",
"andhra-pradesh",
"arunachal-pradesh",
"assam",
"bihar",
"chandigarh",
"chhattisgarh",
"dadra-_-nagar-haveli-_-daman-_-diu",
"delhi",
"goa",
"gujarat",
"haryana",
"himachal-pradesh",
"jammu-_-kashmir",
"jharkhand",
"karnataka",
"kerala",
"ladakh",
"lakshadweep",
"madhya-pradesh",
"maharashtra",
"manipur",
"meghalaya",
"mizoram",
"nagaland",
"odisha",
"puducherry",
"punjab",
"rajasthan",
"sikkim",
"tamil-nadu",
"telangana",
"tripura",
"uttar-pradesh",
"uttarakhand",
"west-bengal",
]


if opt1==True :
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Map of State wise Transaction count and amount")
        st.image("images/1.png", width=None)
    with col2:
        st.subheader("Map of State wise Population and avg transaction amt")
        st.image("images/2.png", width=None)
    with col3:
        st.subheader("Map of State wise Population and Avg Count")
        st.image("images/3.png", width=None)

    col1, col2, col3 = st.columns(3)
    with col1:

        st.subheader("Top Ten States by Count")
        df_state_total = df_t.groupby(["State"]).sum()
        er1=df_state_total[["Count", "Amount"]].sort_values(by=['Count'], ascending=False).head(10)
        er1["State"]=er1.index
        er1.sort_values("Count")
        st.dataframe(data=er1, width=500, height=300, use_container_width=True)
        st.bar_chart(data=er1, x="State", y="Count", width=500, height=500, use_container_width=True)
    with col2:
        st.subheader("Top Ten States by Amount")
        df_state_total = df_t.groupby(["State"]).sum()
        er2 = df_state_total[["Count", "Amount"]].sort_values(by=['Amount'], ascending=False).head(10)
        er2["State"] = er1.index
        er2.sort_values("Amount", inplace=True)
        st.dataframe(data=er2, width=500, height=300, use_container_width=True)
        st.bar_chart(data=er2, x="State", y="Amount", width=500, height=500, use_container_width=True)

    with col3:
        st.subheader("Top Ten States by population, Sort by count and amount")
        df_pop_total = df_pop.sort_values(by=['Population','Urban Population','Count','Amount'], ascending=False).head(10)
        er2 = df_pop_total[['Population',"Urban Population","Count", "Amount"]].sort_values(by=['Amount'], ascending=False).head(10)
        er2["State"] = er2.index
        er2.sort_values("Amount")
        st.dataframe(data=er2, width=500, height=300, use_container_width=True)
        st.bar_chart(data=er2, x="State", y="Population", width=500, height=500, use_container_width=True)

    df_pop2=df_pop.copy()
    df_pop2["Avg_trans_count"] = df_pop2["Count"] / df_pop2["Population"]
    df_pop2["Avg_trans_amt"] = df_pop2["Count"] / df_pop2["Population"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Top Ten States by AVG Transaction Count")
        st.dataframe(df_pop2[["State","Count",	"Amount",	"Population", "Avg_trans_count"]].sort_values("Avg_trans_count", ascending=False))
        ee1=df_pop2[["State", "Count", "Amount", "Population", "Avg_trans_count"]].sort_values("Avg_trans_count",ascending=False)
        st.bar_chart(data=ee1, x="State", y="Avg_trans_count", width=500, height=500, use_container_width=True)

    with col2:
        st.subheader("Top Ten States by AVG Transaction Amount")
        st.dataframe(df_pop2[["State","Count",	"Amount",	"Population", "Avg_trans_amt"]].sort_values("Avg_trans_amt", ascending=False))
        ee1=df_pop2[["State", "Count", "Amount", "Population", "Avg_trans_amt"]].sort_values("Avg_trans_amt")
        st.bar_chart(data=ee1, x="State", y="Avg_trans_amt", width=500, height=500, use_container_width=True)
    st.markdown("""---""")

if opt2==True:
    with st.form(key='my_form'):
        state_1=st.selectbox("Select State", STATES2,)
        submit_button = st.form_submit_button(label='Submit')

    st.subheader("State Wise Totals")
    df_state_wise=df_t.groupby(["State"]).sum()
    st.dataframe(df_state_wise[["Count", "Amount"]].loc[state_1])
    k1,k2=df_state_wise[["Count", "Amount"]].loc[state_1]
    avg_transt_val=k2/k1
    st.markdown("### **:green[{}'s]** avg transaction count is **:red[{}]**".format(state_1,str(avg_transt_val)))
    #transc by pop
    df_spop_wise = df_pop.groupby(["State"]).sum()
    k1, k2 = df_spop_wise[["Count", "Population"]].loc[state_1]
    avg_transt_val = k1 / k2
    st.markdown("### **:green[{}'s]** per person transaction count for is **:red[{}]**".format(state_1, str(avg_transt_val)))
    # transc by pop amount
    df_spop_wise = df_pop.groupby(["State"]).sum()
    k1, k2 = df_spop_wise[["Amount", "Population"]].loc[state_1]
    avg_transt_val = k1 / k2
    st.markdown("### **:green[{}'s]** per person transaction amount for is **:red[{}]**".format(state_1, str(avg_transt_val)))
    #stat top performing Category
    k = df_t[df_t["State"] == "andaman-_-nicobar-islands"][["Catogery", "Count", "Amount"]].groupby(
        "Catogery").sum().sort_values(by=['Amount'], ascending=False).head(1).index
    g=(df_cat[df_cat["Category"]==k[0]]["Meaning"]).values
    st.markdown("### **:green[{}'s]** Top performing Category is **:red[{}]**".format(state_1, str(g[0])))

    # stat top performing year
    t=df_t[df_t["State"] == state_1][["Quater", "Count", "Amount"]].groupby("Quater").sum().sort_values(by=['Amount'],
                                                                                                      ascending=False).head(1).index
    st.markdown("### **:green[{}'s]** Top performing Quarter is **:red[{}]**".format(state_1, str(t[0])))

    # stat top performing year
    t = df_t[df_t["State"] == state_1][["Year", "Count", "Amount"]].groupby("Year").sum().sort_values(by=['Amount'], ascending=False).head(1).index
    st.markdown("### **:green[{}'s]** Top performing Year is **:red[{}]**".format(state_1, str(t[0])))

    y=df_u[df_u["State"] == state_1][["Brand", "Count"]].groupby("Brand").sum().sort_values(by=['Count'], ascending=False).head(1).index
    g = (df_brd[df_brd["Brand"] == y[0]]["Brand Name"]).values
    st.markdown("### **:green[{}'s]** Top performing Phone Brand is  is **:red[{}]**".format(state_1, str(g[0])))

    st.markdown("""---""")
    col1, col2, col3  = st.columns(3)

    with col1:
        st.subheader("State Wise Category Performance")
        temp_df_23 = df_t[df_t["State"] == state_1][["Catogery", "Count", "Amount"]].groupby("Catogery").sum().sort_values(by=['Amount'], ascending=False)
        temp_df_23["Category"] = temp_df_23.index

        # Plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        temp_df_23 = temp_df_23.sort_values(by="Category")
        # Add traces
        fig.add_trace(
            go.Scatter(x=temp_df_23.index, y=temp_df_23["Count"], name="Count Data"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=temp_df_23.index, y=temp_df_23["Amount"], name="Amount Data"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Year vs count and Amount"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Category")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Count</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Amount</b>", secondary_y=True)

        #fig.show()
        st.plotly_chart(fig, use_container_width=True)
        # PLot End



        st.dataframe(temp_df_23)
        st.dataframe(df_cat)


    with col2:
        st.subheader("State Wise Quarter Performance")
        temp_df_23 = df_t[df_t["State"] == state_1][["Quater", "Count", "Amount"]].groupby("Quater").sum().sort_values(by=['Amount'], ascending=False)
        temp_df_23["Quarter"] = temp_df_23.index

        # Plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        temp_df_23 = temp_df_23.sort_values(by="Quarter")
        # Add traces
        fig.add_trace(
            go.Scatter(x=temp_df_23.index, y=temp_df_23["Count"], name="Count Data"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=temp_df_23.index, y=temp_df_23["Amount"], name="Amount Data"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Quarter vs count and Amount"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Quarter")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Count</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Amount</b>", secondary_y=True)

        #fig.show()
        st.plotly_chart(fig, use_container_width=True)
        # PLot End
        st.dataframe(temp_df_23)


    with col3:
        st.subheader("State Wise Year Performance")

        temp_df_24 = df_t[df_t["State"] == state_1][["Year", "Count", "Amount"]].groupby("Year").sum().sort_values(by=['Amount'], ascending=False)
        temp_df_24["Year"] = temp_df_24.index
        #st.dataframe(temp_df_24)
        #temp_df_24.reset_index(inplace=True)
        #temp_df_24 = temp_df_24.sort_values(by="Year", axis=1)

        # Plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=temp_df_24.index, y=temp_df_24["Count"], name="Count Data"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=temp_df_24.index, y=temp_df_24["Amount"], name="Amount Data"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Year vs count and Amount"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Year")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Count</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Amount</b>", secondary_y=True)

        #fig.show()
        st.plotly_chart(fig,use_container_width=True)
        # PLot End
        st.dataframe(temp_df_24)

    # SECTION 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("State Wise Phone Brand Performence")
        temp_df_23 = df_u[df_u["State"] == state_1][["Brand", "Count"]].groupby("Brand").sum().sort_values(by=['Count'], ascending=False)
        temp_df_23["Brand"] = temp_df_23.index
        st.line_chart(data=temp_df_23, x="Brand", y="Count", width=500, height=500, use_container_width=True)



    with col2:
        st.subheader("Phone Brand Label")
        st.dataframe(df_brd)

    st.markdown("""---""")




if st.button("EXIT"):
  st.warning('EXITING IN PROGRESS')
  st.stop()
  st.success('Thank you !')
  st.runtime.legacy_caching.clear_cache()
  st.experimental_rerun()






