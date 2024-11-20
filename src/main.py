import numpy as np
import pandas as pd

# Parameters
NUM_STATES = 32  # Number of states in Mexico
NUM_POLLS = 100  # Number of polls to generate
CANDIDATES = ["Candidate A", "Candidate B"]

# Generate Random Polling Data
def generate_polling_data(num_states, num_polls, candidates):
    """
    Simulates random polling data for multiple states and candidates.
    """
    np.random.seed(42)
    states = [f"State_{i+1}" for i in range(num_states)]
    data = []
    
    for _ in range(num_polls):
        poll_id = f"Poll_{np.random.randint(1000, 9999)}"
        state = np.random.choice(states)
        sample_size = np.random.randint(500, 2000)
        date = pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30))
        
        # Generate random support percentages for candidates
        support = np.random.dirichlet(np.ones(len(candidates))) * 100
        undecided = max(0, 100 - sum(support))
        
        data.append({
            "Poll ID": poll_id,
            "State": state,
            "Sample Size": sample_size,
            "Date": date,
            **{f"{cand} Support (%)": s for cand, s in zip(candidates, support)},
            "Undecided (%)": undecided
        })
    
    return pd.DataFrame(data)

# Adjust Polls
def adjust_polls(df):
    """
    Applies basic adjustments to the polling data:
    1. Recency Adjustment: Weight polls based on how recent they are.
    2. Sample Size Adjustment: Weight polls based on sample size.
    """
    now = pd.Timestamp.now()
    df["Days Ago"] = (now - df["Date"]).dt.days
    df["Recency Weight"] = 1 / (1 + df["Days Ago"])
    df["Sample Weight"] = df["Sample Size"] / df["Sample Size"].max()
    df["Total Weight"] = df["Recency Weight"] * df["Sample Weight"]
    
    # Weighted averages for each state
    adjusted_polls = (
        df.groupby("State")
        .apply(lambda group: pd.Series({
            cand: np.average(group[f"{cand} Support (%)"], weights=group["Total Weight"])
            for cand in CANDIDATES
        }))
        .reset_index()
    )
    return adjusted_polls

# Main Execution
if __name__ == "__main__":
    # Step 1: Generate random polling data
    print("Generating random polling data...")
    polling_data = generate_polling_data(NUM_STATES, NUM_POLLS, CANDIDATES)
    print(polling_data.head())

    # Step 2: Adjust polling data
    print("\nAdjusting polls...")
    adjusted_data = adjust_polls(polling_data)
    print(adjusted_data.head())