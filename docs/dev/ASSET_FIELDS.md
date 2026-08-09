# Asset Inventory — Data Fields & Structure

> **Last updated:** 2026-08-09 16:46:21

This document defines the fields for each asset entry in the inventory. Each asset record includes these fields.

---

## Core Identity Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier | A-001 |
| `category` | Asset category | Cash & Cash Equivalents |
| `subcategory` | Specific type | High-Interest Savings Account |
| `asset_name` | Descriptive name | EQ Bank HISA |
| `asset_type` | Classification | Financial, Real Estate, Digital, etc. |

## Ownership Fields

| Field | Description | Example |
|-------|-------------|---------|
| `owner` | Primary owner | John Smith |
| `joint_owner` | Joint account holder (if any) | Jane Smith |
| `beneficiary` | Beneficiary designation | Children equally |
| `beneficiary_type` | Type of beneficiary | Spouse, Child, Estate, Trust |
| `custodian` | Custodian (for minors) | John Smith (for John Jr.) |
| `nominee` | Registered nominee name | John Smith RRSP |
| `trust_name` | Trust holding asset (if any) | Smith Family Trust |
| `corporation` | Holding corporation (if any) | Smith Holdings Inc. |

## Institution & Access Fields

| Field | Description | Example |
|-------|-------------|---------|
| `institution` | Bank/brokerage/company | EQ Bank |
| `institution_type` | Type of institution | Bank, Credit Union, Brokerage |
| `branch` | Branch location | Toronto Main |
| `account_number` | Account number | 1234-5678-9012 |
| `login_url` | Website URL | https://eqbank.ca |
| `login_username` | Online login username | john@email.com |
| `login_password` | Password (store securely!) | [See password manager] |
| `two_factor` | 2FA method | Authenticator app |
| `security_questions` | Security Q&A location | [See password manager] |

## Financial Value Fields

| Field | Description | Example |
|-------|-------------|---------|
| `currency` | Currency of asset | CAD |
| `acb` | Adjusted Cost Base | $50,000.00 |
| `acb_usd` | ACB in USD (if applicable) | $37,500.00 |
| `fmv` | Fair Market Value | $55,000.00 |
| `fmv_usd` | FMV in USD (if applicable) | $41,250.00 |
| `cost_basis` | Purchase price | $45,000.00 |
| `purchase_price` | Original purchase price | $45,000.00 |
| `current_balance` | Current balance | $55,000.00 |
| `market_value` | Current market value | $55,000.00 |
| `equity` | Equity (market value - debt) | $55,000.00 |
| `unrealized_gain` | Unrealized gain/loss | $10,000.00 |
| `unrealized_gain_pct` | Unrealized gain percentage | 22.2% |
| `annual_income` | Annual income generated | $2,750.00 |
| `yield_pct` | Yield percentage | 5.0% |
| `interest_rate` | Interest rate (if applicable) | 4.00% |
| `dividend_rate` | Dividend rate (if applicable) | $2.50/share |

## Date Fields

| Field | Description | Example |
|-------|-------------|---------|
| `open_date` | Account/asset open date | 2015-03-15 |
| `maturity_date` | Maturity date (GICs, bonds) | 2025-03-15 |
| `purchase_date` | Date of purchase | 2020-01-10 |
| `acquisition_date` | Date acquired | 2018-06-01 |
| `inception_date` | Fund inception date | 2010-01-01 |
| `expiry_date` | Expiry date (options, warrants) | 2025-12-31 |
| `last_valuation` | Last valuation date | 2024-12-31 |
| `last_update` | Record last updated | 2024-12-31 |
| `next_review` | Next scheduled review | 2025-06-30 |
| `transfer_date` | Date of transfer (inheritance, etc.) | 2023-01-01 |

## Registration & Tax Fields

| Field | Description | Example |
|-------|-------------|---------|
| `registration` | Account registration type | TFSA, RRSP, Non-registered |
| `tax_treatment` | How income is taxed | Tax-free, Tax-deferred, Taxable |
| `contribution_room` | Available contribution room | $65,000.00 |
| `contributions_ytd` | Contributions this year | $6,500.00 |
| `withdrawals_ytd` | Withdrawals this year | $0.00 |
| `rrsp_deduction` | RRSP deduction claimed | $5,000.00 |
| `cesg` | Canada Education Savings Grant | $500.00 |
| `clb` | Canada Learning Bond | $500.00 |
| `provincial_grant` | Ontario grant (RESPs) | $250.00 |
| `foreign_tax_credit` | Foreign tax paid | $500.00 |
| `withholding_tax` | Tax withheld at source | $100.00 |
| `asset_allocation` | For asset location planning | 60% equity, 40% fixed income |

