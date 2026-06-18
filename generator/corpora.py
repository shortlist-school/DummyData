"""Shared content banks used across all generators.

Everything here is deliberately light and client-safe: the gallows humour is
strictly pun-based, there is no profanity, and nothing is graphic. Historical
facts are genuine and are surfaced in newsletters and "on this day" notes so
the corpus quietly teaches real Tudor history alongside the fiction.
"""
from __future__ import annotations

# --- Salutations & sign-offs ----------------------------------------------
SALUTATIONS = [
    "Right trusty and well-beloved,",
    "My good lord,",
    "Honoured sir,",
    "Greetings,",
    "To my esteemed colleague,",
    "Good morrow,",
    "Most gracious madam,",
    "Worthy councillor,",
]

SIGN_OFFS = [
    "Your faithful servant,",
    "In haste,",
    "Written in great expedition,",
    "Ever at your command,",
    "With all due reverence,",
    "Yours in loyal service,",
    "By the hand that serves the Crown,",
    "Until the next sitting of the council,",
]

# Tasteful, pun-based gallows humour. Light only.
BEHEADING_QUIPS = [
    "Let us not lose our heads over the seating plan.",
    "I shall stick my neck out and propose Thursday.",
    "Keep your head about you in tomorrow's council.",
    "I trust this note finds you all in one piece.",
    "That motion was dead from the neck up, frankly.",
    "He has been given the chop from the catering committee.",
    "Heads will roll if the venison is late a third time.",
    "Best we get ahead of this before the council does.",
    "A weight off my shoulders — and, for once, nothing else.",
    "Let's nip this one in the bud before it goes to the block.",
]

# Genuine historical facts, surfaced via newsletters / FYI notes.
HISTORICAL_FACTS = [
    "Henry VIII reigned from 1509 to 1547 — nearly thirty-eight years.",
    "The mnemonic for the six queens is: divorced, beheaded, died, divorced, beheaded, survived.",
    "The Act of Supremacy of 1534 declared the king Supreme Head of the Church of England.",
    "Hampton Court Palace passed to the Crown from Cardinal Wolsey in 1529.",
    "The Dissolution of the Monasteries (1536-1541) transferred vast monastic wealth to the Crown.",
    "Henry was a noted musician, linguist and jouster in his youth.",
    "The warship Mary Rose sank in the Solent in 1545 and was raised again in 1982.",
    "Henry's children Mary I, Elizabeth I and Edward VI each took the throne in turn.",
    "The tune 'Greensleeves' is popularly — if doubtfully — attributed to the king himself.",
    "England's currency in this period reckoned in pounds, marks, shillings and pence.",
    "A royal progress could move the entire court between palaces for months at a time.",
    "Cardinal Wolsey rose from humble beginnings to become the second most powerful man in England.",
    "Anne Boleyn's daughter, Elizabeth, would reign for forty-four years.",
    "Thomas Cranmer compiled the foundations of English-language worship.",
    "Catherine Parr was the first woman to publish a book in English under her own name in England.",
]

# --- Geography & setting ---------------------------------------------------
PALACES = [
    "Hampton Court Palace", "the Palace of Whitehall", "Greenwich Palace",
    "Richmond Palace", "Windsor Castle", "Nonsuch Palace", "Eltham Palace",
    "the Tower of London", "Westminster", "Hever Castle",
]

TOWNS = ["London", "Calais", "Dover", "York", "Canterbury", "Oxford", "Cambridge", "Boulogne"]

MONASTERIES = [
    "Glastonbury Abbey", "Furness Abbey", "Rievaulx Abbey", "Tintern Abbey",
    "Fountains Abbey", "Walsingham Priory", "Lewes Priory", "Bury St Edmunds Abbey",
    "Whitby Abbey", "Reading Abbey", "Hailes Abbey", "Syon Abbey",
]

# --- Generic Tudor business vocabulary ------------------------------------
COUNCIL_TOPICS = [
    "the subsidy roll", "the French embassy", "the Scottish border",
    "the wool staple at Calais", "the new coinage", "the harvest levy",
    "the muster of able men", "repairs to the royal barge",
    "the progress itinerary", "the Christmas revels", "the tiltyard schedule",
    "the ordnance accounts", "the victualling of the fleet",
]

DOC_ADJECTIVES = ["draft", "final", "revised", "engrossed", "sealed", "fair-copy", "amended"]

# --- Money helpers ---------------------------------------------------------
def pounds(n: int) -> str:
    return f"£{n:,}"


# --- Disclaimers / footers (adds realism + length) -------------------------
EMAIL_FOOTERS = [
    "This dispatch is intended for the named recipient and may contain matters "
    "touching the Crown. If delivered in error, return it to the Master of the "
    "Posts and destroy all copies.",
    "Sent from my writing-desk. Pray excuse any brevity or blots.",
    "Confidential — for the eyes of the Privy Council only.",
    "Please consider the parchment before printing this message.",
    "",  # many emails have no footer
    "",
]

PRIVILEGE_FOOTER = (
    "PRIVILEGED & CONFIDENTIAL — Attorney-Client Communication. This message "
    "concerns legal advice sought from and rendered by the King's learned "
    "counsel and is not to be disclosed."
)
