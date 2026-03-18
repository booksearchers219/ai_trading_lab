


RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"



def print_market(prices, crypto=False):

    if crypto:
        print(CYAN + "\nCRYPTO MARKET (24/7)" + RESET)
    else:
        print(CYAN + "\nMARKET" + RESET)

    print("------")

    items = list(prices.items())
    cols = 5   # number of tickers per row

    for i in range(0, len(items), cols):

        row = items[i:i+cols]

        line = ""

        for t, p in row:

            if p is None:
                line += f"{t:<8} data     "
            else:
                line += f"{t:<8} {p:>8.2f}  "

        print(line)




def print_signals(pending, confirmed):

    print("\nPENDING SIGNALS")
    print("----------------")

    if not pending:
        print("None")

    for ticker, signal, votes, count in pending:

        if signal == "BUY":
            color = GREEN
        elif signal == "SELL":
            color = RED
        else:
            color = YELLOW

        print(f"{ticker:<6} {color}{signal:<4}{RESET} votes:{votes} confirm:{count}")

    # SORT CONFIRMED SIGNALS BY VOTE STRENGTH
    confirmed = sorted(confirmed, key=lambda x: x[2], reverse=True)

    print("\nCONFIRMED SIGNALS")
    print("-----------------")

    if not confirmed:
        print("None")

    for ticker, signal, votes in confirmed:

        if signal == "BUY":
            color = GREEN
        elif signal == "SELL":
            color = RED
        else:
            color = YELLOW

        print(f"{ticker:<6} {color}{signal:<4}{RESET} votes:{votes}")