## Location & Access Fields

| Field | Description | Example |
|-------|-------------|---------|
| `physical_location` | Where physical asset is kept | 123 Main St, Toronto |
| `safe_deposit_box` | Safe deposit box location | TD Bank, Bay & Bloor |
| `digital_wallet` | Crypto wallet name | Ledger Nano X |
| `exchange` | Crypto exchange | Newton, Shakepay |
| `online_access_url` | Direct access URL | https://app.eqbank.ca |
| `support_contact` | Customer support | 1-888-555-1234 |
| `advisor_name` | Financial advisor | Sarah Johnson |
| `advisor_contact` | Advisor contact info | sarah@wealthsimple.com |

## Insurance & Protection Fields

| Field | Description | Example |
|-------|-------------|---------|
| `insurance_coverage` | Insurance coverage amount | $500,000.00 |
| `insurance_provider` | Insurance company | Manulife |
| `insurance_policy` | Policy number | POL-12345 |
| `insurance_premium` | Annual premium | $1,200.00 |
| `insured_value` | Insured value | $500,000.00 |
| `replacement_cost` | Replacement cost | $600,000.00 |

## Status & Control Fields

| Field | Description | Example |
|-------|-------------|---------|
| `status` | Current status | Active, Dormant, Closed |
| `priority` | Priority level | High, Medium, Low |
| `volatility` | Asset volatility | Low, Medium, High |
| `liquidity` | How quickly convertible | High, Medium, Low |
| `transferable` | Can be transferred | Yes, No |
| `pledgeable` | Can be pledged as collateral | Yes, No |
| `accessible` | Access restrictions | None, Probate, LIRA lock-in |

## Beneficiary Designation Fields

> **Note:** `beneficiary` (in Ownership) and `primary_beneficiary` (below) are
> separate fields. The Excel **Beneficiaries** sheet and the audit view use
> `primary_beneficiary` falling back to `beneficiary` when the former is empty.

| Field | Description | Example |
|-------|-------------|---------|
| `primary_beneficiary` | Primary beneficiary | Jane Smith |
| `contingent_beneficiary` | Contingent beneficiary | Children equally |
| `beneficiary_pct_primary` | Primary beneficiary % | 100% |
| `beneficiary_pct_contingent` | Contingent beneficiary % | 50% each |
| `pod` | Payable on death designation | Yes |
| `tod` | Transfer on death registration | Yes |
| `poa` | Power of Attorney holder | Jane Smith |
| `mandate` | Quebec mandate (if applicable) | N/A |

## Estate Planning Fields

| Field | Description | Example |
|-------|-------------|---------|
| `probate_excluded` | Avoids probate | Yes |
| `will_clause` | Relevant will clause | Clause 4.2 |
| `trust_clause` | Trust reference | Schedule A |
| `estate_duty` | Subject to estate duty | No |
| `capital_gains_exemption` | LCGE eligible | Yes (QSBCS) |
| `succession_plan` | Succession plan reference | Family trust |
| `power_of_appointment` | Who has POA | Spouse |

## Documentation Fields

| Field | Description | Example |
|-------|-------------|---------|
| `document_path` | Location of documents | /Documents/BankStatements/EQ/ |
| `document_reference` | Document reference number | DOC-2024-001 |
| `last_statement` | Last statement date | 2024-12-31 |
| `statement_frequency` | Statement frequency | Monthly |
| `tax_slip_type` | Tax slip type | T5, T3, T5008 |
| `tax_slip_received` | Tax slip received | Yes |
| `annual_report` | Annual report available | Yes |

## Notes & Comments

| Field | Description | Example |
|-------|-------------|---------|
| `notes` | General notes | High-yield promotion rate |
| `alert` | Important alerts | Rate expires March 2025 |
| `todo` | Action items | Update beneficiary |
| `last_modified_by` | Who last modified | John Smith |
| `source` | How asset was acquired | Purchase, Inheritance, Gift |

---

## Sample Record Format

