from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import ProcessFunction, RuntimeContext
from pyflink.common.typeinfo import Types
import json

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

    data_stream = env.from_collection(
        [
            '{"timestamp": 1622548800, "heart_rate": 75}',
            '{"timestamp": 1622548810, "heart_rate": 76}',
            '{"timestamp": 1622548820, "heart_rate": 77}'
        ],
        type_info=Types.STRING()
    )

    processed_stream = data_stream.process(PreprocessFunction(), output_type=Types.STRING())

    processed_stream.print()

    env.execute("Real-Time Processing Job")

if __name__ == '__main__':
    main()
