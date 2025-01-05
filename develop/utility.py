class InputValidation:
    @staticmethod
    def assert_input_within_allowable_range(input_argument, min_value, max_value, input_variable_name):
        if input_argument < min_value or input_argument > max_value:
            raise ValueError(f'{input_variable_name}, ({input_argument}) is not within allowable bounds. '
                             f'Minimum value accepted = {min_value}, maximum value accepted = {max_value}')