```
ID: A-001
Category: Cash & Cash Equivalents
Subcategory: High-Interest Savings Account
Asset Name: EQ Bank HISA
Asset Type: Financial
Owner: John Smith
Joint Owner: Jane Smith
Beneficiary: Children equally (50/50)
Beneficiary Type: Children
Institution: EQ Bank
Account Number: 1234-5678
Login URL: https://eqbank.ca
Login Username: john@email.com
Login Password: [See password manager]
2FA: Authenticator app
Currency: CAD
ACB: $50,000.00
FMV: $55,000.00
Interest Rate: 4.00%
Annual Income: $2,200.00
Open Date: 2020-01-15
Last Valuation: 2024-12-31
Last Updated: 2024-12-31
Next Review: 2025-06-30
Registration: Non-registered
Tax Treatment: Taxable
Physical Location: Online
Online Access: https://app.eqbank.ca
Support Contact: 1-888-555-1234
Insurance Coverage: CDIC insured to $100,000
Status: Active
Liquidity: High
Probate Excluded: No
Document Path: /Documents/Banking/EQ/
Notes: HISA promotional rate
Source: Opened online
```

---

## Summary of Fields

| Field Group | Count |
|-------------|-------|
| Core Identity | 5 |
| Ownership | 8 |
| Institution & Access | 9 |
| Financial Value | 16 |
| Date Fields | 10 |
| Registration & Tax | 12 |
| Location & Access | 8 |
| Insurance & Protection | 6 |
| Status & Control | 7 |
| Beneficiary Designation | 8 |
| Estate Planning | 7 |
| Documentation | 7 |
| Notes & Comments | 5 |
| **TOTAL** | **108** |

---

## Instructions for Python Script

The Python script should:

1. **Input**: Accept optional filters:
   - `--purpose`: estate, insurance, financial, general (default: general)
   - `--owner`: filter by owner name
   - `--category`: filter by category
   - `--status`: filter by status (active, dormant, all)
   - `--output`: md, excel, html, all (default: all)

2. **Output - Markdown**: Formatted table with:
   - Category headers
   - Asset rows with key fields visible
   - Summary statistics

3. **Output - Excel**: Workbook with:
   - Sheet 1: All Assets (master list)
   - Sheet 2: By Category (grouped)
   - Sheet 3: Summary (totals, counts)
   - Sheet 4: Access (login info only)
   - Sheet 5: Financial Summary (values, gains)
   - Sheet 6: Insurance (coverage details)
   - Sheet 7: Beneficiaries (designations)
   - Sheet 8: Estate (probate, will references)

4. **Output - HTML Dashboard**: Self-contained single-file HTML with:
   - **Soft UI Evolution** design language (neumorphism)
   - Professional dashboard layout
   - Fully editable inline
   - Export/save functionality
   - Responsive design

5. **Data Structure**: Dictionary with all 108 fields per asset
   - Pre-populated with the 517 asset types
   - Owner/beneficiary/institution left blank for user input
   - FMV/ACB left blank or default to $0.00

6. **Canadian-specific**: Include TFSA/RRSP/RESP contribution room tracking, CESG/CLB grants, provincial tax considerations.

---

## HTML Dashboard Specifications

### Design: Soft UI Evolution

**Visual Style:**
- Background: `#e0e5ec` (light gray)
- Card shadows: `box-shadow: 8px 8px 16px #b8bec7, -8px -8px 16px #ffffff;`
- Inset shadows: `box-shadow: inset 4px 4px 8px #b8bec7, inset -4px -4px 8px #ffffff;`
- Border radius: `20px` for cards, `12px` for buttons/inputs
- Font: Inter or system-ui
- Colors: Muted pastels with soft gradients

