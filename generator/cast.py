"""The cast: every person and mailbox in the corpus.

A handful are *collected custodians* (we "have" their mailboxes). The rest are
non-custodian participants whose mail only surfaces because they corresponded
with a custodian -- exactly how a real collection behaves.

All domains use the fictional ``.tudor`` top-level domain so nothing can ever
collide with a real address.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

# --- Domains (all fictional) ----------------------------------------------
ORG_CROWN = "crown.gov.tudor"          # the royal household / government
ORG_CHURCH = "canterbury.church.tudor"  # the Church
ORG_SPAIN = "aragon.gov.tudor"          # Spain / House of Aragon
ORG_CLEVES = "kleve.gov.tudor"          # the Duchy of Cleves
WEBMAIL = "ravenmail.tudor"             # personal web-mail (used to hide the affair)


@dataclass(frozen=True)
class Person:
    key: str
    name: str
    email: str
    org: str
    role: str
    is_custodian: bool = False
    alt_emails: tuple[str, ...] = ()
    active_from: dt.date | None = None
    active_to: dt.date | None = None
    note: str = ""

    def display(self, email: str | None = None) -> str:
        """RFC-822 display form, e.g. ``King Henry VIII <henry.rex@...>``."""
        return f"{self.name} <{email or self.email}>"

    def active_on(self, day: dt.date) -> bool:
        if self.active_from and day < self.active_from:
            return False
        if self.active_to and day > self.active_to:
            return False
        return True


def _d(y: int, m: int, d: int) -> dt.date:
    return dt.date(y, m, d)


# --- Collected custodians --------------------------------------------------
CUSTODIANS: list[Person] = [
    Person(
        "henry", "King Henry VIII", f"henry.rex@{ORG_CROWN}", ORG_CROWN,
        "Sovereign", is_custodian=True,
        note="The king. Centre of every storyline.",
    ),
    Person(
        "cromwell", "Thomas Cromwell", f"thomas.cromwell@{ORG_CROWN}", ORG_CROWN,
        "Chief Minister & Vicegerent", is_custodian=True,
        active_to=_d(1540, 7, 28),
        note="The fixer. Administrative hub; runs the Dissolution. Executed 1540.",
    ),
    Person(
        "cranmer", "Archbishop Thomas Cranmer", f"thomas.cranmer@{ORG_CHURCH}", ORG_CHURCH,
        "Archbishop of Canterbury", is_custodian=True,
        active_from=_d(1533, 3, 30),
        note="Architect of the annulments and the English liturgy.",
    ),
    Person(
        "anne_boleyn", "Queen Anne Boleyn", f"anne.boleyn@{ORG_CROWN}", ORG_CROWN,
        "Queen Consort (2nd)", is_custodian=True,
        active_to=_d(1536, 5, 19),
        note="Wife #2. 'Beheaded'. Adultery trial is storyline 2.",
    ),
    Person(
        "catherine_howard", "Queen Catherine Howard", f"catherine.howard@{ORG_CROWN}", ORG_CROWN,
        "Queen Consort (5th)", is_custodian=True,
        alt_emails=(f"kitty.h@{WEBMAIL}",),
        active_from=_d(1540, 7, 28), active_to=_d(1542, 2, 13),
        note="Wife #5. 'Beheaded'. The Culpeper affair is the central investigation.",
    ),
    Person(
        "catherine_parr", "Queen Catherine Parr", f"catherine.parr@{ORG_CROWN}", ORG_CROWN,
        "Queen Consort (6th)", is_custodian=True,
        active_from=_d(1543, 7, 12),
        note="Wife #6. 'Survived'. The organiser; winds the story down.",
    ),
]

# --- Non-custodian participants -------------------------------------------
PARTICIPANTS: list[Person] = [
    Person(
        "aragon", "Queen Catherine of Aragon", f"catalina.aragon@{ORG_CROWN}", ORG_CROWN,
        "Queen Consort (1st)",
        alt_emails=(f"catalina.aragon@{ORG_SPAIN}",), active_to=_d(1536, 1, 7),
        note="Wife #1. 'Divorced' (annulled). The Great Matter is storyline 1.",
    ),
    Person(
        "jane_seymour", "Queen Jane Seymour", f"jane.seymour@{ORG_CROWN}", ORG_CROWN,
        "Queen Consort (3rd)",
        active_from=_d(1536, 5, 30), active_to=_d(1537, 10, 24),
        note="Wife #3. 'Died'. Mother of Edward VI.",
    ),
    Person(
        "anne_cleves", "Anne of Cleves", f"anne.cleves@{ORG_CLEVES}", ORG_CLEVES,
        "Queen Consort (4th)",
        alt_emails=(f"anne.cleves@{ORG_CROWN}",),
        active_from=_d(1539, 9, 1), active_to=_d(1543, 1, 1),
        note="Wife #4. 'Divorced'. The portrait misunderstanding is storyline 4.",
    ),
    Person(
        "wolsey", "Cardinal Thomas Wolsey", f"thomas.wolsey@{ORG_CHURCH}", ORG_CHURCH,
        "Lord Chancellor", active_to=_d(1530, 11, 29),
        note="Failed to secure the annulment; fell from power 1529; died 1530.",
    ),
    Person(
        "more", "Sir Thomas More", f"thomas.more@{ORG_CROWN}", ORG_CROWN,
        "Lord Chancellor", active_to=_d(1535, 7, 6),
        note="Succeeded Wolsey; refused the oath; executed 1535.",
    ),
    Person(
        "thomas_boleyn", "Thomas Boleyn, Earl of Wiltshire", f"thomas.boleyn@{ORG_CROWN}", ORG_CROWN,
        "Earl & diplomat", note="Anne and George Boleyn's father.",
    ),
    Person(
        "george_boleyn", "George Boleyn, Lord Rochford", f"george.boleyn@{ORG_CROWN}", ORG_CROWN,
        "Courtier & diplomat", active_to=_d(1536, 5, 17),
        note="Anne's brother; tried and executed alongside her.",
    ),
    Person(
        "culpeper", "Thomas Culpeper", f"thomas.culpeper@{ORG_CROWN}", ORG_CROWN,
        "Gentleman of the Privy Chamber",
        alt_emails=(f"t.culpeper@{WEBMAIL}",), active_to=_d(1541, 12, 10),
        note="At the heart of the Howard affair. Note the personal web-mail account.",
    ),
    Person(
        "dereham", "Francis Dereham", f"francis.dereham@{ORG_CROWN}", ORG_CROWN,
        "Private Secretary to the Queen", active_to=_d(1541, 12, 10),
        note="Catherine Howard's pre-marriage entanglement; later her secretary.",
    ),
    Person(
        "rochford", "Lady Jane Rochford", f"jane.rochford@{ORG_CROWN}", ORG_CROWN,
        "Lady of the Bedchamber", active_to=_d(1542, 2, 13),
        note="Go-between who arranged the Howard/Culpeper meetings.",
    ),
    Person(
        "smeaton", "Mark Smeaton", f"mark.smeaton@{ORG_CROWN}", ORG_CROWN,
        "Court Musician", active_to=_d(1536, 5, 17),
        note="Accused in the Boleyn case.",
    ),
    Person(
        "norris", "Sir Henry Norris", f"henry.norris@{ORG_CROWN}", ORG_CROWN,
        "Groom of the Stool", active_to=_d(1536, 5, 17),
        note="Accused in the Boleyn case.",
    ),
    Person(
        "chapuys", "Ambassador Eustace Chapuys", f"e.chapuys@{ORG_SPAIN}", ORG_SPAIN,
        "Imperial Ambassador",
        note="Spain's man at court; sympathetic to Catherine of Aragon.",
    ),
    Person(
        "suffolk", "Charles Brandon, Duke of Suffolk", f"charles.brandon@{ORG_CROWN}", ORG_CROWN,
        "Master of the Horse", note="The king's oldest friend and jousting partner.",
    ),
    Person(
        "gardiner", "Bishop Stephen Gardiner", f"stephen.gardiner@{ORG_CHURCH}", ORG_CHURCH,
        "Bishop of Winchester", active_from=_d(1531, 1, 1),
        note="Religious conservative; rival to Cromwell and Cranmer.",
    ),
    Person(
        "mary", "Lady Mary Tudor", f"mary.tudor@{ORG_CROWN}", ORG_CROWN,
        "The King's daughter", active_from=_d(1531, 1, 1),
        note="Daughter of Catherine of Aragon; future Mary I.",
    ),
    Person(
        "seymour_edward", "Sir Edward Seymour", f"edward.seymour@{ORG_CROWN}", ORG_CROWN,
        "Privy Councillor", active_from=_d(1536, 1, 1),
        note="Jane Seymour's brother; rising power.",
    ),
    Person(
        "audley", "Lord Chancellor Thomas Audley", f"thomas.audley@{ORG_CROWN}", ORG_CROWN,
        "Lord Chancellor", active_from=_d(1533, 1, 1),
        note="Succeeded More; presided over several trials.",
    ),
    Person(
        "rich", "Sir Richard Rich", f"richard.rich@{ORG_CROWN}", ORG_CROWN,
        "Solicitor General", active_from=_d(1533, 1, 1),
        note="The crown's legal enforcer.",
    ),
]

# --- Functional / automated mailboxes -------------------------------------
SYSTEM: list[Person] = [
    Person("scribe", "Scribe Services", f"scribe-services@{ORG_CROWN}", ORG_CROWN, "IT / Scriptorium"),
    Person("noreply", "Royal Household (Do Not Reply)", f"no-reply@{ORG_CROWN}", ORG_CROWN, "Automated"),
    Person("postmaster", "Mail Delivery Subsystem", f"postmaster@{ORG_CROWN}", ORG_CROWN, "Automated"),
    Person("privy", "Privy Council Distribution", f"privy-council@{ORG_CROWN}", ORG_CROWN, "Distribution list"),
    Person("hr", "Office of the Lord Steward", f"household-office@{ORG_CROWN}", ORG_CROWN, "HR / Household"),
]

# --- Registries ------------------------------------------------------------
ALL_PEOPLE: list[Person] = CUSTODIANS + PARTICIPANTS + SYSTEM
BY_KEY: dict[str, Person] = {p.key: p for p in ALL_PEOPLE}
CUSTODIAN_KEYS: set[str] = {p.key for p in CUSTODIANS}
# Every email address (incl. alts) mapped back to its Person, for lookups.
BY_EMAIL: dict[str, Person] = {}
for _p in ALL_PEOPLE:
    BY_EMAIL[_p.email.lower()] = _p
    for _alt in _p.alt_emails:
        BY_EMAIL[_alt.lower()] = _p


def get(key: str) -> Person:
    return BY_KEY[key]


def custodian_of_email(email: str) -> str | None:
    """Return the custodian key for an address, or None if not a custodian."""
    p = BY_EMAIL.get(email.lower())
    if p and p.is_custodian:
        return p.key
    return None
