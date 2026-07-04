# User Flows

This document maps out the specific flows users take through the ShopSense AI platform. 

*(Note: Mermaid syntax is used below for flow generation. These can be visualized in any Mermaid-compatible Markdown viewer).*

## 1. Guest User Flow
```mermaid
graph TD
    A[Landing Page] --> B{Action}
    B -->|Search| C[Search Results]
    B -->|Browse| D[Category Page]
    C --> E[Product Details Page]
    D --> E
    E --> F{Decision}
    F -->|Buy| G[Redirect to Merchant]
    F -->|Save/Alert| H[Prompt Login/Signup]
```

## 2. Registered User / Returning User Flow
```mermaid
graph TD
    A[Homepage - Personalized] --> B[View Saved Alerts/Wishlist]
    A --> C[Search New Product]
    B --> D{Price Dropped?}
    D -->|Yes| E[Click Buy -> Merchant]
    D -->|No| F[Keep Waiting]
    C --> G[Product Details]
    G --> H[Add to Compare]
    H --> I[Comparison Page]
    I --> E
```

## 3. Search & AI Chat Flow
```mermaid
graph TD
    A[Search Bar] --> B[Type Query]
    B --> C[Auto-Suggest/Typo Correction]
    C --> D[Results Grid]
    D --> E[Filter & Sort]
    E --> F[Open Product]
    F --> G[Click 'Ask AI']
    G --> H[AI Chat Window Opens]
    H --> I[User Asks Question]
    I --> J[AI Responds with Context]
    J --> K{Helpful?}
    K -->|Yes| L[User Buys]
    K -->|No| M[User Asks Another Question]
```

## 4. Affiliate Click & Coupon Flow
```mermaid
graph TD
    A[Product Page] --> B[View Offers Section]
    B --> C[Copy Coupon Code]
    C --> D[Click 'Go to Store']
    D --> E[Transition Screen: 'Redirecting...']
    E --> F[Backend Logs Click Analytics]
    F --> G[302 Redirect via Affiliate Link]
    G --> H[Merchant Site Opens]
    H --> I[User Applies Coupon & Buys]
```

## 5. Price Alert Flow
```mermaid
graph TD
    A[Product Page] --> B[Click 'Set Alert']
    B --> C{Logged In?}
    C -->|No| D[Login Modal]
    D --> E[Set Target Price]
    C -->|Yes| E
    E --> F[Backend Saves Alert]
    F --> G[Cron Job Checks Prices Daily]
    G --> H{Current <= Target?}
    H -->|Yes| I[Send Email/Push Notification]
    H -->|No| J[Wait for Next Check]
    I --> K[User Clicks Email Link -> Merchant]
```

## 6. Admin Flow
```mermaid
graph TD
    A[Admin Login] --> B[Dashboard]
    B --> C[View Key Metrics CTR, Users]
    B --> D[Manage Blog Posts]
    B --> E[Manage API Keys / Affiliate Tags]
    B --> F[Monitor Scraper/Ingestion Health]
    B --> G[Flagged/Broken Links Report]
```

## 7. Account Settings & Wishlist Flow
```mermaid
graph TD
    A[User Profile] --> B[Account Details]
    A --> C[Manage Wishlist]
    A --> D[Manage Price Alerts]
    C --> E[Remove Item]
    D --> F[Edit Target Price / Delete Alert]
    B --> G[Change Password / Theme Preference]
```