**Layout Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Asset Inventory Dashboard                    [≡]  │
├─────────────────────────────────────────────────────────────┤
│  STATS BAR: Total Assets │ Total Value │ Categories │ ...  │
├─────────────────────────────────────────────────────────────┤
│  FILTERS: [Category ▾] [Owner ▾] [Status ▾] [Search 🔍]  │
├─────────────────────────────────────────────────────────────┤
│  MAIN CONTENT                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Category 1  │ │ Category 2  │ │ Category 3  │ ...      │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │          │
│  │ │ Asset 1 │ │ │ │ Asset 4 │ │ │ │ Asset 7 │ │          │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │          │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │          │
│  │ │ Asset 2 │ │ │ │ Asset 5 │ │ │ │ Asset 8 │ │          │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │          │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │          │
│  │ │ Asset 3 │ │ │ │ Asset 6 │ │ │ │ Asset 9 │ │          │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  FOOTER: Export MD │ Export Excel │ Save HTML │ Last saved  │
└─────────────────────────────────────────────────────────────┘
```

**Dashboard Components:**

1. **Header**
   - Logo/title area
   - Navigation menu (hamburger)
   - Dark/light mode toggle

2. **Statistics Bar**
   - Total assets count
   - Total portfolio value (FMV)
   - Number of categories
   - Last updated timestamp
   - Quick actions (Add Asset, Export)

3. **Filter Bar**
   - Category dropdown
   - Owner dropdown
   - Status dropdown (Active/Dormant/All)
   - Search box
   - Advanced filters toggle

4. **Category Cards**
   - Collapsible accordion sections
   - Category name with count badge
   - Expand/collapse toggle
   - Visual icon per category

5. **Asset Cards** (inside categories)
   - Card with soft shadow
   - Asset name (bold)
   - Key fields visible (institution, value, status)
   - Click to expand/edit
   - Color-coded status indicator

6. **Asset Edit Modal/Panel**
   - Slides in from right or expands inline
   - All 108 fields organized in sections
   - Input fields with soft UI styling
   - Save/Cancel buttons
   - Delete option

7. **Footer/Action Bar**
   - Export to Markdown button
   - Export to Excel button
   - Save HTML (self-update) button
   - Last saved timestamp
   - Version indicator

**Color Palette:**
```
Primary:    #6c5ce7 (purple)
Secondary:  #00cec9 (teal)
Accent:     #fd79a8 (pink)
Success:    #00b894 (green)
Warning:    #fdcb6e (yellow)
Danger:     #e17055 (coral)
Info:       #74b9ff (blue)
Background: #e0e5ec
Card:       #e0e5ec
Text:       #2d3436
Muted:      #636e72
```

**Interactive Features:**
- Inline editing (click to edit)
- Auto-save to localStorage
- Export triggers download
- Search/filter real-time
- Sort by columns
- Print-friendly mode
- Keyboard shortcuts (Ctrl+S to save, Ctrl+E to export)

---

## Layout Switcher — Multiple Presentation Views

Users can switch between 6 different layout presentations via a layout selector in the header.

### Layout 1: Dashboard Grid (Default)
**Icon:** ◻◻◻◻
**Description:** Category-based grid with expandable cards

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │ 💰 Cash & Cash  │  │ 📈 Investments │  │ 🏠 Real Est│ │
│  │    (10 items)   │  │    (45 items)  │  │  (15 items)│ │
│  ├─────────────────┤  ├─────────────────┤  ├────────────┤ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌────────┐│ │
│  │ │ Chequing    │ │  │ │ TFSA        │ │  │ │ Primary││ │
│  │ │ TD Bank     │ │  │ │ Wealthsimple│ │  │ │ 123 St ││ │
│  │ │ $5,000      │ │  │ │ $85,000     │ │  │ │ $750K  ││ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └────────┘│ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌────────┐│ │
│  │ │ Savings     │ │  │ │ RRSP        │ │  │ │ Rental ││ │
│  │ │ EQ Bank     │ │  │ │ Questrade   │ │  │ │ 456 Ave││ │
│  │ │ $25,000     │ │  │ │ $120,000    │ │  │ │ $450K  ││ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └────────┘│ │
│  └─────────────────┘  └─────────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Layout 2: Table View
**Icon:** ☰
**Description:** Spreadsheet-like table with sortable columns

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│ Filter: [All Categories ▾]  Search: [________________] 🔍  │
├──────┬──────────────┬──────────┬──────────┬────────┬────────┤
│ ID   │ Asset Name   │ Category │ Owner    │ FMV    │ Status │
├──────┼──────────────┼──────────┼──────────┼────────┼────────┤
│ A-001│ TD Chequing  │ Cash     │ John     │ $5,000 │ ●      │
│ A-002│ EQ Savings   │ Cash     │ John     │$25,000 │ ●      │
│ A-003│ TFSA         │ Invest   │ John     │$85,000 │ ●      │
│ A-004│ RRSP         │ Invest   │ John     │$120,000│ ●      │
│ A-005│ Primary Home │ Real Est │ Joint    │$750,000│ ●      │
│ A-006│ Rental       │ Real Est │ Joint    │$450,000│ ●      │
│ ...  │ ...          │ ...      │ ...      │ ...    │ ...    │
├──────┴──────────────┴──────────┴──────────┴────────┴────────┤
│ ◀ 1 2 3 4 5 ... 52 ▶  │  Showing 1-10 of 515             │
└─────────────────────────────────────────────────────────────┘
```

