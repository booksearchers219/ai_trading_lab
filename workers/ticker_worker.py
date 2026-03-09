from backtest_utils import run_backtest, calculate_sharpe
from strategies import analyze_market, mean_reversion_strategy, adaptive_strategy, detect_regime


def process_ticker(args):

    ticker, data = args

    try:

        if data is None or len(data) < 50:
            return None

        regime = detect_regime(data)

        ma_equity, ma_final, _, _, _ = run_backtest(data, analyze_market)
        mr_equity, mr_final, _, _, _ = run_backtest(data, mean_reversion_strategy)
        ad_equity, ad_final, _, _, _ = run_backtest(data, adaptive_strategy)

        ma_sharpe = calculate_sharpe(ma_equity)
        mr_sharpe = calculate_sharpe(mr_equity)
        ad_sharpe = calculate_sharpe(ad_equity)

        return (
            ticker,
            regime,
            ma_final,
            mr_final,
            ad_final,
            ma_sharpe,
            mr_sharpe,
            ad_sharpe,
            ma_equity,
            mr_equity,
            ad_equity
        )

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None
