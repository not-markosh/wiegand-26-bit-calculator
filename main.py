import argparse
import sys
import re

parser = argparse.ArgumentParser(description="Wiegand 26-bit Format Calculator")
parser.add_argument("-b", "--bin", metavar="<24-bit binary number>", help="Converts the binary representation of the Facility Code and Card Code without counting parity bits.")
parser.add_argument("-i", "--hex", metavar="<6-digit hexadecimal number>", help="Converts the hexadecimal representation of Facility Code and Card Code.")
parser.add_argument("-d", "--dec", metavar="<decimal Facility Code>,<decimal Card Code>", help="Converts the decimal representation of Facility Code and Card Code.")
parser.add_argument("-n", "--no-parity", action="store_true", help="Do not calculate parity bits. Requires the --bin option with a 26-bit binary number.")


def calculate_parity(binary_data):
    even_parity = binary_data[:12].count("1")
    odd_parity = binary_data[12:].count("1")

    if even_parity % 2:
        even_parity_bit = 1
    else:
        even_parity_bit = 0

    if odd_parity % 2:
        odd_parity_bit = 0
    else:
        odd_parity_bit = 1

    return even_parity_bit, odd_parity_bit


def main():
    args = parser.parse_args()

    if args.no_parity and args.bin:
        if re.fullmatch(r"[0-1]{26}", args.bin):
            hex_data = hex(int(args.bin[1:25], 2))[2:]
            calculated_even_parity_bit, calculated_odd_parity_bit = calculate_parity(args.bin[1:25])
            if args.bin[0] == str(calculated_even_parity_bit):
                even_parity_bit = args.bin[0]
            else:
                even_parity_bit = calculated_even_parity_bit
                print("WARNING: Incorrect even parity bit provided")
            if args.bin[25] == str(calculated_odd_parity_bit):
                odd_parity_bit = args.bin[25]
            else:
                odd_parity_bit = calculated_odd_parity_bit
                print("WARNING: Incorrect odd parity bit provided")
            facility_code_bits = args.bin[1:9]
            card_code_bits = args.bin[9:25]
        else:
            print("ERROR: No valid 26-bit binary number has been provided.\nIf you have a 24-bit binary number, use the --bin option without the --no-parity option.")
            sys.exit(1)
    elif args.bin:
        if re.fullmatch(r"[0-1]{24}", args.bin):
            hex_data = hex(int(args.bin, 2))[2:]
            even_parity_bit, odd_parity_bit = calculate_parity(args.bin)
            facility_code_bits = args.bin[:8]
            card_code_bits = args.bin[8:]
        else:
            print("ERROR: No valid 24-bit binary number has been provided.\nIf you have a 26-bit binary number, use the --bin option with the --no-parity option.")
            sys.exit(1)
    elif args.hex:
        if re.fullmatch(r"(0(x|X))?[0-9a-fA-F]{6}", args.hex):
            if len(args.hex) == 8:
                hex_data = args.hex[2:]
            else:
                hex_data = args.hex
            binary_data = "{0:024b}".format(int(hex_data, 16))
            even_parity_bit, odd_parity_bit = calculate_parity(binary_data)
            facility_code_bits = binary_data[:8]
            card_code_bits = binary_data[8:]
        else:
            print("ERROR: No valid 6-digit hexadecimal number provided.")
            sys.exit(1)
    elif args.dec:
        if re.fullmatch(r"[0-9]+,[0-9]+", args.dec):
            card_data = args.dec.split(",")
            if int(card_data[0]) >= 0 and int(card_data[0]) <= 255:
                if int(card_data[1]) >=0 and int(card_data[1]) <= 65535:
                    facility_code_bits = "{0:08b}".format(int(card_data[0]))
                    card_code_bits = "{0:016b}".format(int(card_data[1]))
                    even_parity_bit, odd_parity_bit = calculate_parity(facility_code_bits + card_code_bits)
                    hex_data = hex(int(facility_code_bits + card_code_bits, 2))[2:]
                else:
                    print("ERROR: Card Code out of range. Must be a decimal number between 0 and 65535")
                    sys.exit(1)
            else:
                print("ERROR: Facility Code out of range. Must be a decimal number between 0 and 255")
                sys.exit(1)
        else:
            print("ERROR: No valid data provided. Must be <Faciliti Code decimal>,<Card Code decimal>")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)

    print("\nWiegand 26-Bit Format Calculator\n")

    print("Binary data: \033[96m{}\033[00m\033[91m{}\033[00m\033[92m{}\033[00m\033[93m{}\033[00m".format(even_parity_bit, facility_code_bits, card_code_bits, odd_parity_bit))
    print("Hexadecimal data without parity bits: {}\n".format(hex_data.upper()))
    print("\033[96mEven parity bit: {}\033[00m".format(even_parity_bit))
    print("\033[91mFacility code: {}\033[00m".format(int(facility_code_bits, 2)))
    print("\033[92mCard code: {}\033[00m".format(int(card_code_bits, 2)))
    print("\033[93mOdd parity bit: {}\033[00m\n".format(odd_parity_bit))

if __name__ == "__main__":
    main()
