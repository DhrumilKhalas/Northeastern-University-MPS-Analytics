# ============================================================
# MODULE 6 FINAL PROJECT
# Temporal Churn Prediction Dataset Generator
# Business: Fitness Subscription App ("FitPulse")
# ============================================================

import numpy as np
import pandas as pd
import random

# -----------------------------
# Reproducibility
# -----------------------------
np.random.seed(42)
random.seed(42)

# ============================================================
# 1. BASIC SETTINGS
# ============================================================

NUM_USERS = 5000
NUM_WEEKS = 52
CHURN_RATE = 0.22

# Weekly timeline
weeks = pd.date_range(
    start="2025-01-06",
    periods=NUM_WEEKS,
    freq="W-MON"
)

# ============================================================
# 2. CREATE USERS
# ============================================================

users = pd.DataFrame({
    "user_id": [f"U{i:05d}" for i in range(1, NUM_USERS + 1)],
    
    # Subscription type
    "subscription_plan": np.random.choice(
        ["Basic", "Premium"],
        size=NUM_USERS,
        p=[0.7, 0.3]
    ),
    
    # Age group
    "age_group": np.random.choice(
        ["18-25", "26-35", "36-50", "50+"],
        size=NUM_USERS,
        p=[0.30, 0.40, 0.22, 0.08]
    )
})

# ============================================================
# 3. RANDOMLY SELECT CHURN USERS
# ============================================================

num_churners = int(NUM_USERS * CHURN_RATE)

churn_users = set(
    np.random.choice(
        users["user_id"],
        size=num_churners,
        replace=False
    )
)

# ============================================================
# 4. GENERATE TEMPORAL USER ACTIVITY
# ============================================================

records = []

for _, row in users.iterrows():
    
    user_id = row["user_id"]
    plan = row["subscription_plan"]
    age_group = row["age_group"]
    
    # Is this user a churner?
    is_churner = user_id in churn_users
    
    # Random churn week
    # Churn happens later in the year
    churn_week = None
    
    if is_churner:
        churn_week = random.randint(20, 50)
    
    # -----------------------------
    # Baseline behavior
    # -----------------------------
    
    if plan == "Premium":
        base_sessions = np.random.randint(10, 16)
        base_workouts = np.random.randint(4, 7)
    else:
        base_sessions = np.random.randint(6, 12)
        base_workouts = np.random.randint(2, 5)
    
    streak = np.random.randint(5, 25)
    
    # ========================================================
    # WEEKLY RECORDS
    # ========================================================
    
    for week_num, current_week in enumerate(weeks):
        
        # -----------------------------
        # Default Stable Behavior
        # -----------------------------
        
        sessions = max(
            0,
            int(np.random.normal(base_sessions, 2))
        )
        
        workouts = max(
            0,
            int(np.random.normal(base_workouts, 1))
        )
        
        avg_session_minutes = round(
            np.random.normal(35, 8),
            1
        )
        
        # ====================================================
        # CHURN DECLINE LOGIC
        # ====================================================
        
        if is_churner and week_num >= churn_week - 8:
            
            # Gradual engagement decline
            decline_factor = week_num - (churn_week - 8)
            
            sessions = max(
                0,
                sessions - decline_factor
            )
            
            workouts = max(
                0,
                workouts - int(decline_factor * 0.7)
            )
            
            avg_session_minutes = max(
                5,
                avg_session_minutes - (decline_factor * 2)
            )
            
            streak = max(
                0,
                streak - (decline_factor * 3)
            )
        
        else:
            # Healthy users maintain streak
            streak = max(
                0,
                streak + np.random.randint(-2, 3)
            )
        
        # ====================================================
        # ADDITIONAL FEATURES
        # ====================================================
        
        # Payment failures increase near churn
        if is_churner and week_num >= churn_week - 4:
            payment_failures = np.random.choice(
                [0, 1, 2],
                p=[0.55, 0.35, 0.10]
            )
        else:
            payment_failures = np.random.choice(
                [0, 1],
                p=[0.95, 0.05]
            )
        
        # Support tickets
        if is_churner and week_num >= churn_week - 6:
            support_tickets = np.random.choice(
                [0, 1, 2],
                p=[0.60, 0.30, 0.10]
            )
        else:
            support_tickets = np.random.choice(
                [0, 1],
                p=[0.88, 0.12]
            )
        
        # Push notification clicks
        push_clicks = max(
            0,
            int(np.random.normal(sessions * 0.5, 2))
        )
        
        # Days since last workout
        if workouts == 0:
            days_since_last_workout = np.random.randint(10, 31)
        else:
            days_since_last_workout = np.random.randint(0, 7)
        
        # ====================================================
        # TARGET VARIABLE
        # ====================================================
        
        churn_next_8_weeks = 0
        
        # Label weeks close to churn
        if is_churner:
            # if churn_week - 4 <= week_num < churn_week:
            if churn_week - 8 <= week_num < churn_week:
                churn_next_8_weeks = 1
        
        # ====================================================
        # SAVE RECORD
        # ====================================================
        
        records.append({
            "user_id": user_id,
            "week_date": current_week,
            "week_number": week_num + 1,
            "subscription_plan": plan,
            "age_group": age_group,
            "app_sessions": sessions,
            "workouts_completed": workouts,
            "avg_session_minutes": round(avg_session_minutes, 1),
            "streak_days": streak,
            "payment_failures": payment_failures,
            "support_tickets": support_tickets,
            "push_notification_clicks": push_clicks,
            "days_since_last_workout": days_since_last_workout,
            "churn_next_8_weeks": churn_next_8_weeks
        })

