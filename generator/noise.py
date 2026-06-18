"""Junk and noise — the realistic chaff every real collection is full of.

Spam, phishing, newsletters, IT notices, out-of-office auto-replies, delivery
failures and calendar invites. All of it is addressed to a collected custodian
so it genuinely lands in the set, giving reviewers a real recall-vs-precision
problem (and giving demos something to cull, tag and suppress). The humour is
light; the phishing/spam are deliberately obvious teaching examples.
"""
from __future__ import annotations

import datetime as dt
import random

from . import cast, config, corpora
from .authoring import doc, ext, mail
from .model import Email

# --- External personas (all fictional .tudor domains) ---------------------
PIZZA = ext("Ye Olde Pizza Hut", "deals@yeoldepizzahut.tudor")
LOTTERY = ext("Royal Spanish Lottery Board", "winner@royal-spanish-lottery.tudor")
PHISH = ext("Crown Account Security", "security@account-secure-crown.tudor")
TIMES = ext("Tudor Times Weekly", "news@tudortimesweekly.tudor")
JOUST = ext("Jousting Monthly", "editor@joustingmonthly.tudor")
TAPESTRY = ext("Hampton Court Home & Bedchamber", "offers@hamptoncourt-deals.tudor")
APOTHECARY = ext("Ye Olde Apothecary", "shop@apothecary-deals.tudor")


def _active_custodian(day: dt.date) -> str:
    custs = [p.key for p in cast.CUSTODIANS if p.active_on(day)]
    return random.choice(custs) if custs else "henry"


def _rand_dt() -> dt.datetime:
    span = (config.PERIOD_END - config.PERIOD_START).days
    day = config.PERIOD_START + dt.timedelta(days=random.randint(0, span))
    return dt.datetime(day.year, day.month, day.day,
                       random.randint(5, 22), random.choice([0, 3, 7, 11, 18, 22, 31, 44, 59]))


# --- Category generators ---------------------------------------------------
def _pizza(to: str, when: dt.datetime) -> Email:
    code = f"TUDOR{when.year}"
    subj = random.choice([
        "Two Trenchers for One — This Sennight Only at Ye Olde Pizza Hut",
        "Hungry After the Hunt? We Deliver to Every Palace",
        "NEW: The Hampton Court Meat Feast (Feeds a Whole Privy Council)",
        "Lenten Special — No Meat, Much Cheese, Still Glorious",
    ])
    body = (
        "Good morrow, noble customer,\n\n"
        "Why hunt all day when supper can come to thy very gate? Ye Olde Pizza Hut now "
        "delivers to all the royal palaces within the hour — or thy next pie is FREE.\n\n"
        f"Quote code {code} at the door this sennight and receive two trenchers for the "
        "price of one. Try our famous Stuffed-Crust Coronation or the new Dissolution "
        "Deep Pan (everything must go).\n\n"
        "Hot, fast, and fit for a king.\n\n"
        "-- To cease these scrolls, despatch a raven marked UNSUBSCRIBE."
    )
    return mail("noise", when, PIZZA, to=[to], subject=subj, body=body,
                category="noise", subcategory="spam_food", storyline="(noise)",
                importance="Low")


def _lottery(to: str, when: dt.datetime) -> Email:
    body = (
        "ESTEEMED FRIEND,\n\n"
        "It is my great honour to inform you that your coffer has been SELECTED in the "
        "El Gordo Royal Draw of the Most Noble Spanish Lottery, which you did not enter "
        "but have nonetheless WON.\n\n"
        "You are entitled to the sum of 500,000 ducats. To release these monies, kindly "
        "reply at once with your full title, your palace, your seal, and the keys to your "
        "treasury for verification purposes only.\n\n"
        "Act with haste, for unclaimed winnings revert to the Crown of Castile.\n\n"
        "Yours in great confidence,\nDon Fernando, Lottery Notary"
    )
    return mail("noise", when, LOTTERY, to=[to],
                subject="CONGRATULATIONS — You Have Won the Royal Spanish Lottery (500,000 Ducats)",
                body=body, category="noise", subcategory="spam_scam", storyline="(noise)",
                importance="High")


def _phish(to: str, when: dt.datetime) -> Email:
    body = (
        "Dear Account Holder,\n\n"
        "We have detected UNUSUAL ACTIVITY upon thy royal seal. For thy protection, thy "
        "mailbox will be SEALED within 24 hours unless thou dost verify thy credentials.\n\n"
        "Press the wax below to confirm thy cipher, thy mother's maiden name, and thy "
        "treasury passphrase:\n\n"
        "    [ VERIFY MY ROYAL ACCOUNT NOW ]\n    http://account-secure-crown.tudor/verify\n\n"
        "Failure to act will result in the permanent loss of thy correspondence.\n\n"
        "Sincerely,\nThe Crown Account Security Team"
    )
    return mail("noise", when, PHISH, to=[to],
                subject="URGENT: Verify Thy Royal Account Within 24 Hours",
                body=body, category="noise", subcategory="phishing", storyline="(noise)",
                importance="High")


