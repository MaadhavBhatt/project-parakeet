import csv


def read_csv(
    filepath: str, headers: list[str] | None | object = None, verbose: bool = True
) -> list[dict[str, float]]:
    """
    Reads a CSV file and returns a list of dictionaries containing the data.

    Args:
        filepath (str): Path to the CSV file.
        headers (list[str] | None): List of headers to use for the dictionary keys. If None, the first row of the CSV is used as headers.
        verbose (bool): If True, prints messages about skipped rows and other information.

    Returns:
        list[dict[str, float]]: List of dictionaries, where each dictionary contains the data from a row in the CSV.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If there are issues with converting values to float.

    Notes:
        - Rows that don't have the expected number of values are skipped.
        - Values that can't be converted to float are skipped.
        - Empty files return an empty list.
    """
    pitch_data: list[dict[str, float]] = []

    try:
        with open(filepath, "r", newline="") as file:
            csv_reader = csv.reader(file)

            # Check if the first row is a header
            try:
                header = next(csv_reader)
                has_header = headers is not None or len(header) > 0
                if has_header:
                    # If headers are provided, use them; otherwise, use the first row as headers
                    if headers is None:
                        headers = header
                    else:
                        assert isinstance(
                            headers, list
                        ), "Headers must be a list of strings."
                        # Ensure the provided headers match the CSV file's headers
                        if len(headers) != len(header):
                            raise ValueError(
                                "Provided headers do not match the number of columns in the CSV file."
                            )
            except StopIteration:
                return pitch_data  # Empty file

            assert isinstance(headers, list), "Headers must be a list of strings."

            for row in csv_reader:
                if len(row) == len(headers):
                    try:
                        # Create a dictionary using the provided or detected headers
                        row_dict = {
                            headers[i]: float(row[i]) for i in range(len(headers))
                        }
                        pitch_data.append(row_dict)
                    except ValueError as e:
                        if verbose:
                            print(f"Skipping row {row} due to error: {e}")
                else:
                    if verbose:
                        print(
                            f"Skipping row {row} due to unexpected number of values. Expected {len(headers)}, got {len(row)}."
                        )

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e

    return pitch_data
