from src.logic.access_stock_performance import access_data_as_dataframe


if __name__ == "__main__":

    code = 8045

    df = access_data_as_dataframe(code=code)