def _tudor_times(to: str, when: dt.datetime) -> Email:
    facts = random.sample(corpora.HISTORICAL_FACTS, 3)
    gossip = random.choice([
        "COURT WHISPERS: A certain cardinal's cook has defected to a rival kitchen.",
        "COURT WHISPERS: New French fashions arrive at Greenwich — ruffs are said to be growing.",
        "COURT WHISPERS: The royal menagerie welcomes a most ill-tempered new leopard.",
        "COURT WHISPERS: Wagers are being laid on the date of the next royal progress.",
    ])
    body = (
        f"TUDOR TIMES WEEKLY — week of {when.strftime('%d %B %Y')}\n"
        "Your trusted source for crown, court and countryside.\n\n"
        "THIS WEEK IN HISTORY:\n"
        + "\n".join(f"  * {f}" for f in facts)
        + f"\n\n{gossip}\n\n"
        "WEATHER: Grey, with a chance of beheadings. (Editorial humour; no offence intended.)\n\n"
        "-- Manage thy subscription at the offices of Tudor Times Weekly, Fleet Street."
    )
    e = mail("noise", when, TIMES, to=[to],
             subject=f"Tudor Times Weekly — {when.strftime('%d %b %Y')}",
             body=body, category="noise", subcategory="newsletter", storyline="(noise)",
             importance="Low")
    if random.random() < 0.25:
        e.attachments.append(doc("pdf", "Tudor_Times_Weekly.pdf", "Tudor Times Weekly — Full Issue",
                                 author="scribe", created=when, storyline="(noise)",
                                 spec=dict(paragraphs=[*facts, gossip])))
    return e


def _jousting(to: str, when: dt.datetime) -> Email:
    body = (
        "JOUSTING MONTHLY — Lists, Lances & League Tables\n\n"
        "TOURNAMENT RESULTS: The Duke of Suffolk unhorsed three challengers at the "
        "Shrovetide lists before retiring to mend his pride and his pauldron.\n\n"
        "GEAR REVIEW: We test five new visors so thou keepest thy head — figuratively, "
        "of course.\n\n"
        "FOR SALE: Lightly used tilting armour, one careful owner, slight dent to the "
        "left shoulder. Enquire within.\n\n"
        "-- Jousting Monthly: the only periodical with a points table and a prayer list."
    )
    return mail("noise", when, JOUST, to=[to],
                subject="Jousting Monthly: Lists, Lances & League Tables",
                body=body, category="noise", subcategory="newsletter", storyline="(noise)",
                importance="Low")


_IT_NOTICES = [
    ("Scheduled Maintenance: The Royal Scriptorium (Sunday, 2am-6am)",
     "The Scriptorium will be unavailable this Sunday between the second and sixth hours "
     "while the scribes re-ink the master ledgers. Despatches sent during this window may "
     "be delayed. We apologise for any inconvenience to the realm."),
    ("New Quill Procurement Policy — Effective Immediately",
     "Henceforth all quills are to be requisitioned through the Office of the Lord Steward "
     "using Form Q-1536. Personal goose quills are no longer reimbursable. Swan quills "
     "require the approval of a department head."),
    ("Reminder: Mandatory Doublet & Hose Compliance Training",
     "All members of the household must complete the annual Doublet & Hose Compliance "
     "module before quarter-day. Those who do not will be referred to the Office of the "
     "Lord Steward. The module takes approximately one hour and may be done at thy desk."),
    ("Mailbox Quota Warning: Thy Coffer is 90% Full",
     "Thy correspondence coffer is nearly full. Please archive or burn old scrolls to "
     "avoid interruption. To request additional storage, raise a ticket with Scribe "
     "Services. Note: burning is irreversible and not recommended for records under hold."),
    ("Password Rotation Required: Change Thy Cipher This Month",
     "In accordance with Crown security policy, all seals and ciphers must be rotated this "
     "month. Choose a passphrase of no fewer than twelve runes. Do not reuse thy previous "
     "three ciphers, and never share thy seal — not even with Security (see prior notice)."),
]


def _it_notice(to: str, when: dt.datetime) -> Email:
    subj, body = random.choice(_IT_NOTICES)
    sender = random.choice(["scribe", "hr", "noreply"])
    e = mail("noise", when, sender, to=[to], subject=subj,
             body=body + "\n\n-- This is an automated notice. Do not reply to this raven.",
             category="noise", subcategory="it_notice", storyline="(noise)")
    if "Quill Procurement" in subj and random.random() < 0.6:
        e.attachments.append(doc("docx", "Quill_Procurement_Policy_Q-1536.docx",
                                 "Quill Procurement Policy (Form Q-1536)", author="hr",
                                 created=when, storyline="(noise)",
                                 spec=dict(paragraphs=[body,
                                           "Questions to the Office of the Lord Steward."])))
    return e


