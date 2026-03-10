def print_market(prices):

    print("MARKET")
    print("------")

    for t, p in prices.items():

        if p is None:
            print(f"{t:<6} data")

        else:
            print(f"{t:<6} {p:8.2f}")


def print_signals(pending, confirmed):

    print("\nPENDING SIGNALS")
    print("----------------")

    if not pending:
        print("None")

    for ticker, signal, votes, count in pending:
        print(f"{ticker:<6} {signal:<4} votes:{votes} confirm:{count}")

    print("\nCONFIRMED SIGNALS")
    print("-----------------")

    if not confirmed:
        print("None")

    for ticker, signal, votes in confirmed:
        print(f"{ticker:<6} {signal:<4} votes:{votes}")