### Layout 3: Kanban Board
**Icon:** ▮▮▮
**Description:** Status-based columns (Active, Dormant, Pending, Closed)

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ ● ACTIVE (342)│ │ ◐ DORMANT (45)│ │ ○ PENDING (28)│     │
│  ├──────────────┤ ├──────────────┤ ├──────────────┤       │
│  │ ┌──────────┐ │ │ ┌──────────┐ │ │ ┌──────────┐ │       │
│  │ │ TD Bank  │ │ │ │ Old RRSP │ │ │ │ Inheritance│ │     │
│  │ │ $5,000   │ │ │ │ $15,000  │ │ │ │ Pending   │ │     │
│  │ └──────────┘ │ │ └──────────┘ │ │ └──────────┘ │       │
│  │ ┌──────────┐ │ │ ┌──────────┐ │ │ ┌──────────┐ │       │
│  │ │ TFSA     │ │ │ │ Closed   │ │ │ │ Insurance │ │     │
│  │ │ $85,000  │ │ │ │ Account  │ │ │ │ Claim     │ │     │
│  │ └──────────┘ │ │ └──────────┘ │ │ └──────────┘ │       │
│  │ ┌──────────┐ │ │              │ │              │       │
│  │ │ RRSP     │ │ │              │ │              │       │
│  │ │ $120,000 │ │ │              │ │              │       │
│  │ └──────────┘ │ │              │ │              │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                             │
│  ┌──────────────┐                                          │
│  │ ✕ CLOSED (200)│                                         │
│  ├──────────────┤                                          │
│  │ ┌──────────┐ │                                          │
│  │ │ Old Acct │ │                                          │
│  │ └──────────┘ │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### Layout 4: Timeline View
**Icon:** ──●──
**Description:** Chronological view by date (open, maturity, review)

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│ View: [Open Date ▾]  Range: [2020 ──────── 2025]          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2020 ────────────────────────────────────────────────     │
│    │                                                        │
│    ├── Jan: TFSA opened (Wealthsimple)                      │
│    │        $7,000 initial                                  │
│    │                                                        │
│    ├── Mar: EQ Bank HISA opened                             │
│    │        $10,000 initial                                 │
│    │                                                        │
│  2021 ────────────────────────────────────────────────     │
│    │                                                        │
│    ├── Jan: RRSP opened (Questrade)                         │
│    │        $15,000 initial                                 │
│    │                                                        │
│    ├── Jun: Primary home purchased                          │
│    │        $750,000                                        │
│    │                                                        │
│  2022 ────────────────────────────────────────────────     │
│    │                                                        │
│    ├── Jan: RESP opened for child                           │
│    │        $2,500 + CESG $500                              │
│    │                                                        │
│  2025 ──── UPCOMING ──────────────────────────────────     │
│    │                                                        │
│    ├── Mar: GIC maturity (EQ Bank)                          │
│    │        $25,000 @ 4.0%                                  │
│    │                                                        │
│    ├── Jun: TFSA contribution room reset                    │
│    │        Room: $7,000                                    │
│    │                                                        │
│    ├── Dec: RRSP deadline                                  │
│    │        Contribution room: $15,000                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Layout 5: Detail View
**Icon:** ☰≡
**Description:** Single asset detailed view with all fields

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│ ◀ Previous │ A-003: TFSA │ Next ▶                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  TAX-FREE SAVINGS ACCOUNT (TFSA)                    │   │
│  │  Wealthsimple Trade                                  │   │
│  │  Status: ● Active    Priority: High                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ Ownership ──────────────┐  ┌─ Financial ─────────────┐ │
│  │ Owner:    John Smith     │  │ FMV:      $85,000.00    │ │
│  │ Joint:    -              │  │ ACB:      $72,000.00    │ │
│  │ Benef:    Spouse (100%)  │  │ Gain:     $13,000.00    │ │
│  │ Trust:    -              │  │ Tax:      Tax-free      │ │
│  └─────────────────────────┘  └─────────────────────────┘ │
│                                                             │
│  ┌─ Access ─────────────────┐  ┌─ Dates ─────────────────┐ │
│  │ URL:    wealthsimple.com │  │ Opened:   2020-01-15    │ │
│  │ User:   john@email.com  │  │ Review:   2025-06-30    │ │
│  │ Pass:   [***]           │  │ Maturity: -              │ │
│  │ 2FA:    Authenticator   │  │ Last Update: 2024-12-31 │ │
│  └─────────────────────────┘  └─────────────────────────┘ │
│                                                             │
│  ┌─ Tax & Registration ─────────────────────────────────┐ │
│  │ Contribution Room:  $65,000.00                       │ │
│  │ YTD Contributions: $6,500.00                         │ │
│  │ YTD Withdrawals:   $0.00                             │ │
│  │ CESG:              -                                 │ │
│  │ CLB:               -                                 │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─ Notes ──────────────────────────────────────────────┐ │
│  │ High-growth ETF portfolio. Rebalance annually.       │ │
│  │ Beneficiary designation on file.                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  [Edit] [Delete] [Print] [Export]                          │
└─────────────────────────────────────────────────────────────┘
```

### Layout 6: Compact/List View
**Icon:** ≡
**Description:** Minimal list with essential fields only

```
┌─────────────────────────────────────────────────────────────┐
│ [Dashboard] [Table] [Kanban] [Timeline] [Detail] [Compact] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ▼ Cash & Cash Equivalents (10)                             │
│    ● A-001  TD Chequing          TD Bank        $5,000     │
│    ● A-002  EQ Savings           EQ Bank       $25,000     │
│    ● A-003  Scotiabank Savings   Scotiabank    $10,000     │
│    ─────────────────────────────────────────────────────── │
│  ▼ Investments (45)                                         │
│    ● A-004  TFSA                 Wealthsimple  $85,000     │
│    ● A-005  RRSP                 Questrade    $120,000     │
│    ● A-006  RESP                 Questrade     $15,000     │
│    ● A-007  Non-reg Account      IBKR          $50,000     │
│    ─────────────────────────────────────────────────────── │
│  ▼ Real Estate (15)                                         │
│    ● A-008  Primary Residence    -            $750,000     │
│    ● A-009  Rental Property      -            $450,000     │
│    ─────────────────────────────────────────────────────── │
│  ▼ Cryptocurrency (41)                                      │
│    ● A-010  Bitcoin              Newton         $8,000     │
│    ● A-011  Ethereum             Shakepay       $4,000     │
│    ─────────────────────────────────────────────────────── │
│                                                             │
│  Total: 517 assets │ Value: $1,527,000                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Layout Switcher Implementation

