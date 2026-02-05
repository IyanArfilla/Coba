import random
from collections import Counter

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, start=2)}

HAND_RANKS = [
    "High Card",
    "One Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
]


def build_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def deal(deck, count):
    hand = deck[:count]
    del deck[:count]
    return hand


def card_display(card):
    rank, suit = card
    return f"{rank}{suit}"


def hand_display(hand):
    return " ".join(card_display(card) for card in hand)


def is_straight(values):
    sorted_vals = sorted(values)
    if sorted_vals == [2, 3, 4, 5, 14]:
        return True, 5
    for i in range(4):
        if sorted_vals[i + 1] != sorted_vals[i] + 1:
            return False, None
    return True, max(sorted_vals)


def evaluate_hand(hand):
    values = [RANK_VALUES[rank] for rank, _ in hand]
    suits = [suit for _, suit in hand]
    counts = Counter(values)
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], -x[0]))

    is_flush = len(set(suits)) == 1
    straight, high_straight = is_straight(values)

    if is_flush and straight:
        return (8, [high_straight])

    if sorted_counts[0][1] == 4:
        four_value = sorted_counts[0][0]
        kicker = max(v for v in values if v != four_value)
        return (7, [four_value, kicker])

    if sorted_counts[0][1] == 3 and sorted_counts[1][1] == 2:
        triple_value = sorted_counts[0][0]
        pair_value = sorted_counts[1][0]
        return (6, [triple_value, pair_value])

    if is_flush:
        return (5, sorted(values, reverse=True))

    if straight:
        return (4, [high_straight])

    if sorted_counts[0][1] == 3:
        triple_value = sorted_counts[0][0]
        kickers = sorted([v for v in values if v != triple_value], reverse=True)
        return (3, [triple_value] + kickers)

    if sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
        pair_values = sorted([sorted_counts[0][0], sorted_counts[1][0]], reverse=True)
        kicker = max(v for v in values if v not in pair_values)
        return (2, pair_values + [kicker])

    if sorted_counts[0][1] == 2:
        pair_value = sorted_counts[0][0]
        kickers = sorted([v for v in values if v != pair_value], reverse=True)
        return (1, [pair_value] + kickers)

    return (0, sorted(values, reverse=True))


def compare_hands(player_hand, dealer_hand):
    player_rank, player_tiebreak = evaluate_hand(player_hand)
    dealer_rank, dealer_tiebreak = evaluate_hand(dealer_hand)

    if player_rank != dealer_rank:
        return 1 if player_rank > dealer_rank else -1
    if player_tiebreak != dealer_tiebreak:
        return 1 if player_tiebreak > dealer_tiebreak else -1
    return 0


def parse_discards(input_text):
    if not input_text.strip():
        return []
    parts = [part.strip() for part in input_text.replace(",", " ").split()]
    discards = []
    for part in parts:
        if not part.isdigit():
            continue
        index = int(part)
        if 1 <= index <= 5 and index not in discards:
            discards.append(index)
    return sorted(discards)


def replace_cards(hand, deck, discards):
    for position in discards:
        hand[position - 1] = deck.pop(0)


def dealer_draw(hand, deck):
    values = [RANK_VALUES[rank] for rank, _ in hand]
    counts = Counter(values)
    discard_positions = []
    for i, value in enumerate(values):
        if counts[value] == 1 and value < 11:
            discard_positions.append(i + 1)
    if len(discard_positions) > 3:
        discard_positions = discard_positions[:3]
    replace_cards(hand, deck, discard_positions)


def play_round():
    deck = build_deck()
    random.shuffle(deck)

    player_hand = deal(deck, 5)
    dealer_hand = deal(deck, 5)

    print("\nKartu kamu:")
    print(hand_display(player_hand))
    discards = parse_discards(
        input("\nMasukkan nomor kartu yang ingin dibuang (1-5), pisahkan dengan spasi. Tekan Enter jika tidak ada: ")
    )

    replace_cards(player_hand, deck, discards)
    dealer_draw(dealer_hand, deck)

    print("\nKartu kamu setelah tukar:")
    print(hand_display(player_hand))
    print(f"Hand kamu: {HAND_RANKS[evaluate_hand(player_hand)[0]]}")

    print("\nKartu dealer:")
    print(hand_display(dealer_hand))
    print(f"Hand dealer: {HAND_RANKS[evaluate_hand(dealer_hand)[0]]}")

    result = compare_hands(player_hand, dealer_hand)
    if result > 0:
        print("\nKamu menang! 🎉")
    elif result < 0:
        print("\nDealer menang.")
    else:
        print("\nSeri!")


def main():
    print("Selamat datang di Poker 5-Card Draw!")
    while True:
        play_round()
        again = input("\nMain lagi? (y/n): ").strip().lower()
        if again != "y":
            print("Terima kasih sudah bermain!")
            break


if __name__ == "__main__":
    main()
