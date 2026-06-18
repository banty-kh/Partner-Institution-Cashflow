import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
from st_aggrid import AgGrid, GridOptionsBuilder

# Set page config
st.set_page_config(
    page_title="Partner Institution Cashflow & Sponsorship Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700 !important;
        color: #0f172a;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #0f766e 0%, #115e59 40%, #1e3a8a 100%);
        color: white;
        border-radius: 16px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.15), 0 8px 10px -6px rgba(15, 118, 110, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-container h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
    }
    
    .header-container p {
        color: #ccfbf1;
        margin: 10px 0 0 0;
        font-size: 1.15rem;
        font-weight: 400;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-top: 4px solid #0f766e;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #14b8a6;
    }
    
    .kpi-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    
    .kpi-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 8px;
        letter-spacing: -0.03em;
    }
    
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fef9c3 0%, #dcfce7 50%, #e0f2fe 100%);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.025em;
        border-bottom: 2px solid rgba(0, 0, 0, 0.1) !important;
        padding-bottom: 15px;
        margin-bottom: 25px;
        text-shadow: none !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 6px !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        display: block;
        margin-top: 15px;
    }
    
    /* Multiselect tags styling in Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        border: 1px solid rgba(0, 0, 0, 0.15) !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"]:hover {
        border-color: #0f766e !important;
        box-shadow: 0 0 0 1px #0f766e !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #0f766e !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] span[data-baseweb="tag"]:hover {
        background-color: #0d9488 !important;
        border-color: #14b8a6 !important;
    }
    
    [data-testid="stSidebar"] span[data-baseweb="tag"] button {
        color: white !important;
    }
    
    /* Buttons styling */
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
        width: 100%;
    }
    
    .stButton button:hover, .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(13, 148, 136, 0.4) !important;
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
    }
    
    .stButton button:active, .stDownloadButton button:active {
        transform: translateY(0) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: none !important;
        margin-bottom: 25px;
        background: linear-gradient(90deg, #fef9c3 0%, #dcfce7 50%, #e0f2fe 100%);
        padding: 6px 12px !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-bottom: none !important;
        transition: all 0.25s ease !important;
        padding: 0 16px !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0f172a !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
    }
    
    /* Table headers styling */
    .stDataFrame {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper to format currency following the Indian Numbering System (INR: e.g., ₹12,34,567)
def format_inr(val):
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)
    
    # Format as rounded integer
    int_part = str(int(round(val)))
    
    # If the number is negative, handle the sign
    is_negative = int_part.startswith('-')
    if is_negative:
        int_part = int_part[1:]
        
    int_reversed = int_part[::-1]
    
    # Group the last 3 digits
    groups = []
    groups.append(int_reversed[:3])
    
    # Group subsequent digits in pairs of 2
    remaining = int_reversed[3:]
    for i in range(0, len(remaining), 2):
        groups.append(remaining[i:i+2])
        
    formatted_int = ",".join(groups)[::-1]
    
    if is_negative:
        return f"-₹{formatted_int}"
    return f"₹{formatted_int}"


def render_fit_table(df, height=None):
    """Render compact read-only tables with wrapped, visible columns."""
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        resizable=True,
        sortable=False,
        filterable=False,
        wrapText=True,
        autoHeight=True,
        wrapHeaderText=True,
        autoHeaderHeight=True,
        minWidth=110,
    )
    gb.configure_grid_options(
        domLayout="autoHeight",
        autoSizeStrategy={"type": "fitGridWidth", "defaultMinWidth": 110},
        suppressHorizontalScroll=True,
    )

    AgGrid(
        df,
        gridOptions=gb.build(),
        height=height or max(120, min(420, 48 + (len(df) + 1) * 42)),
        theme="alpine",
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True,
        reload_data=True,
        custom_css={
            ".ag-header-cell-label": {"white-space": "normal", "line-height": "1.2"},
            ".ag-cell": {"line-height": "1.35", "display": "flex", "align-items": "center"},
        },
    )

# POC name cleanup (mapping Anjali to Barla)
def clean_poc_name(val):
    if pd.isna(val) or str(val).strip() == '':
        return val
    clean_val = str(val).strip()
    if clean_val.lower() == 'anjali' or 'anjali' in clean_val.lower():
        return 'Barla'
    return clean_val

# Name Standardization function
def standardize_name(name):
    if not isinstance(name, str):
        return name
    name_clean = " ".join(name.replace('\n', ' ').split())
    name_lower = name_clean.lower()
    
    # Exclude summary elements
    if name_lower in ['total', 'total school students', 'total sponsorship', 'add base school effect', 'total ', 'total sponsorship ']:
        return "FILTER_OUT_SUMMARY_ROW"
        
    # Substring mappings
    if 'dew drop' in name_lower:
        return 'Dew Drop Academy'
    if 'ayang trust' in name_lower:
        return 'Ayang Trust'
    if 'agape friendship' in name_lower or 'agape children care' in name_lower:
        return 'Agape Friendship School'
    
    mapping = {
        'baptist school panso': 'Baptist School Panso',
        'baptist school, panso': 'Baptist School Panso',
        'baptist school': 'Baptist School Panso',
        'don bosco school (c)': 'Don Bosco School (C)',
        'don bosco school c': 'Don Bosco School (C)',
        'don bosco c': 'Don Bosco School (C)',
        'foundation for maraoni orphans and destitutes upliftment': 'Foundation for Maraoni Orphans',
        'foundation for maraoni orphans and destitutes upliftment (fmodu)': 'Foundation for Maraoni Orphans',
        'fmodu': 'Foundation for Maraoni Orphans',
        'general thangal memorial institutie': 'General Thangal Memorial Institute',
        'general thangal memorial institute': 'General Thangal Memorial Institute',
        'holy vineyard': 'Holy Vineyard School Changlangshu',
        'holy vineyard school changlangshu': 'Holy Vineyard School Changlangshu',
        'jn nazareth english school idp': 'JN Nazareth English School',
        'jn nazareth english school': 'JN Nazareth English School',
        'khongjom eng standard school': 'Khongjom Standard English School',
        'khongjom standard english school': 'Khongjom Standard English School',
        'little drops life public charitable trust': 'Little Drops Life Public Charitable Trust',
        'little drop life public charitable trust': 'Little Drops Life Public Charitable Trust',
        'little flower school': 'Little Flower Public School',
        'little flower public school': 'Little Flower Public School',
        'mercy children home, senapati': 'Mercy Children Home, Senapati',
        'mercy home': 'Mercy Home, CCpur',
        'paangkriang friendship academy': 'Paangkriang Friendship School',
        'paangkriang friendship school': 'Paangkriang Friendship School',
        'peacemark vision english school': 'Peace Mark Vision English School',
        'queen mary school': 'Queen Mary School',
        'scholars\' pakshimi school': 'Scholars\' Pakshimi High School',
        'sophia english school': 'Sofia English School',
        'saint francis de sales': 'St. Francis de Sales School',
        'st. francis de sales school': 'St. Francis de Sales School',
        'st john paul ii school': 'St. John Paul II School',
        'st john paull ii school': 'St. John Paul II School',
        'st. john paul ii school': 'St. John Paul II School',
        'st. joseph school, singngat (idps)': 'St. Joseph School, Singngat',
        'st. joseph school, singngat': 'St. Joseph School, Singngat',
        'st peters school': 'St. Peter School',
        'st.peters school': 'St. Peter School',
        'st. peter school': 'St. Peter School',
        'st. vincent school': 'St. Vincent High School',
        'st xaviers school, moirang': 'St. Xavier\'s School, Moirang',
        'st xavier\'s school, moirang': 'St. Xavier\'s School, Moirang',
        'st. xavier\'s school, moirang': 'St. Xavier\'s School, Moirang',
        'st. xavier\'s high school': 'St. Xavier\'s High School, Makhan',
        'st. xavier\'s high school, makhan': 'St. Xavier\'s High School, Makhan',
        'st. xavier\'s high school, thanlon': 'St. Xavier\'s High School, Thanlon',
        'inside-ne': 'inSIDE-NE',
        'inside-ne (shom-inn- academy)': 'inSIDE-NE'
    }
    
    if name_lower in mapping:
        return mapping[name_lower]
    return name_clean

