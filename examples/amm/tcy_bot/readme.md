# Guide

### Installation

First, install Python 3.9 or higher. Then, create a virtual environment and activate it:

```shell
python3 -m venv venv
source venv/bin/activate
```

Next, install the required packages:

```shell
pip install -r requirements.txt
```

### Configuration

Copy `example.tcy_bot_config.yaml` to `tcy_bot_config.yaml` and fill in the required fields. The configuration file
should look like this:

```yaml
# tcy_bot_config.yaml
thor:
  node_url: "https://thornode.ninerealms.com/"
  midgard_url: "https://midgard.ninerealms.com/"
  phrase: "your twelve word seed phrase goes here"
  network_id: "mainnet"

strategy:
  source_amount: 100   # change this to the amount you want to swap
  source_asset: "THOR.RUNE"  # change this to the asset you want to swap from
  target_asset: "THOR.TCY"

  check_interval: 1  # in seconds
```

### Running the Bot

To run the bot, execute the following command:

```shell
python tcy_bot.py
```

Or if you want to specify a different configuration file, use:

```shell
python tcy_bot.py your_config_file.yaml
```

_ToDo: update this doc_