# ============================================================
# 5. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(records)

# ============================================================
# 6. SORT DATA
# ============================================================

df = df.sort_values(
    by=["user_id", "week_date"]
).reset_index(drop=True)

# ============================================================
# 7. TEMPORAL FEATURE ENGINEERING
# ============================================================

# Rolling averages
df["sessions_last_4_weeks"] = (
    df.groupby("user_id")["app_sessions"]
      .transform(lambda x: x.rolling(4, min_periods=1).mean())
)

df["workouts_last_4_weeks"] = (
    df.groupby("user_id")["workouts_completed"]
      .transform(lambda x: x.rolling(4, min_periods=1).mean())
)

# Trend feature
df["session_trend"] = (
    df.groupby("user_id")["app_sessions"]
      .diff()
      .fillna(0)
)

# Active weeks frequency
df["active_weeks_last_8"] = (
    df.groupby("user_id")["workouts_completed"]
      .transform(
          lambda x: (
              x.rolling(8, min_periods=1)
               .apply(lambda y: np.sum(y > 0))
          )
      )
)

# ============================================================
# 8. ADD REALISTIC MISSINGNESS
# ============================================================

# Introduce some missing values
missing_mask = np.random.rand(len(df)) < 0.02

df.loc[missing_mask, "avg_session_minutes"] = np.nan

# ============================================================
# FIX NEGATIVE SESSION MINUTES
# ============================================================

df["avg_session_minutes"] = (
    df["avg_session_minutes"]
    .clip(lower=1)
)

# ============================================================
# 9. DATASET SUMMARY
# ============================================================

print("=" * 60)
print("TEMPORAL CHURN DATASET CREATED")
print("=" * 60)

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")
print(f"Unique Users: {df['user_id'].nunique():,}")

print("\nChurn Distribution:")
print(df["churn_next_8_weeks"].value_counts())

print("\nSample Data:")
print(df.head())

# ============================================================
# 10. SAVE DATASET
# ============================================================

df.to_csv(
    "fitness_temporal_churn_dataset.csv",
    index=False
)

print("\nDataset saved as:")
print("fitness_temporal_churn_dataset.csv")
 