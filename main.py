import os
from quixstreams import Application  # type: ignore
from datetime import timedelta

# Environment variables and constants
WINDOW_SECONDS = 10  

# Reducer function
def reduce_price(accumulator, current_row):
    return accumulator + current_row["price"]

# Initializer for reduce
init_reduce_price = 0

# Application setup
app = Application(
    broker_address=os.environ["KAFKA_BROKER_ADDRESS"],
    consumer_group="feature-engineer_consumer-group"
)

input_topic = app.topic('trades', value_deserializer="json")
output_topic = app.topic('engineer_features', value_deserializer="json")

# Create your streaming data frame
sdf = app.dataframe(input_topic)

# 10-second window aggregation
sdf = sdf.tumbling_window(timedelta(seconds=WINDOW_SECONDS), 0).reduce(reduce_price, init_reduce_price).final()
sdf = sdf.to_topic(output_topic)

app.run(sdf)
