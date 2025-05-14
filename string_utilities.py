def conditioner(filter_type, comparison_string, target_string, num_words):
    # Split the strings into words
    comparison_words = comparison_string.split(" ")
    target_words = target_string.split(" ")

    if filter_type == 1:  # Check if the first 'num_words' words match
        start_part = " ".join(comparison_words[:num_words])
        if start_part == " ".join(target_words[:num_words]):
            return "true"
        else:
            return "false"

    elif filter_type == 2:  # Check if any word from target_string exists in comparison_string
        count = sum(1 for word in target_words if word in comparison_words)
        return "true" if count > 0 else "false"

    elif filter_type == 3:  # Check if the last 'num_words' words match
        end_part = " ".join(comparison_words[-num_words:])
        if end_part == " ".join(target_words[-num_words:]):
            return "true"
        else:
            return "false"

    return "false"  # Default case (should not happen with valid inputs)


def nom(number_str):
    number_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }

    # Check if the input is a valid integer in string form
    try:
        return int(number_str)
    except ValueError:
        pass  # If it can't be converted, fall through to the word lookup

    # Return the corresponding number for word input
    return number_map.get(number_str.lower(), -1)  # Return -1 if the word is not recognized
