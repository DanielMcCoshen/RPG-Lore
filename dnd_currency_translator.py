#! /usr/bin/env python3

import re
import sys
import getopt


def show_help():
    print(f"""Convert from one type of D&D currency to another.
Usage: {sys.argv[0]} [OPTIONS]

Options to arguments are mandatory:
  -h, --help      Display this help message
  -i, --in TYPE   Set the input currency type of the script. The type must be
                    one of the supported currency types. The default input type
                    is standard.
  -o, --out TYPE  Set the output currency type of the script. the type must be
                    one of the supported currency types. The default output type
                    is durekian

Supported Types:
  standard  This is the standard Dungeons and Dragons currency in copper (c),
              siver (s), electrum (e), gold (g), and platnum (p). It is
              normalized against copper as the smallest value.
  durekian  This is the currency used in Dan's Dungeons and Dragons world. It's
              denominations are in foonts (f), veliks (v), zolots (z), ocels
              (o), kozels (k), and husaks (h). It is normalized against husaks
              as the smallest value

Operation:
  The script reads a value from standard in and outputs the equivilant value on
  standard out. The format for this is the number of coins suffixed with a
  single character to denote it's denomination. multiple coins should be
  separated with a ','.
  Example:
    1g,3s
    would output as
    1z,12o,1k
""")


def process_args(argv):

    in_type = "standard"
    out_type = "durekian"

    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["help", "in=", "out="])
    except getopt.GetoptError:
        show_help()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit(0)
        if opt in ("-i", "--in"):
            in_type = arg
        if opt in ("-o", "--out"):
            out_type = arg
    return in_type, out_type


def get_value(coin):
    try:
        return int(coin[:-1])
    except ValueError:
        print(f"{coin} is not a valid coin string. see --help for more")
        sys.exit(1)


def normalize_standard(coins):
    copper_total = 0
    for coin in coins:
        denomination = coin[-1]
        if denomination == "p":
            value = get_value(coin)
            copper_total += value * 1000
        elif denomination == "g":
            value = get_value(coin)
            copper_total += value * 100
        elif denomination == "e":
            value = get_value(coin)
            copper_total += value * 50
        elif denomination == "s":
            value = get_value(coin)
            copper_total += value * 10
        elif denomination == "c":
            value = get_value(coin)
            copper_total += value

    return copper_total


def normalize_durekian(coins):
    husak_total = 0
    for coin in coins:
        denomination = coin[-1]
        if denomination == "f":
            value = get_value(coin)
            husak_total += value * 960
        elif denomination == "v":
            value = get_value(coin)
            husak_total += value * 320
        elif denomination == "z":
            value = get_value(coin)
            husak_total += value * 80
        elif denomination == "o":
            value = get_value(coin)
            husak_total += value * 4
        elif denomination == "k":
            value = get_value(coin)
            husak_total += value * 2
        elif denomination == "h":
            value = get_value(coin)
            husak_total += value
    return husak_total


def normal_to_standard(normal):
    platnum = normal // 1000
    remaining = normal % 1000
    gold = remaining // 100
    remaining = remaining % 100
    electrum = remaining // 50
    remaining = remaining % 50
    silver = remaining // 10
    copper = remaining % 10

    p_str = f"{platnum}p," if platnum != 0 else ""
    g_str = f"{gold}g," if gold != 0 else ""
    e_str = f"{electrum}e," if electrum != 0 else ""
    s_str = f"{silver}s," if silver != 0 else ""
    c_str = f"{copper}c" if copper != 0 else ""

    output = f"{p_str}{g_str}{e_str}{s_str}{c_str}"

    if output[-1] == ",":
        output = output[:-1]
    return output


def normal_to_durekian(normal):
    foonts = normal // 960
    remaining = normal % 960
    veliks = remaining // 320
    remaining = remaining % 320
    zolots = remaining // 80
    remaining = remaining % 80
    ocels = remaining // 4
    remaining = remaining % 4
    kozels = remaining // 2
    husaks = remaining % 2

    f_str = f"{foonts}f," if foonts != 0 else ""
    v_str = f"{veliks}v," if veliks != 0 else ""
    z_str = f"{zolots}z," if zolots != 0 else ""
    o_str = f"{ocels}o," if ocels != 0 else ""
    k_str = f"{kozels}k," if kozels != 0 else ""
    h_str = f"{husaks}h" if husaks != 0 else ""

    output = f"{f_str}{v_str}{z_str}{o_str}{k_str}{h_str}"

    if output[-1] == ",":
        output = output[:-1]
    return output


def main(argv):
    in_type, out_type = process_args(argv)
    coin_types = ("durekian", "standard")

    if not in_type in coin_types:
        print(f"Unrecognized input type: {in_type}. See  --help for more")
        return
    elif not out_type in coin_types:
        print(f"Unrecognized output type: {out_type}. See  --help for more")
        return

    for line in sys.stdin:
        normalized = 0
        coins = line.strip().split(",")
        if not all([re.match(r"[0-9]+[pgescfvzokh]",coin) for coin in coins]):
            print("Bad coin entry. See --help for more")
            return

        if in_type == coin_types[0]:
            normalized = normalize_durekian(line.strip().split(","))
        elif in_type == coin_types[1]:
            normalized = normalize_standard(line.strip().split(","))

        if out_type == coin_types[0]:
            print(normal_to_durekian(normalized))
        elif out_type == coin_types[1]:
            print(normal_to_standard(normalized))


if __name__ == "__main__":
    main(sys.argv[1:])
