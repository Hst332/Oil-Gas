#!/usr/bin/env python3

from gas_forecast import run_gas_forecast
from oil_forecast import run_oil_forecast

OUTPUT = "forecast_combined.txt"


def main():
    gas = run_gas_forecast()
    oil = run_oil_forecast()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("===================================\n")
        f.write("   COMBINED ENERGY FORECAST – CODE A\n")
        f.write("===================================\n\n")

        for r in (gas, oil):
            f.write(f"{r['section']}\n")
            f.write("-----------------------------------\n")
            f.write(f"Run time (UTC): {r['run_time']}\n")
            f.write(f"Data date     : {r['data_date']}\n\n")
            f.write(f"Prob UP       : {r['prob_up']:.2%}\n")
            f.write(f"Prob DOWN     : {r['prob_down']:.2%}\n")
            f.write(f"Signal        : {r['signal']}\n\n")

        f.write("===================================\n")

    print("[OK] forecast_combined.txt created")


if __name__ == "__main__":
    main()
