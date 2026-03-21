def run_research_pipeline():

    print("\nRunning research pipeline")

    scan_args = argparse.Namespace(
        scan="sp500",
        limit=50,
        window=6,
        crypto=args.crypto,
        parallel=False,
        report=False,
        ticker="SPY",
        top=20
    )

    run_scan_and_report(scan_args)

    evo_args = argparse.Namespace(ticker="SPY", window=12)
    run_evolution_search(evo_args)

    lab_args = argparse.Namespace(ticker="SPY", window=12, top=10, report=False)
    run_strategy_lab(lab_args)