# Cache data loading from source (BytesIO or file path)
@st.cache_data
def load_data_from_source(source):
    xls = pd.ExcelFile(source)
    
    # Note: 'Team RACI' and 'Mastersheet' sheets are excluded from analysis.
    # 1. AMOUNT Sheet
    df_amt = pd.read_excel(xls, sheet_name='Amount')
    df_amt.columns = [str(c).strip() for c in df_amt.iloc[0]]
    df_amt = df_amt.iloc[1:].reset_index(drop=True)

    amount_records = []
    current_school_orig = None
    current_institution = None
    current_poc = None
    current_state = None
    current_basetype = None
    current_donor = None
    current_rec_by = None

    def parse_num(v):
        if pd.isna(v) or str(v).strip() == '' or str(v).strip().lower() == 'nan':
            return 0.0
        try:
            return float(str(v).replace(',', '').strip())
        except:
            return 0.0

    # Track running sum of school budgets to detect the grand total row
    running_total_sanc = 0.0

    for idx, row in df_amt.iterrows():
        school_val = row.get('School')
        is_main = pd.notna(school_val) and str(school_val).strip() != ""
        
        if is_main:
            std_sch = standardize_name(school_val)
            if std_sch == "FILTER_OUT_SUMMARY_ROW":
                current_school_orig = None
                current_institution = None
                continue
                
            current_school_orig = school_val
            current_institution = std_sch
            current_poc = clean_poc_name(row.iloc[0])
            current_state = row.iloc[5]
            current_basetype = row.iloc[6]
            current_donor = row.iloc[69]
            current_rec_by = row.iloc[70]
            
        if current_institution is None:
            continue

        tuition = parse_num(row.iloc[48])
        hostel = parse_num(row.iloc[53])
        nutrition = parse_num(row.iloc[58])
        salary = parse_num(row.iloc[63])
        sheet_total = parse_num(row.iloc[65])
        total = tuition + hostel + nutrition + salary
        if total == 0 and sheet_total > 0:
            total = sheet_total

        # Parse detailed columns
        tuition_stud = parse_num(row.iloc[45])
        tuition_rate = parse_num(row.iloc[46])
        tuition_freq = parse_num(row.iloc[47])

        hostel_stud = parse_num(row.iloc[50])
        hostel_rate = parse_num(row.iloc[51])
        hostel_freq = parse_num(row.iloc[52])

        nutrition_stud = parse_num(row.iloc[55])
        nutrition_rate = parse_num(row.iloc[56])
        nutrition_freq = parse_num(row.iloc[57])

        salary_staff = parse_num(row.iloc[60])
        salary_rate = parse_num(row.iloc[61])
        salary_freq = parse_num(row.iloc[62])

        # Skip bottom summary row
        is_summary = False
        for cell in row:
            if pd.notna(cell) and ("a+b" in str(cell).lower() or "total" in str(cell).lower()):
                is_summary = True
                break

        # Check running sum grand total row detection against the sheet-level Total Amount cell.
        # Row-level sanctioned totals are intentionally calculated from each expense head's
        # sanctioned Total Amount column so multi-row approvals are aggregated accurately.
        if not is_main and running_total_sanc > 0:
            if abs(sheet_total - running_total_sanc) < 1.0 and sheet_total > 100000.0:
                is_summary = True
                current_school_orig = None
                current_institution = None

        if not is_main and is_summary:
            current_school_orig = None
            current_institution = None
            continue

        has_sanction = (tuition > 0 or hostel > 0 or nutrition > 0 or salary > 0 or total > 0)

        if is_main or has_sanction:
            amount_records.append({
                'School_Original': current_school_orig,
                'Institution': current_institution,
                'POC': current_poc,
                'State': current_state,
                'Type of School': current_basetype,
                'Sanc_Tuition': tuition,
                'Sanc_Hostel': hostel,
                'Sanc_Nutrition': nutrition,
                'Sanc_Salary': salary,
                'Sanc_Total': total,
                'Sanc_Tuition_Students': tuition_stud,
                'Sanc_Tuition_Rate': tuition_rate,
                'Sanc_Tuition_Freq': tuition_freq,
                'Sanc_Hostel_Students': hostel_stud,
                'Sanc_Hostel_Rate': hostel_rate,
                'Sanc_Hostel_Freq': hostel_freq,
                'Sanc_Nutrition_Students': nutrition_stud,
                'Sanc_Nutrition_Rate': nutrition_rate,
                'Sanc_Nutrition_Freq': nutrition_freq,
                'Sanc_Salary_Staff': salary_staff,
                'Sanc_Salary_Rate': salary_rate,
                'Sanc_Salary_Freq': salary_freq,
                'Donor': current_donor,
                'Recommended_By': current_rec_by
            })
            running_total_sanc += total

    df_amt_cleaned = pd.DataFrame(amount_records)

    # 2. STUDENT SUMMA Sheet
    df_sum = pd.read_excel(xls, sheet_name='Sanctioned student number Summa')
    df_sum.columns = [str(c).strip() for c in df_sum.iloc[0]]
    df_sum = df_sum.iloc[1:].reset_index(drop=True)

    summa_records = []
    current_institution = None

    for idx, row in df_sum.iterrows():
        school_name = row.get('School name')
        sl_no = row.get('Sl no')
        
        is_main = pd.notna(school_name) and str(school_name).strip() != ""
        has_sl = pd.notna(sl_no) and str(sl_no).strip() != ""
        
        if is_main:
            if has_sl:
                std_sch = standardize_name(school_name)
                if std_sch == "FILTER_OUT_SUMMARY_ROW":
                    current_institution = None
                else:
                    current_institution = std_sch
            else:
                # Summary/subtotal row at the bottom
                current_institution = None
                
        if current_institution is None:
            continue
            
        def parse_int(v):
            if pd.isna(v) or str(v).strip() == '' or str(v).strip().lower() == 'nan':
                return 0
            try:
                return int(float(str(v).replace(',', '').strip()))
            except:
                return 0
                
        summa_records.append({
            'Institution': current_institution,
            'Students_Tuition': parse_int(row.iloc[6]),
            'Students_Hostel': parse_int(row.iloc[7]),
            'Students_Nutrition': parse_int(row.iloc[8]),
            'Students_Total_Sponsored': parse_int(row.iloc[9]),
            'BaseEffect_Tuition': parse_int(row.iloc[10]),
            'BaseEffect_Hostel': parse_int(row.iloc[11]),
            'BaseEffect_Nutrition': parse_int(row.iloc[12]),
            'BaseEffect_Total': parse_int(row.iloc[13]),
            'Unique_Students': parse_int(row.iloc[15])
        })
    df_sum_cleaned = pd.DataFrame(summa_records)

    poc_map = df_amt_cleaned.groupby('Institution')['POC'].first().to_dict()

    # 3. CASHFLOW Sheet
    df_cf_raw = pd.read_excel(xls, sheet_name='Cashflow 26-27')
    df_cf_raw.columns = [str(c).strip() for c in df_cf_raw.iloc[0]]
    df_cf_raw = df_cf_raw.iloc[1:].reset_index(drop=True)

    cf_rows = []
    curr_sl, curr_inst, curr_poc, curr_state = None, None, None, None
    curr_total_approved, curr_overall_paid, curr_total_unpaid = None, None, None
    curr_prog, curr_village, curr_loc = None, None, None

    for idx, row in df_cf_raw.iterrows():
        sl_val = row.get('Sl no')
        inst_val = row.get('Institution')
        state_val = row.get('State')
        
        if pd.notna(sl_val) or (pd.notna(inst_val) and inst_val != curr_inst and pd.notna(state_val)):
            curr_sl = sl_val
            curr_inst = inst_val
            raw_poc = row.get('POC')
            is_placeholder = False
            if pd.isna(raw_poc) or str(raw_poc).strip() == '':
                is_placeholder = True
            else:
                try:
                    float(str(raw_poc).replace(',', '').strip())
                    is_placeholder = True
                except ValueError:
                    is_placeholder = False
                    
            if is_placeholder:
                if pd.notna(curr_inst):
                    std_sch = standardize_name(curr_inst)
                    curr_poc = clean_poc_name(poc_map.get(std_sch, raw_poc))
                else:
                    curr_poc = clean_poc_name(raw_poc)
            else:
                curr_poc = clean_poc_name(raw_poc)
            curr_state = state_val
            curr_total_approved = row.get('Total approved')
            curr_prog = row.get('Programme')
            curr_village = row.get('Village')
            curr_loc = row.get('Location')
            curr_overall_paid = row.iloc[59]
            curr_total_unpaid = row.iloc[60]
        
        if curr_inst is None or pd.isna(curr_inst):
            continue
            
        expense_head = row.iloc[9]
        if pd.isna(expense_head) and pd.isna(row.iloc[58]):
            if row.notna().sum() <= 5:
                continue
                
        r_dict = {
            'POC': curr_poc,
            'Sl no': curr_sl,
            'Institution': curr_inst,
            'Programme': curr_prog,
            'Village': curr_village,
            'Location': curr_loc,
            'State': curr_state,
            'Total approved': curr_total_approved,
            'Expense head': expense_head,
            'Total paid per expense Head': row.iloc[58],
            'Oveall Total Paid': curr_overall_paid,
            'Total Unpaid': curr_total_unpaid,
            'Donor': row.iloc[61],
            'Beneficiary': row.iloc[62],
            # Payout Installments and transaction dates
            'Inst1_Date': row.iloc[64],
            'Inst1_Ref': row.iloc[65],
            'Inst2_Date': row.iloc[66],
            'Inst2_Ref': row.iloc[67],
            'Inst3_Date': row.iloc[68],
            'Inst3_Ref': row.iloc[69],
            'Inst4_Date': row.iloc[70],
            'Inst4_Ref': row.iloc[71],
            'Inst5_Date': row.iloc[72],
            'Inst5_Ref': row.iloc[73]
        }
        
        months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']
        for m_idx, m_name in enumerate(months):
            start_col = 10 + m_idx * 4
            r_dict[f'{m_name}_Students'] = row.iloc[start_col]
            r_dict[f'{m_name}_Amount'] = row.iloc[start_col+1]
            r_dict[f'{m_name}_Total'] = row.iloc[start_col+2]
            r_dict[f'{m_name}_Remark'] = row.iloc[start_col+3]
            
        cf_rows.append(r_dict)

    df_cf_cleaned = pd.DataFrame(cf_rows)
    df_cf_cleaned['Institution'] = df_cf_cleaned['Institution'].apply(standardize_name)
    df_cf_cleaned = df_cf_cleaned[df_cf_cleaned['Institution'] != "FILTER_OUT_SUMMARY_ROW"].copy()

    # Align cashflow approved amounts with the sanctioned Total Amount columns
    # from the Amount sheet for each respective expense head. The Cashflow
    # sheet's `Total approved` column can repeat an institution-level total on
    # every itemized row, so replacing it here keeps cashflow exports and
    # remaining-balance calculations category-specific.
    sanctioned_totals_by_head = df_amt_cleaned.groupby('Institution').agg({
        'Sanc_Tuition': 'sum',
        'Sanc_Hostel': 'sum',
        'Sanc_Nutrition': 'sum',
        'Sanc_Salary': 'sum'
    }).to_dict('index')

    def get_sanctioned_total_for_expense(row):
        head = str(row.get('Expense head', '')).strip().lower()
        inst_totals = sanctioned_totals_by_head.get(row.get('Institution'), {})

        if 'tuition' in head or 'admission' in head:
            return inst_totals.get('Sanc_Tuition', 0.0)
        if 'hostel' in head:
            return inst_totals.get('Sanc_Hostel', 0.0)
        if 'nutrition' in head:
            return inst_totals.get('Sanc_Nutrition', 0.0)
        if 'salary' in head or 'teacher' in head or 'founder' in head:
            return inst_totals.get('Sanc_Salary', 0.0)

        return row.get('Total approved', 0.0)

    df_cf_cleaned['Total approved'] = df_cf_cleaned.apply(get_sanctioned_total_for_expense, axis=1)

    # Note: 'Partners Monthly Payment' sheet is always excluded from analysis.

    # Merging and Aggregating
    df_amt_agg = df_amt_cleaned.groupby('Institution').agg({
        'State': 'first',
        'Type of School': 'first',
        'POC': 'first',
        'Sanc_Tuition': 'sum',
        'Sanc_Hostel': 'sum',
        'Sanc_Nutrition': 'sum',
        'Sanc_Salary': 'sum',
        'Sanc_Total': 'sum',
        'Sanc_Tuition_Students': 'sum',
        'Sanc_Tuition_Rate': 'first',
        'Sanc_Tuition_Freq': 'first',
        'Sanc_Hostel_Students': 'sum',
        'Sanc_Hostel_Rate': 'first',
        'Sanc_Hostel_Freq': 'first',
        'Sanc_Nutrition_Students': 'sum',
        'Sanc_Nutrition_Rate': 'first',
        'Sanc_Nutrition_Freq': 'first',
        'Sanc_Salary_Staff': 'sum',
        'Sanc_Salary_Rate': 'first',
        'Sanc_Salary_Freq': 'first',
        'Donor': 'first',
        'Recommended_By': 'first'
    }).reset_index()

    df_sum_agg = df_sum_cleaned.groupby('Institution').agg({
        'Students_Tuition': 'sum',
        'Students_Hostel': 'sum',
        'Students_Nutrition': 'sum',
        'Students_Total_Sponsored': 'sum',
        'BaseEffect_Tuition': 'sum',
        'BaseEffect_Hostel': 'sum',
        'BaseEffect_Nutrition': 'sum',
        'BaseEffect_Total': 'sum',
        'Unique_Students': 'sum'
    }).reset_index()

    # Aggregate actual monthly payments, total paid, and total balance from the Cashflow sheet
    df_mon_agg = df_cf_cleaned.groupby('Institution').agg({
        'April_Total': 'sum',
        'May_Total': 'sum',
        'June_Total': 'sum',
        'July_Total': 'sum',
        'August_Total': 'sum',
        'September_Total': 'sum',
        'October_Total': 'sum',
        'November_Total': 'sum',
        'December_Total': 'sum',
        'January_Total': 'sum',
        'February_Total': 'sum',
        'March_Total': 'sum',
        'Total paid per expense Head': 'sum',
        'Total Unpaid': 'first'
    }).reset_index()

    # Rename columns to match df_mon_agg expectations in the UI
    df_mon_agg = df_mon_agg.rename(columns={
        'April_Total': 'Paid_April',
        'May_Total': 'Paid_May',
        'June_Total': 'Paid_June',
        'July_Total': 'Paid_July',
        'August_Total': 'Paid_August',
        'September_Total': 'Paid_September',
        'October_Total': 'Paid_October',
        'November_Total': 'Paid_November',
        'December_Total': 'Paid_December',
        'January_Total': 'Paid_January',
        'February_Total': 'Paid_February',
        'March_Total': 'Paid_March',
        'Total paid per expense Head': 'Paid_Till_Now',
        'Total Unpaid': 'Balance_To_Be_Paid'
    })

    # Set Monthly_Approved to 0.0 (reference values are no longer pulled from the excluded Monthly Payment sheet)
    df_mon_agg['Monthly_Approved'] = 0.0

    # Aggregate installment columns from cashflow to school level
    df_inst_agg = df_cf_cleaned.groupby('Institution').agg({
        'Inst1_Date': 'first',
        'Inst1_Ref': 'first',
        'Inst2_Date': 'first',
        'Inst2_Ref': 'first',
        'Inst3_Date': 'first',
        'Inst3_Ref': 'first',
        'Inst4_Date': 'first',
        'Inst4_Ref': 'first',
        'Inst5_Date': 'first',
        'Inst5_Ref': 'first',
    }).reset_index()

    df_merged = df_amt_agg.merge(df_sum_agg, on='Institution', how='outer')
    df_merged = df_merged.merge(df_mon_agg, on='Institution', how='outer')
    df_merged = df_merged.merge(df_inst_agg, on='Institution', how='left')

    # Metadata fixups
    df_merged['State'] = df_merged['State'].fillna('Unknown')
    df_merged['Type of School'] = df_merged['Type of School'].fillna('Unknown')
    df_merged['Donor'] = df_merged['Donor'].fillna('Unmapped')
    df_merged['Recommended_By'] = df_merged['Recommended_By'].fillna('N/A')
    
    # Map POC from Cashflow sheet first (to respect user overrides like Barla), fallback to Amount sheet
    poc_map_cf = df_cf_cleaned.groupby('Institution')['POC'].first().to_dict()
    df_merged['POC'] = df_merged['Institution'].map(poc_map_cf)
    
    poc_map_amt = df_amt_cleaned.groupby('Institution')['POC'].first().to_dict()
    df_merged['POC'] = df_merged['POC'].fillna(df_merged['Institution'].map(poc_map_amt)).fillna('Unknown')
    
    # Fill numeric columns
    numeric_cols = [
        'Sanc_Tuition', 'Sanc_Hostel', 'Sanc_Nutrition', 'Sanc_Salary', 'Sanc_Total',
        'Students_Tuition', 'Students_Hostel', 'Students_Nutrition', 'Students_Total_Sponsored',
        'BaseEffect_Tuition', 'BaseEffect_Hostel', 'BaseEffect_Nutrition', 'BaseEffect_Total',
        'Unique_Students', 'Monthly_Approved', 'Paid_Till_Now', 'Balance_To_Be_Paid',
        'Sanc_Tuition_Students', 'Sanc_Tuition_Rate', 'Sanc_Tuition_Freq',
        'Sanc_Hostel_Students', 'Sanc_Hostel_Rate', 'Sanc_Hostel_Freq',
        'Sanc_Nutrition_Students', 'Sanc_Nutrition_Rate', 'Sanc_Nutrition_Freq',
        'Sanc_Salary_Staff', 'Sanc_Salary_Rate', 'Sanc_Salary_Freq'
    ]
    for col in numeric_cols:
        if col in df_merged.columns:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce').fillna(0.0)
            
    df_merged['Balance_To_Be_Paid'] = df_merged['Sanc_Total'] - df_merged['Paid_Till_Now']
            
    # Clean Cashflow numerics
    df_cf_cleaned['Total approved'] = pd.to_numeric(df_cf_cleaned['Total approved'], errors='coerce').fillna(0.0)
    df_cf_cleaned['Total paid per expense Head'] = pd.to_numeric(df_cf_cleaned['Total paid per expense Head'], errors='coerce').fillna(0.0)
    df_cf_cleaned['Total Unpaid'] = pd.to_numeric(df_cf_cleaned['Total Unpaid'], errors='coerce').fillna(0.0)
    df_cf_cleaned['Expense head'] = df_cf_cleaned['Expense head'].fillna('Other fees')

    # Clean monthly amounts
    months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']
    for m in months:
        df_cf_cleaned[f'{m}_Total'] = pd.to_numeric(df_cf_cleaned[f'{m}_Total'], errors='coerce').fillna(0.0)

    return df_merged, df_cf_cleaned

