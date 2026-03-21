def print_strategy_performance(
    ma_equity, mr_equity, adaptive_equity,
    ma_final, mr_final, adaptive_final,
    ma_sharpe, mr_sharpe, adaptive_sharpe,
    ma_max_dd, mr_max_dd, adaptive_max_dd,
    ma_profits, mr_profits, ad_profits,
    vote_final, vote_sharpe,
    council_final, council_sharpe,
    bh_final, bh_sharpe, bh_max_dd,
    ticker,
    record_trade,
    log_trade,
    print_strategy_stats
):

    print("\nSTRATEGY PERFORMANCE")
    print("--------------------------------------------")

    strategy_table = [
        ("MA", ma_final, ma_sharpe, ma_max_dd),
        ("MR", mr_final, mr_sharpe, mr_max_dd),
        ("Adaptive", adaptive_final, adaptive_sharpe, adaptive_max_dd),
        ("Vote", vote_final, vote_sharpe, 0),
        ("Council", council_final, council_sharpe, 0),
        ("BuyHold", bh_final, bh_sharpe, bh_max_dd),
    ]

    strategy_table.sort(key=lambda x: x[2], reverse=True)

    print(f"{'Strategy':<12}{'Final':>12}{'Sharpe':>10}{'MaxDD':>10}")

    for name, final, sharpe, dd in strategy_table:
        print(f"{name:<12}{final:>12.2f}{sharpe:>10.2f}{dd * 100:>9.2f}%")

    # record trades

    for p in ma_profits:
        record_trade("MA", p)
        log_trade(ticker, "TRADE", 1, p, "MA", 0, ma_final)

    for p in ad_profits:
        record_trade("AD", p)
        log_trade(ticker, "TRADE", 1, p, "AD", 0, adaptive_final)

    for p in mr_profits:
        record_trade("MR", p)
        log_trade(ticker, "TRADE", 1, p, "MR", 0, mr_final)

    print_strategy_stats()
