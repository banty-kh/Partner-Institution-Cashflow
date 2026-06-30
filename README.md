# Partner Institution Cashflow & Sponsorship Dashboard

An interactive, premium Streamlit dashboard for monitoring partner institution budget allocations, actual monthly disbursements, and student sponsorships. Sourced dynamically from Google Sheets with offline backup support.

## 🚀 Key Features

*   **Live Google Sheet Sync:** Reads the latest data directly from the online spreadsheet at runtime with an **Offline Fallback** to a local Excel file if internet connectivity is unavailable. Includes a **Sync to Local Disk** utility to update the local backup cache.
*   **Context-Propagating Aggregation Pipeline:** Resolves multi-row school approvals and demographic breakdowns correctly
*   **Dynamic Pivot Builder:** Allows users to dynamically configure pivot rows, columns, metrics, and aggregation functions (sum, mean, count) to slice and dice datasets, accompanied by automatic data-labeled Plotly bar charts.
*   **Institution Factsheet Explorer:** View individual institution details, payout cycles, and category-specific remaining balances.
*   **Interactive Master Registry:** Built on `streamlit-aggrid` with column sorting, resizing, pagination, and advanced conditional formatting rules (highlighting high budgets in blue, high balances in red, and large cohorts in green).
*   **Soft Pastel Gradient Theme:** Styled with custom CSS utilizing Outfit typography, glassmorphism filters, and a soft yellow-green-blue gradient.

## 📦 Project Structure

*   `app.py`: Main Streamlit application codebase.
*   `requirements.txt`: Python library dependencies required for deployment.
*   `Partner Institution Cashflow_FY 2026-2027.xlsx`: Offline backup data cache.
*   `README.md`: Application documentation and instructions.
*   `LICENSE`: MIT License terms.

## 🛠️ Local Installation

1.  Clone or extract the project files.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
