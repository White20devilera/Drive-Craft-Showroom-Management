<p align="center">
  <!-- 🏢 Showroom Logo එක (උඹට කැමති වෙන පින්තූරයක් වුණත් දාන්න පුළුවන්) -->
  <img src="cars/no_image.png" alt="Drive Craft Logo" width="120" style="border-radius: 12px;"/>
</p>

<h1 align="center">DRIVE CRAFT</h1>
<p align="center"><b>Vehicle Showroom & Inventory Manager v1.0.0</b></p>
<p align="center">Enterprise Automobile Dealership Logistics & Billing Framework | Desktop Edition</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-0052CC?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-00BFFF?style=flat-square" alt="GUI">
  <img src="https://img.shields.io/badge/Database-MySQL-EA5B0C?style=flat-square&logo=mysql&logoColor=white" alt="Database">
  <img src="https://img.shields.io/badge/Document_Engine-ReportLab-26A65B?style=flat-square" alt="ReportLab">
  <img src="https://img.shields.io/badge/Status-Active-47A248?style=flat-square" alt="Status">
</p>

---


## 📸 System Walkthrough & Interface

### 🔐 Secure Multi-Role Authentication
Features dynamic secure login using **SHA-256 cryptographic password hashing**. Supports role-based access control (RBAC), automatically stripping management tabs (Analytics and Supplier Directory) and restrictive operations (such as record deletion) for ordinary `Sales_Staff` accounts while keeping full privilege capabilities locked for the `Admin`.

[Login Interface]

<img width="1773" height="1026" alt="login" src="https://github.com/user-attachments/assets/e3ceeccb-15c4-41b7-9f6b-01496b44dc8b" />


### 📊 Centralized Fleet Inventory Dashboard
Provides real-time fleet analytics tracking total stock capacity, availability status, vehicles sold, and collective showroom revenue. Features an interactive inventory database grid with instant multi-criteria searching (Brand/Model) and state filtering. It includes a dynamic preview pane that rendering high-fidelity vehicle visuals without redundant file duplication.

[Dashboard & Fleet Directory]

<img width="1776" height="1026" alt="dashboard" src="https://github.com/user-attachments/assets/cb18deaa-4d7d-4656-825d-84fec683227f" />


### 🚨 Autonomous Smart Inventory Triggers
Equipped with an integrated threshold-monitoring listener. The system automatically deploys system-wide visual alert notifications if the showroom's available stock descends beneath critical operational minimums, warning staff of immediate replenishment needs.

[Low Stock Warning Protocol]

<img width="1777" height="1025" alt="stock_warning" src="https://github.com/user-attachments/assets/ff5d2785-7488-4896-afa6-882c71089e63" />


### ⚙️ Full-Lifecycle Fleet Provisioning
A technical, comprehensive pipeline enabling incoming fleet registration. Accommodates granular vehicular technical specifications including fuel-cell architecture, precise engine displacement metrics, multi-tier transmission configurations, and premium accessory badge selection checkboxes.

[Add New Vehicle Framework]

<img width="1776" height="1026" alt="add_vehicles" src="https://github.com/user-attachments/assets/1d21229e-efee-4e9f-9fc9-eb4b9b00ce2e" />


### 💰 Real-Time Transaction Ledger & Billing Terminal
An advanced point-of-sale console parsing live user inputs through background arithmetic threads to evaluate agreed prices, initial advance commitments, and balance-due totals instantly. Features an embedded read-only live text preview of the transaction schema before formalizing commits.

[Sales Processing Terminal]

<img width="1782" height="1032" alt="sell_and_bill" src="https://github.com/user-attachments/assets/c896ac51-ae6c-470e-b1c5-a3f992120d70" />


### 🖨️ Automated Transaction Invoice Compilation
Simultaneously translates confirmed transaction states into a permanent relational db commit, structural text preview logs, and generates a client-ready, fully styled transaction invoice ledger layout dynamically engineered via native **ReportLab utility sheets**.