### Header Controls
```
┌─────────────────────────────────────────────────────────────┐
│  📊 Asset Inventory Dashboard                              │
│                                                             │
│  ┌─Layout─┐ ┌─Theme─┐ ┌─Export─┐                          │
│  │◻◻◻◻    │ │ ☀/☾  │ │ ▼ MD   │                          │
│  │☰       │ │       │ │ ▼ XLSX │                          │
│  │▮▮▮     │ │       │ │ ▼ HTML │                          │
│  │──●──   │ │       │ │        │                          │
│  │☰≡      │ │       │ │        │                          │
│  │≡       │ │       │ │        │                          │
│  └────────┘ └───────┘ └────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### Layout State Persistence
- Current layout saved to localStorage
- Persists across sessions
- Reset option available

### Keyboard Shortcuts per Layout
| Shortcut | Dashboard | Table | Kanban | Timeline | Detail | Compact |
|----------|-----------|-------|--------|----------|--------|---------|
| Arrow keys | Navigate cards | Navigate cells | Navigate columns | Navigate timeline | Previous/Next asset | Navigate list |
| Enter | Open asset | Edit cell | Edit asset | Open asset | Edit mode | Expand details |
| Escape | Close asset | Cancel edit | Cancel | Back | Exit detail | Collapse |
| Space | Toggle card | Sort column | Move to next status | Toggle zoom | Toggle edit | Toggle expand |
| Tab | Next section | Next column | Next column | Next period | Next field | Next asset |

### Responsive Behavior
| Layout | Desktop | Tablet | Mobile |
|--------|---------|--------|--------|
| Dashboard | 3-column grid | 2-column grid | 1-column stack |
| Table | Full table | Horizontal scroll | Card view fallback |
| Kanban | 4 columns | 2 columns | Vertical stack |
| Timeline | Horizontal | Horizontal scroll | Vertical stack |
| Detail | Side panel | Full page | Full page |
| Compact | Full list | Full list | Full list |

**Self-Update Mechanism:**
- Save button generates new HTML
- Downloads updated HTML file
- Preserves all edits
- Maintains soft UI styling
- Single portable file

**Responsive Design:**
- Desktop: 3-column grid
- Tablet: 2-column grid
- Mobile: Single column, stacked

**Accessibility:**
- ARIA labels
- Keyboard navigation
- Focus indicators
- Screen reader friendly
