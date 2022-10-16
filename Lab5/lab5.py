"""
Course: CS-3860
Author: Nigel Nelson
Lab: 5
Date: 10/18/21
"""
import mysql.connector
import numpy as np
import itertools as iter


def simulation(cursor, ticker_allocations):
    """
    Simulates the results of the stock market if certain
    allocations are granted to specified stock ticker names
    :param cursor: SQLCursor instance
    :param ticker_allocations: Dictionary where the key is the ticker, and the
    value is the allocation of the portfolio out of 1.0
    :return: std, avg, sharpe ration, overall_return
    """
    allocation_sum = 0
    for key, value in ticker_allocations.items():
        if(value < 0):
            raise ValueError("Allocation must be greater than 0")
        allocation_sum += value
    if allocation_sum != 1:
        raise ValueError("Portfolio allocations must sum to be equal to 1")
    update_values(cursor, ticker_allocations)
    cumulative_portfolio_return(cursor)
    return calculate_sharpe(cursor)


def update_values(cursor, ticker_allocations):
    """
    Updates the values of given stocks in the connected database
    :param cursor: SQLCursor instance
    :param ticker_allocations: Dictionary where the key is the ticker, and the
    value is the allocation of the portfolio out of 1.0
    :return: N/A
    """
    for key, value in ticker_allocations.items():
        query = f"Update portfolio set {key}_value = {value}*{key}_cumulative_return;"
        cursor.execute(query)

    port_value_query = f"Update portfolio set portfolio_value = "
    for key, value in ticker_allocations.items():
        port_value_query += f"{key}_value +"
    cursor.execute(port_value_query[:-1])


def calculate_sharpe(cursor):
    """
    Calculates the standard deviation, average, overall return, and
    sharpe ration of the connected portfolio
    :param cursor: SQLCursor instance
    :return: std, avg, sharpe ration, overall_return
    """
    cursor.execute("select portfolio_cumulative_return from portfolio")
    cumulative_return = cursor.fetchall()
    cursor.execute("select spy_cumulative_return from portfolio")
    spy_cumulative_return = cursor.fetchall()

    avg = np.average(cumulative_return)
    std = np.std(cumulative_return)
    sharpe_avg = np.average(np.array(cumulative_return) - np.array(spy_cumulative_return))
    sharpe_std = np.std(np.array(cumulative_return) - np.array(spy_cumulative_return))
    sharpe = ((len(cumulative_return)**(1/2)) * sharpe_avg) / sharpe_std
    overall_return = (cumulative_return[-1][0] - cumulative_return[0][0]) / cumulative_return[0][0]
    return std, avg, sharpe, overall_return


def cumulative_portfolio_return(cursor):
    """
    Updates the connected portfolio's portfolio_cumulative_return attribute
    :param cursor: SQLCursor instance
    :return: N/A
    """
    value_query = "update portfolio set portfolio_cumulative_return = portfolio_value/1"
    cursor.execute(value_query)


def optimization(cursor, ticker_names):
    """
    Finds the allocations out of 1 for the provided ticker_names that
    results in the highest Sharpe ratio
    :param cursor: SQLCursor instance
    :param ticker_names: List of ticker names
    :return: Dictionary with highest Sharpe Ratio where the key is the ticker,
     and the value is the allocation of the portfolio out of 1.0 as well as a
     list of the resulting std, avg, sharpe ration, and overall_return
    """
    combinations = np.array(list(iter.product(range(0, 11), repeat=4)))/10
    mask = np.sum(combinations, axis=1) == 1
    combinations = combinations[mask]

    max_sharpe = 0
    ticker_allocations = {}
    best_allocations = {}

    for comb in combinations:
        for i in range(0, 4):
            ticker_allocations[ticker_names[i]] = comb[i]
        results = simulation(cursor, ticker_allocations)
        if results[2] > max_sharpe:
            max_sharpe = results[2]
            best_allocations = ticker_allocations.copy()

    return best_allocations, simulation(cursor, best_allocations)


def main():
    connect = mysql.connector.connect(host="localhost", user="root", password="Frohfosho01)",
                                      database="data_analytics_2020", autocommit=True)
    cursor = connect.cursor()

    ticker_allocations = {
        "goog": 0.0,
        "celg": 0.9,
        "nvda": 0.1,
        "fb": 0.0
    }

    results = simulation(cursor, ticker_allocations)
    print("Weights used: " + str(ticker_allocations))
    print("Daily Returns Standard Deviation: " + str(results[0]))
    print("Daily Returns Average: " + str(results[1]))
    print("Sharpe Ratio: " + str(results[2]))
    print("Overall Return: " + str(results[3]))

    results = optimization(cursor, ["goog", "celg", "nvda", "fb"])
    print("Weights used: " + str(results[0]))
    print("Daily Returns Standard Deviation: " + str(results[1][0]))
    print("Daily Returns Average: " + str(results[1][1]))
    print("Sharpe Ratio: " + str(results[1][2]))
    print("Overall Return: " + str(results[1][3]))

if __name__ == "__main__":
    main()