[Generated ReportLab Transaction Invoice]

<img width="1033" height="922" alt="generated_sales_invoice" src="https://github.com/user-attachments/assets/4f4f0ab6-72b3-4346-b0b9-e888ad527100" />


### 📜 Comprehensive Sales Audit Directory
Maintains a full structural history log of prior dealership transactions. Integrates asynchronous live filtering protocols across multiple data-layer entries (Customer Names, NIC sequences, and explicit Sale IDs) and features an instant re-printing portal link.

[Audited Sales Records Directory]

<img width="1782" height="1027" alt="sales_history" src="https://github.com/user-attachments/assets/ff27e408-2b82-4f7d-aec9-d31c13018c89" />


### 📈 Predictive Business Analytics Engine
Integrates a dedicated scientific visualization panel powered by an isolated **Matplotlib matrix renderer**. Utilizes automated dynamic window listeners that auto-refresh upon tab selection to fetch fresh data queries, mapping out visual brand composition and revenue growth timelines seamlessly.

[Matplotlib Data Visualization Panel]

<img width="1781" height="1030" alt="business_analytics" src="https://github.com/user-attachments/assets/979d7a87-9c6d-4770-87de-1777bee4f5c3" />


### 🪪 International & Local Supplier Frameworks
An integrated directory map tracking local automobile dealer houses and foreign import auction hubs across Japan and the United Kingdom, sorting operational agent commissions inside professional currency-formatted structures.

[Supplier & Sourcing Agent Directory]

<img width="1777" height="1026" alt="suppliers" src="https://github.com/user-attachments/assets/8aa11720-b9b7-40f4-b2a6-50c4cce68f64" />


---

## ✨ Premium Architectural Superpowers

*   **Zero-Copy Image Pipeline:** Eliminates resource wastage by optimizing absolute system paths instead of replicating duplicate physical assets inside storage pools, solving concurrent file collisions permanently.
*   **Bulletproof Sri Lankan Regex Validations:** Implements strict validation arrays enforcing rigorous structural compliance verification across classic 9-digit `V/X` frameworks, contemporary 12-digit national identity numbers (NIC), and global Sri Lankan telecommunication numbering formats.
*   **Garbage Collection Protection:** Fixes standard Tkinter engine reference-drop anomalies by hard-locking underlying bitmap data memory addresses directly onto active widget labels, mitigating graphic fading defects.
*   **Threaded Real-Time Clock Core:** Runs an independent localized chronometer updating interface timestamps seamlessly without introducing main UI application freezing states.

---

## 🛠️ Software Stack & Core Technologies
*   **GUI Framework:** CustomTkinter (Modernized Tkinter Wrapper)
*   **Engine Core:** Python 3.11+
*   **Database Management:** MySQL Relational Model (via XAMPP Data Layer)
*   **Vector Engine & Plotting:** Matplotlib Data Systems
*   **Asset Encoding Engine:** Pillow (PIL) Processing Toolkit
*   **Document Generation:** ReportLab Layout Engine

---

## 🚀 Deployment & Local Environment Setup

### 1. Database Provisioning
1. Launch your local **XAMPP Control Panel** and execute the **Apache** and **MySQL** services.
2. Direct your browser node to the database administration panel: `http://localhost/phpmyadmin/`.
3. Provision an empty relational repository container named exactly: **`showroom_db`**.
4. Access the **Import** tab window pane, allocate the database backup structural file **`showroom_db.sql`** located in the root root repository folder, and trigger execution.

### 2. Software Installation & Run Execution
Execute these terminal sequencing queries inside your localized system environment workspace folder:

```bash
# 1. Clone the core engineering repository system
git clone [https://github.com/White20devilera/Drive-Craft-Showroom-Management.git](https://github.com/White20devilera/Drive-Craft-Showroom-Management.git)
cd Drive-Craft-Showroom-Management

# 2. Deploy required operational dependencies and libraries
pip install -r requirements.txt

# 3. Boot up the main application framework
python main.py