def _ooo(to: str, when: dt.datetime) -> Email:
    pool = [p.key for p in cast.PARTICIPANTS if p.active_on(when.date())]
    if not pool:
        pool = ["suffolk"]
    sender = random.choice(pool)
    where = random.choice(["on royal progress", "at the tiltyard", "hunting at Windsor",
                           "attending the French embassy", "indisposed with a chill",
                           "in the country until quarter-day"])
    body = (
        f"Automatic reply.\n\nI am presently {where} and away from my writing-desk. I will "
        "answer thy despatch on my return. For matters touching the Crown that cannot wait, "
        "apply to the Privy Council clerk.\n\n"
        f"-- {cast.get(sender).name}"
    )
    return mail("noise", when, sender, to=[to],
                subject=f"Automatic reply: {random.choice(corpora.COUNCIL_TOPICS).title()}",
                body=body, category="noise", subcategory="auto_reply", storyline="(noise)")


def _bounce(to: str, when: dt.datetime) -> Email:
    bad = random.choice(corpora.COUNCIL_TOPICS).title()
    reason = random.choice([
        "the recipient is no longer with the household.",
        "the mailbox is full and burning is in progress.",
        "the recipient is presently lodged in the Tower and cannot receive post.",
        "the address could not be found in the court directory.",
        "delivery was refused by the recipient's clerk.",
    ])
    body = (
        "This is the Mail Delivery Subsystem.\n\n"
        f"Your message could not be delivered to one or more recipients. Reason: {reason}\n\n"
        f"   Subject: {bad}\n   Status: 5.1.1 (permanent failure)\n\n"
        "No further action is required on thy part. The original despatch is appended below."
    )
    return mail("noise", when, "postmaster", to=[to],
                subject=f"Undeliverable: {bad}",
                body=body, category="noise", subcategory="bounce", storyline="(noise)",
                importance="High")


def _calendar(to: str, when: dt.datetime) -> Email:
    event, place = random.choice([
        ("Grand Joust at the Shrovetide Lists", "the Tiltyard, Greenwich"),
        ("Coronation Banquet", "Westminster Hall"),
        ("Privy Council — Weekly Sitting", "the Council Chamber, Whitehall"),
        ("Christmas Revels", "the Great Hall, Hampton Court"),
        ("Garter Ceremony", "St George's Chapel, Windsor"),
        ("Diplomatic Reception for the French Embassy", "the Presence Chamber"),
        ("Attendance Requested at Tower Green, 9 o'clock", "Tower Green (attendance of the court is requested)"),
    ])
    event_day = when + dt.timedelta(days=random.randint(3, 30))
    time_str = random.choice(["10 o'clock", "noon", "2 in the afternoon", "dusk"])
    body = (
        "You are invited to the following:\n\n"
        f"  EVENT:    {event}\n"
        f"  WHEN:     {event_day.strftime('%A, %d %B %Y')} at {time_str}\n"
        f"  WHERE:    {place}\n"
        "  DRESS:    Court dress; orders and decorations\n\n"
        "Please respond by return raven: ACCEPT / DECLINE / TENTATIVE."
    )
    e = mail("noise", when, "noreply", to=[to], subject=f"Invitation: {event}",
             body=body, category="noise", subcategory="calendar", storyline="(noise)")
    if random.random() < 0.4:
        ics = (
            "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Royal Household//RoyalPost//EN\n"
            f"BEGIN:VEVENT\nSUMMARY:{event}\n"
            f"DTSTART:{event_day.strftime('%Y%m%d')}T100000Z\nLOCATION:{place}\n"
            "STATUS:CONFIRMED\nEND:VEVENT\nEND:VCALENDAR\n"
        )
        e.attachments.append(doc("txt", "invite.ics", f"Invitation — {event}", author="noreply",
                                 created=when, storyline="(noise)", spec=dict(text=ics)))
    return e


def _vendor(to: str, when: dt.datetime) -> Email:
    sender, subj, body = random.choice([
        (TAPESTRY, "Tapestries Half Price — This Quarter Only",
         "Refresh thy bedchamber for the new season. Arras, millefleurs and hunting scenes, "
         "all at half price. Free hanging with any order over ten pounds."),
        (APOTHECARY, "New Leeches In Stock + Free Delivery on Tonics",
         "Fresh leeches, finest theriac, and a new line of pomanders to ward off ill humours "
         "and worse smells. Mention this scroll for a complimentary balancing of thy humours."),
    ])
    return mail("noise", when, sender, to=[to], subject=subj,
                body=body + "\n\n-- Despatch a raven marked STOP to unsubscribe.",
                category="noise", subcategory="spam_vendor", storyline="(noise)",
                importance="Low")


# (generator, weight)
_CATEGORIES = [
    (_pizza, 12), (_lottery, 8), (_phish, 9), (_tudor_times, 12), (_jousting, 7),
    (_it_notice, 18), (_ooo, 10), (_bounce, 8), (_calendar, 12), (_vendor, 4),
]


def build_noise(count: int) -> list[Email]:
    gens = [g for g, _ in _CATEGORIES]
    weights = [w for _, w in _CATEGORIES]
    out: list[Email] = []
    for _ in range(count):
        gen = random.choices(gens, weights=weights, k=1)[0]
        when = _rand_dt()
        out.append(gen(_active_custodian(when.date()), when))
    return out