import os
import datetime

# Google Sheet Link
google_sheet_link = "https://docs.google.com/spreadsheets/d/1nYUoPkf22OoGvJ6PkKZAlv0_1T7ZwrtyUIIMq53WTnI/edit?usp=drive_link"
google_sheets_url = google_sheet_link.replace("/edit?usp=drive_link", "/export?format=xlsx")

# Local file path for offline sync
LOCAL_FILE_PATH = os.path.join(os.path.dirname(__file__), "Partner Institution Cashflow_FY 2026-2027.xlsx")

# Load the data from Google Sheet or Local backup
df_schools = None
df_cashflow = None
data_source = ""
last_sync_time = None

with st.spinner("📥 Loading cashflow data..."):
    # Try fetching live data first
    try:
        response = requests.get(google_sheets_url, timeout=15)
        response.raise_for_status()
        df_schools, df_cashflow = load_data_from_source(io.BytesIO(response.content))
        data_source = "Live (Google Sheets)"
    except Exception as live_err:
        # Fallback to local offline file
        if os.path.exists(LOCAL_FILE_PATH):
            try:
                df_schools, df_cashflow = load_data_from_source(LOCAL_FILE_PATH)
                data_source = "Offline (Local Disk File)"
                mtime = os.path.getmtime(LOCAL_FILE_PATH)
                last_sync_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception as local_err:
                st.error("Failed to load both live data and offline file.")
                st.write(f"Live fetch error: {live_err}")
                st.write(f"Local file load error: {local_err}")
                st.stop()
        else:
            st.error(f"Failed to fetch live data and no local offline file exists at `{LOCAL_FILE_PATH}`.")
            st.write(f"Live fetch error: {live_err}")
            st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("## Global Filters")

