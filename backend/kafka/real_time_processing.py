# real_time_processing.py
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import ProcessFunction
from pyflink.common.typeinfo import Types
import json
import logging
from backend.thingspeak import read_from_thingspeak

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PreprocessFunction(ProcessFunction):

    def process_element(self, value, ctx: 'ProcessFunction.Context'):
        data = json.loads(value)
        timestamp = data['timestamp']
        heart_rate = data['heart_rate']

        # Calculate HRV, rolling averages, etc. (simplified example)
        hrv = heart_rate / 2  # Replace with actual HRV calculation
        rolling_mean = heart_rate  # Replace with actual rolling mean calculation
        rolling_std = heart_rate / 3  # Replace with actual rolling std calculation

        processed_data = json.dumps({
            'timestamp': timestamp,
            'heart_rate': heart_rate,
            'hrv': hrv,
            'rolling_mean': rolling_mean,
            'rolling_std': rolling_std
        })

        yield processed_data

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # Fetch data from ThingSpeak
    data = read_from_thingspeak()

    if data:
        # Convert the data to the format expected by the stream
        data_stream = env.from_collection(
            [json.dumps(record) for record in data],
            type_info=Types.STRING()
        )

        processed_stream = data_stream.process(PreprocessFunction(), output_type=Types.STRING())

        processed_stream.print()

        env.execute("Real-Time Processing Job")
    else:
        logger.error("No data retrieved from ThingSpeak.")

if __name__ == '__main__':
    main()
