def encryp(method, message):
    # Define the character mappings for encryption and decryption
    source_chars = "123ABCDEFGHIJ4567890KLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^&*()_-+=[];',|:<>."
    target_chars = "<IemS)_9^DxXd6Z3|fVp8aF&2'~-5$k[QWP(*w?,>%KqCilOYT]MsJ!:u=tGvRoH4ghj+10U@zcAbE;7nrLy#NB"

    # Determine direction of transformation based on method
    if method == "enc":
        from_chars = source_chars
        to_chars = target_chars
    elif method == "dec":
        from_chars = target_chars
        to_chars = source_chars
    else:
        raise ValueError("Method must be 'enc' for encryption or 'dec' for decryption")

    # Split message into words
    words = message.split(" ")
    transformed_words = []

    # Process each word
    for word in words:
        transformed_word = ""
        for char in word:
            if char in from_chars:
                index = from_chars.index(char)
                transformed_word += to_chars[index]
            else:
                # If character not found in mapping, leave it as is
                transformed_word += char
        transformed_words.append(transformed_word)

    # Join transformed words with spaces
    result = " ".join(transformed_words)
    return result