# State Filter
states = sorted(df_schools['State'].unique().tolist())
selected_states = st.sidebar.multiselect("Select State", states, default=[], placeholder="All States (Overall)")

# POC Filter
pocs = sorted(df_schools['POC'].unique().tolist())
selected_pocs = st.sidebar.multiselect("Select POC", pocs, default=[], placeholder="All POCs (Overall)")

# Type of School Filter
base_types = sorted(df_schools['Type of School'].unique().tolist())
selected_base_types = st.sidebar.multiselect("Select Type of School", base_types, default=[], placeholder="All Types (Overall)")

# Donor Filter
donors = sorted(df_schools['Donor'].unique().tolist())
selected_donors = st.sidebar.multiselect("Select Donor", donors, default=[], placeholder="All Donors (Overall)")

st.sidebar.markdown("---")
# Visual Power Query Data Pipeline Flow
with st.sidebar.expander("🛠️ Power Query ETL Pipeline", expanded=False):
    st.markdown("""
    <div style='font-size: 0.85rem; line-height: 1.4; color: #cbd5e1;'>
        <div style='margin-bottom: 8px;'><strong>1. Extract Data:</strong><br>Parsed 3 sheets (Amount, Summa, Cashflow) from Excel source.</div>
        <div style='margin-bottom: 8px;'><strong>2. Clean & Map POCs:</strong><br>Standardized POC name variations and resolved Anjali to <code>Barla</code>.</div>
        <div style='margin-bottom: 8px;'><strong>3. Context Propagation:</strong><br>Forward-filled empty school names to correctly sum multi-approval rows (e.g., Alpha hostel).</div>
        <div style='margin-bottom: 8px;'><strong>4. Standardize Names:</strong><br>Fuzzy-matched and standardized variations of school names.</div>
        <div style='margin-bottom: 8px;'><strong>5. Skip Summaries:</strong><br>Dynamically filtered out grand totals and bottom text summaries via Sl no & running sum.</div>
        <div><strong>6. Merge & Load:</strong><br>Aggregated payments and student counts to generate master schools registry.</div>
    </div>
    """, unsafe_allow_html=True)

# Apply filters to Master DataFrame
df_filtered = df_schools.copy()
if selected_states:
    df_filtered = df_filtered[df_filtered['State'].isin(selected_states)]
if selected_pocs:
    df_filtered = df_filtered[df_filtered['POC'].isin(selected_pocs)]
if selected_base_types:
    df_filtered = df_filtered[df_filtered['Type of School'].isin(selected_base_types)]
if selected_donors:
    df_filtered = df_filtered[df_filtered['Donor'].isin(selected_donors)]

# Apply filters to Cashflow DataFrame
df_cf_filtered = df_cashflow[
    (df_cashflow['Institution'].isin(df_filtered['Institution']))
]

# --- HEADER SECTION ---
st.markdown("""
<div class="header-container">
    <h1>Partner Institution Sponsorship & Cashflow Dashboard</h1>
    <p>Read-Only Live Analytics pipeline from the Management Google Sheet</p>
</div>
""", unsafe_allow_html=True)

# --- LOCAL SYNC OPTIONS CONTAINER ---
sync_card_style = """
<style>
.sync-container {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 18px 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 25px;
}
.status-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}
.status-live {
    background-color: #dcfce7;
    color: #15803d;
}
.status-offline {
    background-color: #fee2e2;
    color: #b91c1c;
}
</style>
"""
st.markdown(sync_card_style, unsafe_allow_html=True)

