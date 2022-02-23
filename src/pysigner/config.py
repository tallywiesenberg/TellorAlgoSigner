def get_configs(args: List[str]) -> Box:
    """get all signer configurations from passed flags or yaml file"""

    # read in configurations from yaml file
    with open("config.yml") as ymlfile:
        config = yaml.safe_load(ymlfile)

    # parse command line flags & arguments
    parser = argparse.ArgumentParser(description="Submit values to Tellor Mesosphere")
    parser.add_argument(
        "-n",
        "--network",
        nargs=1,
        required=False,
        type=str,
        help="An EVM compatible network.",
    )
    parser.add_argument(
        "-gp",
        "--gasprice",
        nargs=1,
        required=False,
        type=str,
        help="The gas price used for transactions. If no gas price is set, it is retrieved from https://gasstation-mainnet.matic.network.",
    )
    parser.add_argument(
        "-egp",
        "--error-gasprice",
        nargs=1,
        required=False,
        type=float,
        help="Extra gwei added to gas price if gas price too low.",
    )
    parser.add_argument(
        "-pk",
        "--private-key",
        nargs=1,
        required=False,
        type=str,
        help="an ethereum private key",
    )

    # get dict of parsed args
    cli_cfg = vars(parser.parse_args(args))

    # overwrite any configs from yaml file also given by user via cli
    for flag, arg in cli_cfg.items():
        if arg != None:
            config[flag] = arg[0]

    # enable dot notation for accessing configs
    config = Box(config)

    return config