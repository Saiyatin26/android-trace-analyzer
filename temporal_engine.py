import sqlite3

DB_NAME = "events.db"


# =========================================================
# FETCH EVENTS ORDERED BY TIME
# =========================================================

def fetch_all_events():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        timestamp,
        duration_ms,
        event_type,
        binder_name
    FROM events
    ORDER BY timestamp ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# BUILD TEMPORAL EVENT CHAINS
# =========================================================

def build_event_chains():

    events = fetch_all_events()

    chains = []

    current_chain = []

    previous_timestamp = None

    # Threshold:
    # events within 50ms are grouped together
    threshold_ns = 50_000_000

    for event in events:

        timestamp = event[0]

        if previous_timestamp is None:

            current_chain.append(event)

        else:

            difference = timestamp - previous_timestamp

            if difference <= threshold_ns:

                current_chain.append(event)

            else:

                chains.append(current_chain)

                current_chain = [event]

        previous_timestamp = timestamp

    # Add final chain
    if current_chain:
        chains.append(current_chain)

    return chains


# =========================================================
# GENERATE HUMAN-READABLE INSIGHTS
# =========================================================

def generate_temporal_insights(chains):

    insights = []

    for index, chain in enumerate(chains):

        event_types = []

        for event in chain:

            event_types.append(event[2])

        insight = {
            "chain_id": index + 1,
            "events": event_types
        }

        insights.append(insight)

    return insights