with st.container():
    sync_col1, sync_col2 = st.columns([3, 1])
    
    with sync_col1:
        status_badge = '<span class="status-badge status-live">Live Online</span>' if data_source == "Live (Google Sheets)" else '<span class="status-badge status-offline">Offline Mode</span>'
        st.markdown(f"""
<div style="padding-top: 4px;">
    <h4 style="margin: 0 0 6px 0; font-weight: 600; color: #1e293b; font-size: 1.15rem;">💾 Local File Sync {status_badge}</h4>
    <p style="margin: 0; color: #64748b; font-size: 0.9rem;">
        Current Data Source: <strong>{data_source}</strong> {f' | Last Synced: <strong>{last_sync_time}</strong>' if last_sync_time else ''}
    </p>
</div>
""", unsafe_allow_html=True)
        
    with sync_col2:
        st.write("") # spacing
        if st.button("🔄 Sync to Local Disk", use_container_width=True, help="Download online Google Sheet and overwrite local file"):
            with st.spinner("Downloading and writing local Excel backup..."):
                try:
                    response = requests.get(google_sheets_url, timeout=30)
                    response.raise_for_status()
                    with open(LOCAL_FILE_PATH, "wb") as f:
                        f.write(response.content)
                    st.cache_data.clear()
                    st.toast("✅ Offline local file updated successfully!")
                    st.success("Successfully synchronized and updated offline local disk file!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Sync failed: {e}")

# Validate empty selection
if df_filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your filters in the sidebar.")
    st.stop()

# --- TOP METRIC CARDS ---
col1, col2, col3, col4, col5 = st.columns(5)

total_schools = df_cf_filtered['Institution'].nunique()
total_students_sanc = int(df_filtered['Students_Total_Sponsored'].sum())
total_students_uniq = int(df_filtered['Unique_Students'].sum())
total_sanc_budget = df_filtered['Sanc_Total'].sum()
total_disbursed = df_filtered['Paid_Till_Now'].sum()
total_balance = df_filtered['Balance_To_Be_Paid'].sum()

