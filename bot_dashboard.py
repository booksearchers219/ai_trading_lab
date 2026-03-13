import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# find equity logs
files = glob.glob("equity_log_*.csv")

if not files:
    print("No equity logs found.")
    exit()

# load all logs
data = []

for f in files:
    bot = f.replace("equity_log_", "").replace(".csv", "")
    df = pd.read_csv(f)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bot"] = bot
    df["equity"] = df["MA"] + df["MR"] + df["AD"]
    data.append(df)

df = pd.concat(data)

# compute drawdown
df["peak"] = df.groupby("bot")["equity"].cummax()
df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]

# final stats
stats = df.groupby("bot").agg(
    final_equity=("equity","last"),
    max_drawdown=("drawdown","min")
)

# create figure
fig, axes = plt.subplots(2,2, figsize=(14,10))

ax1, ax2, ax3, ax4 = axes.flatten()

# ------------------------
# Equity Curve
# ------------------------

for bot, g in df.groupby("bot"):
    ax1.plot(g["timestamp"], g["equity"], label=bot)

ax1.set_title("Equity Curve")
ax1.legend()
ax1.grid(True)

# ------------------------
# Drawdown
# ------------------------

for bot, g in df.groupby("bot"):
    ax2.plot(g["timestamp"], g["drawdown"], label=bot)

ax2.set_title("Drawdown")
ax2.legend()
ax2.grid(True)

# ------------------------
# Histogram of returns
# ------------------------

returns = df.groupby("bot")["equity"].pct_change().dropna()

ax3.hist(returns, bins=40)

ax3.set_title("Return Distribution")
ax3.grid(True)

# ------------------------
# Strategy comparison
# ------------------------

stats["final_equity"].plot(kind="bar", ax=ax4)

ax4.set_title("Final Equity by Strategy")
ax4.grid(True)

plt.tight_layout()

plt.savefig("bot_dashboard.png", dpi=300)

print("Dashboard saved to bot_dashboard.png")