disbursed_pct = (total_disbursed / total_sanc_budget * 100) if total_sanc_budget > 0 else 0

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Partner Institutions</div>
        <div class="kpi-value">{total_schools}</div>
        <div class="kpi-subtitle">Active Institutions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Unique Students</div>
        <div class="kpi-value">{total_students_uniq:,}</div>
        <div class="kpi-subtitle">Total Enrolled ({total_students_sanc:,} sponsored)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Approved</div>
        <div class="kpi-value">{format_inr(total_sanc_budget)}</div>
        <div class="kpi-subtitle">Sanctioned Budget</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Disbursed</div>
        <div class="kpi-value">{format_inr(total_disbursed)}</div>
        <div class="kpi-subtitle">{disbursed_pct:.1f}% Disbursed Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Outstanding Bal.</div>
        <div class="kpi-value">{format_inr(total_balance)}</div>
        <div class="kpi-subtitle">Pending Disbursements</div>
    </div>
    """, unsafe_allow_html=True)

# TABS FOR ORGANIZATION
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive View", "🏫 Institution Factsheet Explorer", "🎯 Monitoring & Evaluation", "📋 Raw Data & Exports"])

# ==================== TAB 1: EXECUTIVE VIEW ====================
with tab1:
    st.markdown("### Management & Donor Visual Overview")
    
    # Progress bar showing budget usage
    st.markdown(f"**Disbursement Progress: {format_inr(total_disbursed)} / {format_inr(total_sanc_budget)} ({disbursed_pct:.1f}% Paid)**")
    st.progress(min(disbursed_pct / 100.0, 1.0))
    
    st.markdown("#### 📊 Overall Sponsorship & Budget Summary")
    summary_data = {
        "Sponsorship Category": ["Tuition Fees Support", "Hostel Fees Support", "Nutrition Support", "Teacher / Founder Salary"],
        "Total Students Approved": [
            f"{int(df_filtered['Students_Tuition'].sum()):,}",
            f"{int(df_filtered['Students_Hostel'].sum()):,}",
            f"{int(df_filtered['Students_Nutrition'].sum()):,}",
            # Teacher/founder salary uses the sanctioned No of Teachers column
            # from the Amount sheet (Excel column BI, e.g. BI124 in the source).
            f"{int(df_filtered['Sanc_Salary_Staff'].sum()):,}"
        ],
        "Total Sanctioned Budget": [
            format_inr(df_filtered['Sanc_Tuition'].sum()),
            format_inr(df_filtered['Sanc_Hostel'].sum()),
            format_inr(df_filtered['Sanc_Nutrition'].sum()),
            format_inr(df_filtered['Sanc_Salary'].sum())
        ]
    }
    df_exec_summary = pd.DataFrame(summary_data)
    st.dataframe(df_exec_summary, hide_index=True, use_container_width=True)
    st.markdown("---")
    
    # Donut Chart for Sanctioned Expense Heads
    heads = ['Tuition', 'Hostel', 'Nutrition', 'Salary']
    values = [
        df_filtered['Sanc_Tuition'].sum(),
        df_filtered['Sanc_Hostel'].sum(),
        df_filtered['Sanc_Nutrition'].sum(),
        df_filtered['Sanc_Salary'].sum()
    ]
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=heads, 
        values=values, 
        hole=.4,
        marker=dict(colors=px.colors.qualitative.Pastel2),
        texttemplate='₹%{value:,.0f}<br>%{percent}',
        textinfo='value+percent'
    )])
    fig_donut.update_layout(
        title_text="Approved Budget by Expense Category",
        title_x=0.0,
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )

    df_state_school_counts = (
        df_filtered.groupby('State')['Institution']
        .nunique()
        .reset_index(name='Number of Partner Institutions')
        .sort_values('Number of Partner Institutions', ascending=False)
    )
    fig_state_schools = px.bar(
        df_state_school_counts,
        x='State',
        y='Number of Partner Institutions',
        title="Number of Partner Institutions by State",
        labels={
            'State': 'State',
            'Number of Partner Institutions': 'Number of Partner Institutions'
        },
        color='State',
        color_discrete_sequence=px.colors.qualitative.Pastel2,
        text='Number of Partner Institutions'
    )
    fig_state_schools.update_layout(
        title_x=0.0,
        template="plotly_white",
        showlegend=False,
        yaxis=dict(dtick=1)
    )
    fig_state_schools.update_traces(textposition='outside')

    budget_chart_col, state_school_chart_col = st.columns(2)
    with budget_chart_col:
        st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with state_school_chart_col:
        st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
        st.plotly_chart(fig_state_schools, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Grouped Bar chart: Statewise Sanctioned vs Paid
    df_state = df_filtered.groupby('State')[['Sanc_Total', 'Paid_Till_Now']].sum().reset_index()
    fig_state = go.Figure()
    fig_state.add_trace(go.Bar(
        name='Approved Budget',
        x=df_state['State'],
        y=df_state['Sanc_Total'],
        marker_color=px.colors.qualitative.Pastel2[0],
        text=df_state['Sanc_Total'].apply(format_inr),
        textposition='auto'
    ))
    fig_state.add_trace(go.Bar(
        name='Actual Paid',
        x=df_state['State'],
        y=df_state['Paid_Till_Now'],
        marker_color=px.colors.qualitative.Pastel2[1],
        text=df_state['Paid_Till_Now'].apply(format_inr),
        textposition='auto'
    ))
    fig_state.update_layout(
        barmode='group',
        title_text="Approved Budget vs. Actual Disbursed by State",
        title_x=0.0,
        template="plotly_white",
        xaxis_title="State",
        yaxis=dict(title="Amount in INR", tickformat=',.0f', tickprefix='₹'),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15)
    )
    st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
    st.plotly_chart(fig_state, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Monthly Cashflow Outflow Schedule Line Chart
    months_cols = [f"Paid_{m}" for m in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']]
    months_names = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']
    
    monthly_sums = df_filtered[months_cols].sum().values
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=months_names,
        y=monthly_sums,
        mode='lines+markers+text',
        name='Actual Monthly Payout',
        text=[format_inr(val) if val > 0 else "" for val in monthly_sums],
        textposition='top center',
        line=dict(color='#0f766e', width=4),
        marker=dict(size=8, color='#0f766e'),
        fill='tozeroy',
        fillcolor='rgba(15, 118, 110, 0.1)'
    ))
    
    max_val = max(monthly_sums) if len(monthly_sums) > 0 else 0
    y_max = max_val * 1.3 if max_val > 0 else 10000
    
    fig_monthly.update_layout(
        title_text="Monthly Payout Timeline & Budget Cycle (April - March)",
        title_x=0.0,
        xaxis=dict(title="Month", type='category', range=[-0.8, 11.8]),
        yaxis=dict(title="Payout Amount in INR", tickformat=',.0f', tickprefix='₹', range=[0, y_max]),
        template="plotly_white",
        height=350,
        showlegend=False,
        margin=dict(l=80, r=40, t=50, b=50)
    )
    st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Live installment registry table under timeline
    all_inst_records = []
    for idx, row in df_filtered.iterrows():
        for inst_num in range(1, 6):
            date_val = row.get(f'Inst{inst_num}_Date')
            ref_val = row.get(f'Inst{inst_num}_Ref')
            is_paid = pd.notna(date_val) and str(date_val).strip() != '' and str(date_val).strip().lower() != 'nan'
            if is_paid:
                all_inst_records.append({
                    'Partner Institution': row['Institution'],
                    'State': row['State'],
                    'POC': row['POC'],
                    'Installment': f"{inst_num}st" if inst_num == 1 else (f"{inst_num}nd" if inst_num == 2 else (f"{inst_num}rd" if inst_num == 3 else f"{inst_num}th")),
                    'Payment Date': str(date_val).split(' ')[0],
                    'Reference No': ref_val,
                    'Approved Budget': format_inr(row['Sanc_Total']),
                    'Unpaid Balance': format_inr(row['Balance_To_Be_Paid'])
                })

    st.markdown("#### 💳 Installment Transaction Log")
    if all_inst_records:
        df_inst_rec = pd.DataFrame(all_inst_records)
        df_inst_rec.insert(0, 'Sl No', range(1, len(df_inst_rec) + 1))
        render_fit_table(df_inst_rec)
    else:
        st.info("No installment transaction dates are currently logged in columns 64-73 of the Google Sheet. Transactions and their payment dates will appear here automatically once recorded.")
        
    st.markdown("---")
    
    # Sponsorship Types Student counts
    std_types = ['Tuition', 'Hostel', 'Nutrition']
    std_counts = [
        df_filtered['Students_Tuition'].sum(),
        df_filtered['Students_Hostel'].sum(),
        df_filtered['Students_Nutrition'].sum()
    ]
    
    fig_std = px.bar(
        x=std_types, 
        y=std_counts,
        labels={'x': 'Sponsorship Type', 'y': 'Number of Students'},
        title="Total Students Sponsored by Category",
        color=std_types,
        color_discrete_sequence=px.colors.qualitative.Pastel2,
        text=std_counts
    )
    fig_std.update_layout(
        template="plotly_white", 
        showlegend=False
    )
    fig_std.update_traces(textposition='outside')
    st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
    st.plotly_chart(fig_std, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top 10 institutions by budget allocation
    top_10 = df_filtered.sort_values(by='Sanc_Total', ascending=True).tail(10)
    fig_top = px.bar(
        top_10,
        x='Sanc_Total',
        y='Institution',
        orientation='h',
        title="Top 10 Partner Institutions by Approved Budget",
        labels={'Sanc_Total': 'Total Budget (INR)', 'Institution': 'Partner Institution'},
        color='Institution',
        color_discrete_sequence=px.colors.qualitative.Pastel2,
        text=top_10['Sanc_Total'].apply(format_inr)
    )
    fig_top.update_layout(
        template="plotly_white",
        xaxis=dict(tickformat=',.0f', tickprefix='₹'),
        showlegend=False
    )
    fig_top.update_traces(textposition='outside')
    st.markdown('<div class="kpi-card" style="padding: 15px; border-top: 3px solid #0f766e;">', unsafe_allow_html=True)
    st.plotly_chart(fig_top, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: SCHOOL FACTSHEET ====================
with tab2:
    st.markdown("### Individual Partner Factsheet Explorer")
    
    school_list = sorted(df_filtered['Institution'].tolist())
    selected_school = st.selectbox("Select Partner Institution", school_list)
    
    sch_row = df_filtered[df_filtered['Institution'] == selected_school].iloc[0]
    
    st.markdown(f"""
    <div style="background-color: #f1f5f9; padding: 20px; border-radius: 12px; border-left: 6px solid #0f766e; margin-bottom: 25px;">
        <h4 style="margin: 0 0 10px 0; color: #0f766e; font-size: 1.2rem;">{selected_school} Details</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div><strong>State:</strong> {sch_row['State']}</div>
            <div><strong>Point of Contact (POC):</strong> {sch_row['POC']}</div>
            <div><strong>Type of School:</strong> {sch_row['Type of School']}</div>
            <div><strong>Donor Mapping:</strong> {sch_row['Donor']}</div>
            <div><strong>Recommended By:</strong> {sch_row['Recommended_By']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown("#### Student Demographics & Base Effect")
        demo_data = {
            "Sponsorship Category": ["Tuition Sponsorship", "Hostel Sponsorship", "Nutrition Sponsorship", "Total Sponsored", "Base Effect Tuition", "Base Effect Hostel", "Base Effect Nutrition", "Base Effect Total", "Unique Students Supported"],
            "Student Count": [
                int(sch_row['Students_Tuition']),
                int(sch_row['Students_Hostel']),
                int(sch_row['Students_Nutrition']),
                int(sch_row['Students_Total_Sponsored']),
                int(sch_row['BaseEffect_Tuition']),
                int(sch_row['BaseEffect_Hostel']),
                int(sch_row['BaseEffect_Nutrition']),
                int(sch_row['BaseEffect_Total']),
                int(sch_row['Unique_Students'])
            ]
        }
        df_demo = pd.DataFrame(demo_data)
        render_fit_table(df_demo)
        
        # Payment Cycle timeline in Left Column (HTML formatting flattened to prevent markdown code block treatment)
        st.markdown("#### Payout Cycle & Installment Timeline")
        inst_status = []
        for inst_num in range(1, 6):
            date_val = sch_row.get(f'Inst{inst_num}_Date')
            ref_val = sch_row.get(f'Inst{inst_num}_Ref')
            
            is_paid = pd.notna(date_val) and str(date_val).strip() != '' and str(date_val).strip().lower() != 'nan'
            
            inst_suffix = "st" if inst_num == 1 else ("nd" if inst_num == 2 else ("rd" if inst_num == 3 else "th"))
            
            if is_paid:
                inst_status.append({
                    'name': f"{inst_num}{inst_suffix} Installment",
                    'status': "✅ Disbursed",
                    'date': str(date_val).split(' ')[0],
                    'ref': str(ref_val),
                    'color': "#10b981",
                    'icon': "✓"
                })
            else:
                inst_status.append({
                    'name': f"{inst_num}{inst_suffix} Installment",
                    'status': "⏳ Pending",
                    'date': "Not logged",
                    'ref': "N/A",
                    'color': "#94a3b8",
                    'icon': "○"
                })

        timeline_html = "<div style='padding: 10px; font-family: \"Outfit\", sans-serif;'>"
        for item in inst_status:
            timeline_html += f"<div style='display: flex; margin-bottom: 12px; align-items: flex-start;'><div style='width: 26px; height: 26px; border-radius: 50%; background-color: {item['color']}; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px; font-size: 0.85rem;'>{item['icon']}</div><div style='flex-grow: 1;'><div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>{item['name']} - <span style='color: {item['color']}; font-weight: bold;'>{item['status']}</span></div><div style='font-size: 0.8rem; color: #64748b; margin-top: 2px;'>Date: {item['date']} | Ref: {item['ref']}</div></div></div>"
        timeline_html += "</div>"
        st.markdown(timeline_html, unsafe_allow_html=True)
        
    with c_right:
        st.markdown("#### Approved Budget Payout Structures")
        budget_data = {
            "Expense Head": [
                "Tuition Fees", 
                "Hostel Fees", 
                "Nutrition Support", 
                "Teacher/Founder Salary", 
                "Total Sanctioned Budget", 
                "Paid Till Now", 
                "Outstanding Balance"
            ],
            "No. of Students / Staff": [
                int(sch_row['Sanc_Tuition_Students']) if sch_row['Sanc_Tuition_Students'] > 0 else "-",
                int(sch_row['Sanc_Hostel_Students']) if sch_row['Sanc_Hostel_Students'] > 0 else "-",
                int(sch_row['Sanc_Nutrition_Students']) if sch_row['Sanc_Nutrition_Students'] > 0 else "-",
                int(sch_row['Sanc_Salary_Staff']) if sch_row['Sanc_Salary_Staff'] > 0 else "-",
                "-",
                "-",
                "-"
            ],
            "Rate per Month (INR)": [
                format_inr(sch_row['Sanc_Tuition_Rate']) if sch_row['Sanc_Tuition_Rate'] > 0 else "-",
                format_inr(sch_row['Sanc_Hostel_Rate']) if sch_row['Sanc_Hostel_Rate'] > 0 else "-",
                format_inr(sch_row['Sanc_Nutrition_Rate']) if sch_row['Sanc_Nutrition_Rate'] > 0 else "-",
                format_inr(sch_row['Sanc_Salary_Rate']) if sch_row['Sanc_Salary_Rate'] > 0 else "-",
                "-",
                "-",
                "-"
            ],
            "Frequency (Months)": [
                int(sch_row['Sanc_Tuition_Freq']) if sch_row['Sanc_Tuition_Freq'] > 0 else "-",
                int(sch_row['Sanc_Hostel_Freq']) if sch_row['Sanc_Hostel_Freq'] > 0 else "-",
                int(sch_row['Sanc_Nutrition_Freq']) if sch_row['Sanc_Nutrition_Freq'] > 0 else "-",
                int(sch_row['Sanc_Salary_Freq']) if sch_row['Sanc_Salary_Freq'] > 0 else "-",
                "-",
                "-",
                "-"
            ],
            "Amount Approved (INR)": [
                format_inr(sch_row['Sanc_Tuition']),
                format_inr(sch_row['Sanc_Hostel']),
                format_inr(sch_row['Sanc_Nutrition']),
                format_inr(sch_row['Sanc_Salary']),
                format_inr(sch_row['Sanc_Total']),
                format_inr(sch_row['Paid_Till_Now']),
                format_inr(sch_row['Balance_To_Be_Paid'])
            ]
        }
        df_budget = pd.DataFrame(budget_data)
        render_fit_table(df_budget)
        
    st.markdown("#### Itemized Cashflow & Disbursement Milestones")
    df_cf_school = df_cf_filtered[df_cf_filtered['Institution'] == selected_school].copy()
    
    if not df_cf_school.empty:
        # Calculate category-specific remaining balance
        def get_category_remaining_balance(row):
            sanc = pd.to_numeric(row['Total approved'], errors='coerce')
            if pd.isna(sanc):
                sanc = 0.0

            paid = pd.to_numeric(row['Total paid per expense Head'], errors='coerce')
            if pd.isna(paid):
                paid = 0.0
            return max(0.0, sanc - paid)

        df_cf_school['Category Remaining Balance'] = df_cf_school.apply(get_category_remaining_balance, axis=1)

        display_cf_cols = ['Expense head', 'Total approved', 'Total paid per expense Head', 'Category Remaining Balance']
        df_cf_show = df_cf_school[display_cf_cols].rename(columns={
            'Expense head': 'Expense Category',
            'Total approved': 'Approved Amount (INR)',
            'Total paid per expense Head': 'Disbursed Amount (INR)',
            'Category Remaining Balance': 'Remaining Balance (INR)'
        })
        # Format amounts in the table
        df_cf_show['Approved Amount (INR)'] = df_cf_show['Approved Amount (INR)'].map(format_inr)
        df_cf_show['Disbursed Amount (INR)'] = df_cf_show['Disbursed Amount (INR)'].map(format_inr)
        df_cf_show['Remaining Balance (INR)'] = df_cf_show['Remaining Balance (INR)'].map(format_inr)
        render_fit_table(df_cf_show)
        
        st.markdown("#### Monthly Payout Timeline breakdown (INR)")
        monthly_sched_cols = [f"{m}_Total" for m in months_names]
        df_monthly_sched = df_cf_school[['Expense head'] + monthly_sched_cols].copy()
        df_monthly_sched.columns = ['Expense head'] + months_names
        
        for col in months_names:
            df_monthly_sched[col] = pd.to_numeric(df_monthly_sched[col], errors='coerce').fillna(0.0)
            df_monthly_sched[col] = df_monthly_sched[col].map(format_inr)
            
        render_fit_table(df_monthly_sched)
    else:
        st.info("No itemized expense head disbursements found in the Cashflow logs for this school.")

# ==================== TAB 3: MONITORING & EVALUATION (M&E) ====================
with tab3:
    st.markdown("### 🎯 Monitoring & Evaluation (M&E) SOPs & Guidelines")
    st.markdown("Guiding questions, recording standards, and standard operating procedures for offline data verification and impact assessment.")
    
    # Custom HTML info box
    st.markdown("""
    <div style="background-color: #f0fdf4; border-left: 5px solid #16a34a; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
        <h5 style="color: #15803d; margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem;">📌 M&E Framework & SOP Purpose</h5>
        <p style="color: #166534; margin: 0; font-size: 0.95rem; line-height: 1.5;">
            Since offline student performance, attendance logs, and school audits are managed locally, this dashboard tab serves as the official M&E Standard Operating Procedure (SOP) manual. The guiding questions and guidelines below define how POCs should reconcile dashboard cashflow datasets with actual ground-level operations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_me_l, col_me_r = st.columns(2)
    
    with col_me_l:
        st.markdown("#### ❓ Guiding Questions for Data Review")
        
        with st.expander("📊 1. Budget & Sponsorship/Institution Utilization (Amount Sheet)", expanded=True):
            st.markdown("""
            * **Fund Utilization Check:**
              * *Is the institution budget being utilized exactly as sanctioned under the approved categories (Tuition, Hostel, Nutrition, Salary)?*
              * *Are there any budget categories showing zero expenditures where students were originally mapped?*
            * **Sponsorship Alignment:**
              * *Does the number of students sponsored in each category match the active numbers in the Master Registry?*
              * *Is the calculated cost per sponsored student matching the budget projections?*
            """)
            
        with st.expander("📅 2. Monthly Disbursement & Logs (Cashflow Sheet)", expanded=True):
            st.markdown("""
            * **Payout Timeliness:**
              * *Are the monthly disbursements released on time (referencing payout transaction dates vs planned timelines)?*
              * *Are there delays in logging installment details (Dates / Reference numbers)?*
            * **Cohort Validation:**
              * *Do the monthly student counts logged in the Cashflow sheet match active enrolled students in the institution registers?*
              * *What reasons are noted in the "Remark" columns for payment variances or delays?*
            """)
            
        with st.expander("👥 3. Student Enrolment & Retention (Summa Sheet)", expanded=True):
            st.markdown("""
            * **Cohort Performance:**
              * *What is the retention rate of the sponsored cohort (active vs dropped-out students)?*
              * *What is the proportion of unique students supported in Base Schools vs. Non-Base Schools?*
            * **Demographics Update:**
              * *Are there student demographic changes that require updating the master record?*
              * *Has the student size matched the physical capacity of the hostels and classrooms?*
            """)
            
    with col_me_r:
        st.markdown("#### 📋 Standard Operating Procedures (SOPs)")
        
        with st.expander("🛠️ SOP 1: Institution Verification & Cohort Tracking", expanded=True):
            st.markdown("""
            * **Objective:** Ensure student counts correspond to actual, attending beneficiaries.
            * **Required Actions:**
              * POCs must conduct monthly checks on student attendance sheets.
              * Log dropout details (date, reason) and submit immediate updates to the master file.
            * **Verification Standard:**
              * Monthly Cashflow student counts must match the verified physical registers.
            """)
            
        with st.expander("💼 SOP 2: Disbursement & Expense Audit", expanded=True):
            st.markdown("""
            * **Objective:** Ensure financial accountability and proper budget category use.
            * **Required Actions:**
              * Reconcile payout transaction dates and reference numbers with bank receipts.
              * Audit sample expenditures to confirm salary support reached teachers, and nutrition funds reached meals.
            * **Verification Standard:**
              * Verify that no payments are released without complete receipt validation of previous payouts.
            """)
            
        with st.expander("🔄 SOP 3: Monthly Log Reconciliation", expanded=True):
            st.markdown("""
            * **Objective:** Maintain dashboard sync integrity.
            * **Required Actions:**
              * Match dashboard figures with the physical cashbook of the partner institution.
              * Log any discrepancy explanation in the "Remark" column in the Cashflow sheet.
            * **Verification Standard:**
              * Complete monthly sync audits within 10 days of the cycle end.
            """)

    st.markdown("---")
    st.markdown("#### 📝 M&E Data Logging Template Guidelines")
    
    st.markdown("""
    When logging offline information into the Excel / Google Sheets, ensure the following standards are met to preserve dashboard data integrity:
    
    1. **Installment Date Formatting:** Log transaction dates strictly in `YYYY-MM-DD` format (avoid text descriptions like 'pending' or 'released' in date columns).
    2. **Disbursement Head Mapping:** Ensure expense heads in the Cashflow sheet match standardized naming (`Tuition fees`, `Hostel fees`, `Nutrition fees`, `Teacher's Salary`, `Founder Salary`).
    3. **Remark Standards:** Always enter the specific cause for payment delays or student variance in the `Remark` field (e.g., *'Delayed school reopening'*, *'Cohort transfer to Base school'*).
    4. **Student Counts:** Record actual active students attending for that month, rather than copy-pasting the approved cap.
    """)

# ==================== TAB 4: RAW DATA EXPLORER ====================
with tab4:
    st.markdown("### Search, Filter & Export Datasets")
    
    # Imports for conditional formatting
    from st_aggrid import JsCode
    
    # JsCode conditional cell stylings (Advanced conditional formatting)
    js_balance_style = JsCode("""
    function(params) {
        if (params.value > 500000) {
            return {
                'color': '#991b1b',
                'backgroundColor': '#fee2e2',
                'fontWeight': 'bold'
            };
        }
        return null;
    }
    """)
    
    js_students_style = JsCode("""
    function(params) {
        if (params.value > 100) {
            return {
                'color': '#15803d',
                'backgroundColor': '#dcfce7',
                'fontWeight': 'bold'
            };
        }
        return null;
    }
    """)

    js_budget_style = JsCode("""
    function(params) {
        if (params.value > 1000000) {
            return {
                'color': '#0369a1',
                'backgroundColor': '#e0f2fe',
                'fontWeight': 'bold'
            };
        }
        return null;
    }
    """)

    st.markdown("#### 🏫 Master Partner Institutions Registry")
    
    # Master Schools Registry AgGrid Configuration
    gb_master = GridOptionsBuilder.from_dataframe(df_filtered)
    gb_master.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb_master.configure_side_bar()
    gb_master.configure_default_column(resizable=True, filterable=True, sortable=True)
    
    # Apply Advanced Conditional Formatting
    gb_master.configure_column("Balance_To_Be_Paid", cellStyle=js_balance_style)
    gb_master.configure_column("Unique_Students", cellStyle=js_students_style)
    gb_master.configure_column("Sanc_Total", cellStyle=js_budget_style)
    
    grid_options_master = gb_master.build()
    
    AgGrid(
        df_filtered,
        gridOptions=grid_options_master,
        height=450,
        theme="alpine",
        enable_enterprise_modules=False,
        reload_data=True,
        allow_unsafe_jscode=True
    )
    
    csv_master = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Master Registry (CSV)",
        data=csv_master,
        file_name="master_schools_data_filtered.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("#### 💳 Itemized Cashflow Registry")
    
    # Itemized Cashflow Registry AgGrid Configuration
    gb_cf = GridOptionsBuilder.from_dataframe(df_cf_filtered)
    gb_cf.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb_cf.configure_side_bar()
    gb_cf.configure_default_column(resizable=True, filterable=True, sortable=True)
    
    # Apply Advanced Conditional Formatting to Cashflow table as well
    gb_cf.configure_column("Total Unpaid", cellStyle=js_balance_style)
    
    grid_options_cf = gb_cf.build()
    
    AgGrid(
        df_cf_filtered,
        gridOptions=grid_options_cf,
        height=450,
        theme="alpine",
        enable_enterprise_modules=False,
        reload_data=True,
        allow_unsafe_jscode=True
    )
    
    csv_cf = df_cf_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Cashflow Details (CSV)",
        data=csv_cf,
        file_name="cleaned_cashflow_filtered.csv",
        mime="text/csv"
    )

    st.markdown("---")
    # Dynamic Pivot Tables and Pivot Charts
    st.markdown("### Dynamic Pivot Builder")
    st.markdown("Build your own pivot tables and charts dynamically across school datasets.")
    
    pivot_df = df_filtered.copy()
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        pivot_index = st.multiselect("Rows (Index)", ["State", "POC", "Type of School", "Donor", "Institution"], default=["State"])
    with col_p2:
        pivot_columns = st.multiselect("Columns", ["State", "POC", "Type of School", "Donor"], default=[])
    with col_p3:
        pivot_values = st.selectbox("Values (Metric)", ["Sanc_Total", "Paid_Till_Now", "Balance_To_Be_Paid", "Unique_Students", "Students_Total_Sponsored"], index=0)
    with col_p4:
        pivot_agg = st.selectbox("Aggregation Function", ["sum", "mean", "count", "min", "max"], index=0)
        
    if pivot_index:
        try:
            # Construct the Pivot Table
            if pivot_columns:
                df_pivot = pd.pivot_table(pivot_df, index=pivot_index, columns=pivot_columns, values=pivot_values, aggfunc=pivot_agg, fill_value=0.0)
            else:
                df_pivot = pd.pivot_table(pivot_df, index=pivot_index, values=pivot_values, aggfunc=pivot_agg, fill_value=0.0)
                
            # Render the pivot table
            st.markdown("#### Pivot Table")
            st.dataframe(df_pivot, use_container_width=True)
            
            # Render a pivot chart
            st.markdown("#### Pivot Chart")
            df_plot = df_pivot.reset_index()
            
            is_monetary = pivot_values in ["Sanc_Total", "Paid_Till_Now", "Balance_To_Be_Paid"]
            
            if pivot_columns:
                df_plot = df_plot.melt(id_vars=pivot_index, value_name=pivot_values)
                if is_monetary:
                    plot_text = df_plot[pivot_values].apply(format_inr)
                else:
                    plot_text = df_plot[pivot_values].apply(lambda x: f"{int(round(x)):,}" if pd.notna(x) else "")
                fig_pivot = px.bar(
                    df_plot, 
                    x=pivot_index[0], 
                    y=pivot_values, 
                    color=df_plot.columns[-2], 
                    barmode="group", 
                    template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Pastel2,
                    text=plot_text
                )
            else:
                if is_monetary:
                    plot_text = df_plot[pivot_values].apply(format_inr)
                else:
                    plot_text = df_plot[pivot_values].apply(lambda x: f"{int(round(x)):,}" if pd.notna(x) else "")
                fig_pivot = px.bar(
                    df_plot, 
                    x=pivot_index[0], 
                    y=pivot_values, 
                    color=pivot_index[0], 
                    template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Pastel2,
                    text=plot_text
                )
            fig_pivot.update_traces(textposition='outside')
                
            fig_pivot.update_layout(
                title=f"{pivot_agg.upper()} of {pivot_values} by {', '.join(pivot_index)}",
                xaxis_title=pivot_index[0],
                yaxis_title=pivot_values,
                showlegend=False
            )
            
            if is_monetary:
                fig_pivot.update_layout(
                    yaxis=dict(tickformat=',.0f', tickprefix='₹')
                )
            else:
                fig_pivot.update_layout(
                    yaxis=dict(tickformat=',.0f')
                )
            st.plotly_chart(fig_pivot, use_container_width=True)
            
        except Exception as e:
            st.error(f"Cannot generate pivot: {e}")
    else:
        st.warning("Please select at least one Row (Index) for the pivot table.")
