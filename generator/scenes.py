"""The bespoke narrative spine: six storylines as threaded conversations.

These are the hand-crafted, evidentiary "gem" documents a reviewer is meant to
find — privileged legal advice, financial spreadsheets, and the concealed
correspondence of the Howard affair. Each function returns a list of Emails
(with their attachment families) wired into conversations. Procedural filler in
``narrative.py`` bulks the storylines out around this spine.

Tone note: gallows humour is strictly pun-based; nothing is graphic; everything
is fictional and client-safe.
"""
from __future__ import annotations

from .authoring import at, compose, doc, mail, thread
from .model import Email

# Confidentiality vocabulary reused throughout.
PRIV_AC = "Privileged - Attorney-Client"
PRIV_WP = "Privileged - Work Product"
CONF = "Confidential"
PRIVY = "Internal - Privy Council"


# ==========================================================================
# STORYLINE 1 — THE KING'S GREAT MATTER  (1527-1533)
# ==========================================================================
def great_matter() -> list[Email]:
    out: list[Email] = []

    out += thread([
        mail("gm", at(1527, 5, 17, 8, 30), "henry", to=["wolsey"], cc=["cromwell"],
             subject="The King's Great Matter — to be handled with all discretion",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             importance="High", confidentiality=CONF,
             body=compose(
                 "My Lord Cardinal,",
                 ["You know the disquiet that has long sat upon my conscience touching my "
                  "marriage to the Queen. The matter can wait no longer.",
                  "I charge you to obtain from His Holiness a clean and lawful annulment, "
                  "and to do so quietly. Spare no effort, and spare me no excuses.",
                  "I need not remind you what hangs upon a male heir."],
                 "By the King's own hand,", "Henry R.")),
        mail("gm", at(1527, 6, 2, 14, 0), "wolsey", to=["henry"], cc=["cromwell"],
             subject="Re: The King's Great Matter — to be handled with all discretion",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             confidentiality=CONF,
             body=compose(
                 "Your Majesty,",
                 ["I have set the wheels in motion and opened a quiet correspondence with Rome. "
                  "The path is delicate: the Emperor is the Queen's nephew, and His Holiness "
                  "is presently much in the Emperor's debt.",
                  "I counsel patience. These things cannot be rushed without rousing suspicion."],
                 "Your faithful servant,", "T. Wolsey, Cardinal")),
    ], "great-matter-tasking")

    # Catherine of Aragon's dignified protest.
    out.append(mail("gm", at(1528, 11, 9, 10, 0), "aragon", to=["henry"], cc=["chapuys"],
                    subject="A wife's answer",
                    category="narrative", subcategory="great_matter", storyline="The Great Matter",
                    body=compose(
                        "My lord and husband,",
                        ["I have been to you a true and humble wife these many years. I came to "
                         "you a maid, and I will not now consent to a question that touches my "
                         "honour and our daughter's right.",
                         "Do as your conscience bids you, but know that mine is clear."],
                        "Your loyal wife,", "Catalina")))

    # Wolsey's failure and fall.
    out += thread([
        mail("gm", at(1529, 7, 23, 16, 30), "wolsey", to=["henry"],
             subject="The legatine court at Blackfriars",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             importance="High", confidentiality=CONF,
             body=compose(
                 "Your Majesty,",
                 ["I must report, with a heavy heart, that the cause has been revoked to Rome. "
                  "The court will give no verdict here. I have failed to bring it to the close "
                  "you desired, though not for want of labour."],
                 "In sorrow,", "T. Wolsey")),
        mail("gm", at(1529, 10, 19, 9, 0), "henry", to=["wolsey"], cc=["cromwell", "more"],
             subject="Re: The legatine court at Blackfriars",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             importance="High",
             body=compose(
                 "Wolsey,",
                 ["You have had years, and the finest revenues in England, and you bring me "
                  "nothing. The Great Seal is to be surrendered this day to Sir Thomas More.",
                  "Reflect on how far a man may rise, and how swiftly he may come down."],
                 "Henry R.", "")),
    ], "great-matter-wolsey-fall")

    # Cromwell's pivot: the break with Rome (privileged legal advice + attachment).
    opinion = doc("pdf", "Opinion_on_Royal_Supremacy.pdf",
                  "Opinion on the Royal Supremacy",
                  author="cromwell", created=at(1532, 1, 8, 7, 0), modified=at(1532, 1, 9, 18, 0),
                  confidentiality=PRIV_AC, storyline="The Great Matter", hot=True,
                  spec=dict(paragraphs=[
                      "QUESTION PRESENTED: Whether the King's Majesty may lawfully be recognised "
                      "as the supreme head of the Church in England, and the cause of his marriage "
                      "determined within the realm without recourse to Rome.",
                      "SHORT ANSWER: Yes. The ancient privileges of this realm, and the authority "
                      "of Convocation and Parliament, are sufficient to the purpose.",
                      "ANALYSIS: We advise that an Act be drawn restraining appeals to Rome, "
                      "declaring this realm an empire entire of itself. The Archbishop of "
                      "Canterbury may then hear and determine the cause at home.",
                      "This memorandum reflects confidential legal advice prepared at the King's "
                      "request and is protected from disclosure."],
                      closing="Respectfully submitted for the King's eyes only."))
    out += thread([
        mail("gm", at(1532, 1, 10, 8, 15), "cromwell", to=["henry"], cc=["cranmer"],
             subject="A way through — privileged advice enclosed",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             importance="High", confidentiality=PRIV_AC, hot=True, attachments=[opinion],
             body=compose(
                 "Your Majesty,",
                 ["Where Rome will not give, England may take. I enclose privileged advice setting "
                  "out the lawful path: an Act restraining appeals, and recognition of Your Majesty "
                  "as Supreme Head of the Church in England.",
                  "The Archbishop may then determine the Great Matter here at home. I commend the "
                  "enclosed to Your Majesty's careful and private reading."],
                 "Your servant,", "Thomas Cromwell")),
        mail("gm", at(1532, 1, 11, 10, 0), "henry", to=["cromwell"], cc=["cranmer"],
             subject="Re: A way through — privileged advice enclosed",
             category="narrative", subcategory="great_matter", storyline="The Great Matter",
             importance="High", confidentiality=PRIV_AC,
             body=compose(
                 "Cromwell,",
                 ["This is the first sensible counsel I have had in five years. Proceed — quietly, "
                  "lawfully, and quickly. Keep More away from the drafting; his conscience is "
                  "tender and his pen is slow."],
                 "Henry R.", "")),
    ], "great-matter-supremacy")

    # The annulment granted by Cranmer (decree attachment) and the announcement.
    decree = doc("docx", "Decree_of_Annulment_1533.docx",
                 "Sentence of Annulment of the Marriage of the King and the Lady Catherine",
                 author="cranmer", created=at(1533, 5, 22, 7, 0), modified=at(1533, 5, 23, 6, 0),
                 confidentiality=CONF, storyline="The Great Matter",
                 spec=dict(paragraphs=[
                     "We, Thomas Cranmer, Archbishop of Canterbury, having examined the cause, "
                     "do pronounce the union of the King's Majesty and the Lady Catherine to have "
                     "been against the law of God, and therefore null and of no effect.",
                     "The King's Majesty is free to contract such marriage as God and the realm "
                     "shall bless."], closing="Given at Dunstable, this 23rd day of May, 1533."))
    out.append(mail("gm", at(1533, 5, 23, 9, 30), "cranmer", to=["henry"], cc=["cromwell"],
                    subject="The cause is determined",
                    category="narrative", subcategory="great_matter", storyline="The Great Matter",
                    importance="High", confidentiality=CONF, attachments=[decree],
                    body=compose(
                        "Your Majesty,",
                        ["It is done. I enclose the sentence. The former union is declared void, "
                         "and Your Majesty's marriage to Queen Anne stands lawful and good.",
                         "May this at last set Your Majesty's conscience at rest."],
                        "Your obedient servant,", "T. Cranmer")))
    out.append(mail("gm", at(1533, 6, 1, 12, 0), "henry", to=["privy"], cc=["cromwell", "cranmer"],
                    subject="Proclamation — Queen Anne",
                    category="narrative", subcategory="great_matter", storyline="The Great Matter",
                    body=compose(
                        "My lords,",
                        ["Let it be known throughout the realm that the Lady Anne is this day "
                         "crowned Queen of England. You will accord Her Majesty all honour due "
                         "to her estate.",
                         "Let us not lose our heads over the seating at the coronation feast — "
                         "the Imperial ambassador is, regrettably, on the list."],
                        "Henry R.", "")))
    return out


# ==========================================================================
# STORYLINE 2 — THE RISE AND FALL OF ANNE BOLEYN  (1533-1536)
# ==========================================================================
def anne_boleyn() -> list[Email]:
    out: list[Email] = []

    birth = doc("pdf", "Birth_Announcement_Princess_Elizabeth.pdf",
                "Announcement of the Birth of the Princess Elizabeth",
                author="cromwell", created=at(1533, 9, 7, 18, 0),
                storyline="Anne Boleyn",
                spec=dict(paragraphs=[
                    "Be it known that on this 7th day of September, 1533, at Greenwich Palace, "
                    "the Queen's Majesty was delivered of a fair and healthy princess, to be "
                    "named Elizabeth.",
                    "The realm gives thanks for the safe delivery of mother and child."],
                    closing="God save the King and Queen."))
    out += thread([
        mail("ab", at(1533, 9, 7, 19, 30), "anne_boleyn", to=["henry"],
             subject="Our daughter",
             category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
             attachments=[birth],
             body=compose(
                 "My dear husband,",
                 ["We have a daughter, strong and well, and I have named her Elizabeth for your "
                  "lady mother. I know you hoped for a son. Sons will follow.",
                  "Come and see her. She has your temper already."],
                 "Your loving Anne", "")),
        mail("ab", at(1533, 9, 8, 8, 0), "henry", to=["anne_boleyn"],
             subject="Re: Our daughter",
             category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
             body=compose(
                 "Anne,",
                 ["A daughter is a fine beginning, and Elizabeth a fine name. I am well pleased "
                  "with you both. Rest, and grow strong, for England will want a prince before "
                  "long."],
                 "Your Henry", "")),
    ], "anne-elizabeth-birth")

    # Strain after the miscarriage of January 1536.
    out.append(mail("ab", at(1536, 1, 30, 16, 0), "anne_boleyn", to=["henry"],
                    subject="I am grieved",
                    category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
                    importance="High",
                    body=compose(
                        "My lord,",
                        ["You will have heard. I am as grieved as you, and more. I beg you not to "
                         "turn from me for a misfortune that God alone governs.",
                         "Do not let the whisperers at court make of my sorrow a weapon against me."],
                        "Your unhappy wife,", "Anne")))

    # Cromwell builds the case (privileged work product + investigatory attachments).
    witnesses = doc("xlsx", "Schedule_of_Examinations.xlsx",
                    "Schedule of Examinations — Privy Matter",
                    author="cromwell", created=at(1536, 4, 24, 7, 0), modified=at(1536, 4, 29, 20, 0),
                    confidentiality=PRIV_WP, storyline="Anne Boleyn", hot=True,
                    spec=dict(sheet="Examinations",
                              headers=["Name", "Office", "Date to be Examined", "Status"],
                              rows=[
                                  ["Mark Smeaton", "Court Musician", "30 Apr 1536", "Detained for questioning"],
                                  ["Sir Henry Norris", "Groom of the Stool", "01 May 1536", "To be examined"],
                                  ["Sir Francis Weston", "Gentleman", "02 May 1536", "To be examined"],
                                  ["William Brereton", "Gentleman", "02 May 1536", "To be examined"],
                                  ["George Boleyn, Lord Rochford", "Courtier", "02 May 1536", "To be examined"],
                              ],
                              note="WORK PRODUCT — prepared in anticipation of proceedings. Not for distribution."))
    out += thread([
        mail("ab", at(1536, 4, 24, 7, 45), "cromwell", to=["henry"], cc=["rich"],
             subject="A delicate inquiry — privileged",
             category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
             importance="High", confidentiality=PRIV_WP, hot=True, attachments=[witnesses],
             body=compose(
                 "Your Majesty,",
                 ["Acting on Your Majesty's instruction, I have begun a discreet inquiry into "
                  "certain conduct touching the Queen's household. I enclose a schedule of those "
                  "to be examined.",
                  "I will report findings to Your Majesty alone. This work is privileged and must "
                  "not pass beyond Your Majesty, Sir Richard, and myself."],
                 "Your servant,", "Thomas Cromwell")),
        mail("ab", at(1536, 5, 1, 21, 0), "cromwell", to=["henry"],
             subject="Re: A delicate inquiry — privileged",
             category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
             importance="High", confidentiality=PRIV_WP, hot=True,
             body=compose(
                 "Your Majesty,",
                 ["The musician has made a statement. On the strength of it, and of the other "
                  "examinations, there is matter enough to proceed. I have given the necessary "
                  "instructions for the morning.",
                  "I will not commit the particulars to writing beyond this."],
                 "Your servant,", "T.C.")),
    ], "anne-investigation")

    indictment = doc("pdf", "Indictment_Crown_Matter.pdf",
                     "Bill of Indictment — Crown Matter",
                     author="rich", created=at(1536, 5, 10, 7, 0), confidentiality=CONF,
                     storyline="Anne Boleyn",
                     spec=dict(paragraphs=[
                         "The jurors present that the persons named did conspire against the King's "
                         "Majesty and did commit offences touching the honour of the Crown.",
                         "The cause is set down for hearing before the peers at the Tower of London."],
                         closing="Exhibited by the Solicitor General."))
    out.append(mail("ab", at(1536, 5, 12, 8, 0), "rich", to=["audley", "cromwell"], cc=["henry"],
                    subject="Cause set down for hearing",
                    category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
                    confidentiality=CONF, attachments=[indictment],
                    body=compose(
                        "My lords,",
                        ["The bill is exhibited and the cause set down. The peers will sit at the "
                         "Tower. I attach the indictment for your records."],
                        "Your servant,", "Ric. Rich")))

    # Anne's dignified final letter, and the king's grim humour to a confidant.
    out.append(mail("ab", at(1536, 5, 16, 6, 0), "anne_boleyn", to=["henry"],
                    subject="From a faithful wife",
                    category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
                    importance="High", hot=True,
                    body=compose(
                        "Sir,",
                        ["You have raised me from a gentlewoman to a marchioness, from a marchioness "
                         "to a queen. There remains only to raise me, as you intend, to be a saint "
                         "in heaven.",
                         "I ask only an open trial, and that my honour be not buried with me. Whatever "
                         "becomes of me, our daughter is innocent of all."],
                        "From my cheerless lodging in the Tower,", "Anne")))
    out.append(mail("ab", at(1536, 5, 18, 20, 0), "henry", to=["suffolk"],
                    subject="The arrangements",
                    category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
                    confidentiality=CONF,
                    body=compose(
                        "Charles,",
                        ["I have sent to Calais for the French swordsman, as a mercy. They tell me "
                         "his aim is very good — which is more than can be said for half my council.",
                         "See that all is done with dignity, and quietly. Then we will speak no more "
                         "of it."],
                        "Henry R.", "")))
    # Cranmer annuls the Boleyn marriage two days before the execution (the irony).
    out.append(mail("ab", at(1536, 5, 17, 11, 0), "cranmer", to=["henry"], cc=["cromwell"],
                    subject="The second cause",
                    category="narrative", subcategory="anne_boleyn", storyline="Anne Boleyn",
                    confidentiality=CONF,
                    body=compose(
                        "Your Majesty,",
                        ["As instructed, I have pronounced the marriage to Queen Anne void on the "
                         "grounds laid before me. I confess the lawyer in me struggles to reconcile "
                         "a marriage that never was with a charge of unfaithfulness within it, but "
                         "I have done as I was bid."],
                        "Heavily,", "T. Cranmer")))
    return out


# ==========================================================================
# STORYLINE 3 — THE DISSOLUTION OF THE MONASTERIES  (1535-1540)
# ==========================================================================
def dissolution() -> list[Email]:
    out: list[Email] = []

    articles = doc("docx", "Visitation_Articles.docx",
                   "Articles of Visitation for the Religious Houses",
                   author="cromwell", created=at(1535, 1, 18, 7, 0), confidentiality=PRIVY,
                   storyline="Dissolution",
                   spec=dict(paragraphs=[
                       "By the King's authority as Supreme Head, the following houses are to be "
                       "visited and their revenues, plate, and ornaments faithfully recorded.",
                       "Commissioners shall enquire into the manner of life of the religious, the "
                       "value of lands, and all debts owing.",
                       "Returns are to be made to the office of the Vicegerent with all speed."],
                       closing="By command of Thomas Cromwell, Vicegerent in Spirituals."))
    out += thread([
        mail("dis", at(1535, 1, 20, 8, 0), "cromwell", to=["rich"], cc=["henry"],
             subject="Visitation of the religious houses — articles enclosed",
             category="narrative", subcategory="dissolution", storyline="Dissolution",
             confidentiality=PRIVY, attachments=[articles],
             body=compose(
                 "Sir Richard,",
                 ["The great survey begins. I enclose the articles. Send out the commissioners "
                  "and let them be thorough — the Crown's needs are pressing and the harvest of "
                  "this work will be considerable.",
                  "Accurate returns, mind. I will not have the valuations padded nor pared."],
                 "Cromwell", "")),
        mail("dis", at(1535, 6, 30, 17, 0), "rich", to=["cromwell"], cc=["henry"],
             subject="Re: Visitation of the religious houses — returns",
             category="narrative", subcategory="dissolution", storyline="Dissolution",
             confidentiality=CONF,
             body=compose(
                 "Master Secretary,",
                 ["The first returns are in and they are richer than we hoped. I will forward the "
                  "consolidated valuation under separate cover.",
                  "Some houses have, shall we say, misremembered their plate. We are reminding them."],
                 "Your servant,", "Ric. Rich")),
    ], "dissolution-visitation")

    valor = doc("xlsx", "Valor_Ecclesiasticus_Summary.xlsx",
                "Valor Ecclesiasticus — Summary of Net Annual Values",
                author="rich", created=at(1535, 7, 1, 6, 0), modified=at(1535, 7, 2, 19, 0),
                confidentiality=CONF, storyline="Dissolution", hot=True,
                spec=dict(sheet="Net Values",
                          headers=["Religious House", "County", "Gross (£)", "Net (£)", "Plate (oz)"],
                          rows=[
                              ["Glastonbury Abbey", "Somerset", 3642, 3508, 11400],
                              ["Bury St Edmunds Abbey", "Suffolk", 2336, 1659, 7200],
                              ["Reading Abbey", "Berkshire", 2116, 1938, 4100],
                              ["Fountains Abbey", "Yorkshire", 1173, 1115, 3850],
                              ["Tintern Abbey", "Monmouth", 234, 192, 540],
                              ["Whitby Abbey", "Yorkshire", 505, 437, 1220],
                              ["Furness Abbey", "Lancashire", 967, 805, 2600],
                              ["Walsingham Priory", "Norfolk", 446, 391, 1890],
                          ],
                          note="Net annual values per the commissioners' returns. CONFIDENTIAL — Court of Augmentations."))
    out += thread([
        mail("dis", at(1535, 7, 3, 9, 0), "rich", to=["cromwell"], cc=["henry"],
             subject="Consolidated valuation — for the King",
             category="narrative", subcategory="dissolution", storyline="Dissolution",
             importance="High", confidentiality=CONF, attachments=[valor],
             body=compose(
                 "Master Secretary,",
                 ["I enclose the consolidated valuation. Glastonbury alone is worth more than three "
                  "thousand pounds clear, with plate to match.",
                  "The total will keep the Treasury in good heart for years. Pray lay it before the "
                  "King."],
                 "Your servant,", "Ric. Rich")),
        mail("dis", at(1535, 7, 4, 11, 0), "cromwell", to=["henry"], cc=["rich"],
             subject="Fw: Consolidated valuation — for the King",
             category="narrative", subcategory="dissolution", storyline="Dissolution",
             importance="High", confidentiality=CONF, attachments=[valor],
             body=compose(
                 "Your Majesty,",
                 ["As foreshadowed, the enclosed shows the yearly worth of the houses surveyed so "
                  "far. The sums speak for themselves. With Your Majesty's leave I will proceed to "
                  "the greater houses next."],
                 "Your servant,", "Thomas Cromwell")),
    ], "dissolution-valor")

    # Resistance: the Pilgrimage of Grace (1536).
    out.append(mail("dis", at(1536, 10, 14, 7, 30), "rich", to=["cromwell", "henry"],
                    subject="Trouble in the North",
                    category="narrative", subcategory="dissolution", storyline="Dissolution",
                    importance="High", confidentiality=CONF,
                    body=compose(
                        "My lords,",
                        ["There is a rising in Lincolnshire and Yorkshire, calling itself the "
                         "Pilgrimage of Grace. They demand the abbeys be spared and Cromwell be "
                         "dismissed — in that order, which I take as a compliment to the Master "
                         "Secretary.",
                         "We will need a firm hand and fair words both."],
                        "In haste,", "Ric. Rich")))

    treasury = doc("pdf", "Treasury_Receipts_Augmentations.pdf",
                   "Court of Augmentations — Receipts to Date",
                   author="rich", created=at(1540, 3, 1, 7, 0), confidentiality=CONF,
                   storyline="Dissolution",
                   spec=dict(paragraphs=[
                       "Statement of receipts into the Court of Augmentations arising from the "
                       "dissolved houses, comprising rents, sales of lead and bells, and plate "
                       "delivered to the Jewel House.",
                       "The greater monasteries are now substantially surrendered. Disposal of "
                       "lands to the gentry proceeds and brings further ready money."],
                       table={"headers": ["Source", "Amount (£)"],
                              "rows": [["Rents and farms", "32,000"], ["Sales of materials", "18,500"],
                                       ["Plate and jewels", "26,750"], ["Land sales", "41,200"]]},
                       closing="Submitted to the Vicegerent."))
    out.append(mail("dis", at(1540, 3, 2, 9, 0), "rich", to=["cromwell"], cc=["henry"],
                    subject="Receipts to date — Augmentations",
                    category="narrative", subcategory="dissolution", storyline="Dissolution",
                    confidentiality=CONF, attachments=[treasury],
                    body=compose(
                        "Master Secretary,",
                        ["The receipts to date are enclosed. The work has more than paid for itself. "
                         "Whatever else is said of this enterprise, it has filled the Treasury."],
                        "Your servant,", "Ric. Rich")))
    return out


# ==========================================================================
# STORYLINE 4 — THE CLEVES MISUNDERSTANDING  (1539-1540)
# ==========================================================================
def cleves() -> list[Email]:
    out: list[Email] = []

    portrait = doc("png", "Portrait_Anne_of_Cleves_Holbein.png",
                   "Portrait of the Lady Anne of Cleves",
                   author="cromwell", created=at(1539, 8, 12, 9, 0),
                   storyline="Cleves",
                   spec=dict(style="portrait", caption="The Lady Anne of Cleves",
                             subtitle="after Master Holbein"))
    out += thread([
        mail("clv", at(1539, 8, 14, 10, 0), "cromwell", to=["henry"],
             subject="A most advantageous match — portrait enclosed",
             category="narrative", subcategory="cleves", storyline="Cleves",
             importance="High", confidentiality=CONF, attachments=[portrait],
             body=compose(
                 "Your Majesty,",
                 ["I commend to Your Majesty the Lady Anne, sister to the Duke of Cleves. The "
                  "alliance would bind us to the Protestant princes and answer the threat of France "
                  "and the Emperor combining against us.",
                  "Master Holbein has sent her likeness, which I enclose. All report her gentle and "
                  "of good understanding."],
                 "Your servant,", "Thomas Cromwell")),
        mail("clv", at(1540, 1, 2, 18, 0), "henry", to=["cromwell"],
             subject="Re: A most advantageous match — portrait enclosed",
             category="narrative", subcategory="cleves", storyline="Cleves",
             importance="High", confidentiality=CONF, hot=True,
             body=compose(
                 "Cromwell,",
                 ["I have met the lady at Rochester. I will say only that the portrait was a great "
                  "deal more agreeable than the introduction, and that Master Holbein has a "
                  "diplomat's eye for flattery.",
                  "I am not well handled in this. We will speak privately, and soon."],
                 "Henry R.", "")),
    ], "cleves-match")

    out += thread([
        mail("clv", at(1540, 7, 6, 8, 0), "henry", to=["cranmer", "cromwell"],
             subject="The Cleves marriage — a quiet remedy",
             category="narrative", subcategory="cleves", storyline="Cleves",
             confidentiality=PRIV_AC,
             body=compose(
                 "My lords,",
                 ["The marriage was never to my liking and, I am advised, never fully made. Find me "
                  "the lawful means to undo it — quietly, and with all courtesy to the lady, who is "
                  "blameless in this."],
                 "Henry R.", "")),
        mail("clv", at(1540, 7, 9, 16, 0), "cranmer", to=["henry"], cc=["cromwell"],
             subject="Re: The Cleves marriage — a quiet remedy",
             category="narrative", subcategory="cleves", storyline="Cleves",
             confidentiality=PRIV_AC,
             body=compose(
                 "Your Majesty,",
                 ["The convocation has pronounced the marriage void on the grounds advised. The "
                  "Lady Anne consents most graciously and asks only to remain in England as Your "
                  "Majesty's friend."],
                 "Your servant,", "T. Cranmer")),
        mail("clv", at(1540, 7, 11, 11, 0), "anne_cleves", to=["henry"],
             subject="With no hard feeling",
             category="narrative", subcategory="cleves", storyline="Cleves",
             body=compose(
                 "Your Majesty,",
                 ["I accept the judgement freely and gladly. I would far rather be Your Majesty's "
                  "beloved sister than an unhappy wife. England suits me, and I find I am very fond "
                  "of it.",
                  "Let us be friends. I hear the hunting at Richmond is excellent."],
                 "Your affectionate sister,", "Anne of Cleves")),
    ], "cleves-annulment")
    return out


# ==========================================================================
# STORYLINE 5 — THE HOWARD AFFAIR  (1540-1542)  *** central investigation ***
# ==========================================================================
def howard_affair() -> list[Email]:
    """The smoking-gun storyline: concealed correspondence over personal web-mail,
    a go-between, a love-letter attachment, spoliation hints, and the discovery."""
    out: list[Email] = []

    # Lady Rochford brokers the meetings (collected from Catherine Howard's mailbox).
    out += thread([
        mail("hwd", at(1541, 4, 28, 22, 10), "rochford", to=["catherine_howard"],
             subject="The arrangements for Thursday",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             confidentiality="", hot=True, custodian="catherine_howard",
             body=compose(
                 "Madam,",
                 ["All is made ready as you asked. The back stair will be unwatched after the "
                  "household sleeps, and I will keep the door myself.",
                  "Master Culpeper will come when the King rides out to hunt. Send word by me only — "
                  "trust nothing to the ordinary post, and keep nothing in writing that you would "
                  "not wish read aloud."],
                 "Your faithful servant,", "Jane Rochford")),
        mail("hwd", at(1541, 4, 29, 6, 45), "catherine_howard", to=["rochford"],
             subject="Re: The arrangements for Thursday",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             hot=True, custodian="catherine_howard",
             body=compose(
                 "Jane,",
                 ["You are a comfort to me. Thursday then, when the King hunts. Burn this once you "
                  "have read it, as I shall burn yours.",
                  "Say to him only that I count the hours."],
                 "C.H.", "")),
    ], "howard-arrangements")

    # The concealed correspondence over personal web-mail + the love-letter attachment.
    letter = doc("docx", "For_Your_Eyes_Only.docx",
                 "For Your Eyes Only",
                 author="catherine_howard", created=at(1541, 5, 3, 23, 0),
                 storyline="Howard Affair", hot=True,
                 spec=dict(paragraphs=[
                     "Master Culpeper,",
                     "I never longed so much for anything as I do to see you again. It troubles my "
                     "heart to think I cannot always be in your company.",
                     "Come when the King hunts, as we agreed, and come quietly. Lady Rochford will "
                     "keep the stair. When you have read this, do as I bid the others — let the fire "
                     "have it.",
                     "Yours as long as life endures,",
                     "C."],
                     closing="(Do not keep this. I mean it.)"))
    out += thread([
        mail("hwd", at(1541, 5, 3, 23, 20), ("catherine_howard", "kitty.h@ravenmail.tudor"),
             to=[("culpeper", "t.culpeper@ravenmail.tudor")],
             subject="(no subject)",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             confidentiality="", hot=True, custodian="catherine_howard",
             attachments=[letter],
             body=("Read what I have written and then let the fire have it.\n"
                   "Do not write my name. Do not keep my letters.\n— C.\n")),
        mail("hwd", at(1541, 5, 4, 5, 30), ("culpeper", "t.culpeper@ravenmail.tudor"),
             to=[("catherine_howard", "kitty.h@ravenmail.tudor")],
             subject="Re: (no subject)",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             hot=True, custodian="catherine_howard",
             body=("I have read it twice and cannot bring myself to burn it. I will be careful.\n"
                   "Thursday, when he rides out. Tell Jane I am grateful.\n— T.\n")),
    ], "howard-letters")

    # Dereham's leverage over the past (veiled, client-safe).
    out.append(mail("hwd", at(1541, 6, 9, 13, 0), "dereham", to=["catherine_howard"],
                    subject="An old friend",
                    category="narrative", subcategory="howard_affair", storyline="Howard Affair",
                    hot=True, custodian="catherine_howard",
                    body=compose(
                        "Madam,",
                        ["You have risen very high, and I am glad of it. I ask only a small place at "
                         "court, in memory of the friendship we shared before your marriage.",
                         "I am sure neither of us wishes old letters and older promises to be the "
                         "talk of the household. A secretaryship would settle the matter handsomely."],
                        "Your old friend,", "Francis Dereham")))

    # The discovery — collected naturally from custodian mailboxes (Cranmer/Henry).
    deposition = doc("pdf", "Confidential_Deposition_Summary.pdf",
                     "Summary of Information Received — Confidential",
                     author="cranmer", created=at(1541, 11, 1, 21, 0), confidentiality=CONF,
                     storyline="Howard Affair", hot=True,
                     spec=dict(paragraphs=[
                         "An informant has come forward with matter touching the Queen's conduct "
                         "before and during her marriage. The information concerns Francis Dereham, "
                         "lately appointed her secretary, and Thomas Culpeper of the Privy Chamber.",
                         "It is alleged that meetings were arranged by a lady of the bedchamber while "
                         "the court was on progress in the North, and that correspondence passed by a "
                         "private hand to avoid the household post.",
                         "Given the gravity, this is laid before the King in writing only because it "
                         "cannot in conscience be spoken aloud."],
                         closing="Submitted in strict confidence to His Majesty."))
    out += thread([
        mail("hwd", at(1541, 11, 2, 7, 0), "cranmer", to=["henry"],
             subject="A matter I cannot bring myself to speak — for Your Majesty alone",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             importance="High", confidentiality=CONF, hot=True, attachments=[deposition],
             body=compose(
                 "Your Majesty,",
                 ["It is with the greatest sorrow that I lay the enclosed before you. I could not "
                  "speak it to your face, and so I have set it down. I pray it proves false.",
                  "I have told no one else and committed nothing further to writing."],
                 "In sorrow and duty,", "T. Cranmer")),
        mail("hwd", at(1541, 11, 6, 9, 0), "henry", to=["cranmer"], cc=["rich", "gardiner"],
             subject="Re: A matter I cannot bring myself to speak",
             category="narrative", subcategory="howard_affair", storyline="Howard Affair",
             importance="High", confidentiality=CONF,
             body=compose(
                 "Cranmer,",
                 ["Examine it to the bottom, and quietly, before the court takes the scent. Question "
                  "the lady of the bedchamber first; the go-between always knows the most.",
                  "Recover every letter. I will not be made a jest of in my own household."],
                 "Henry R.", "")),
    ], "howard-discovery")

    # The investigation closes (examination transcript family).
    examination = doc("docx", "Examination_Transcript.docx",
                      "Record of Examination — Crown Matter",
                      author="rich", created=at(1541, 11, 12, 7, 0), confidentiality=PRIV_WP,
                      storyline="Howard Affair", hot=True,
                      spec=dict(paragraphs=[
                          "Examination taken before the King's Commissioners.",
                          "The lady of the bedchamber acknowledges that she carried messages and kept "
                          "watch at the stair, but says she did so at the Queen's command and dared "
                          "not refuse.",
                          "Master Culpeper acknowledges meetings and the receipt of letters, which he "
                          "says he did not destroy. Letters have been recovered and are held as "
                          "evidence.",
                          "The matter is sufficiently proven to proceed."],
                          closing="Certified a true record. — R. Rich"))
    out.append(mail("hwd", at(1541, 11, 13, 8, 0), "rich", to=["cranmer", "henry"],
                    subject="Examination concluded — record enclosed",
                    category="narrative", subcategory="howard_affair", storyline="Howard Affair",
                    importance="High", confidentiality=PRIV_WP, hot=True, attachments=[examination],
                    body=compose(
                        "Your Majesty, my lord Archbishop,",
                        ["The examinations are concluded and the record is enclosed. The go-between "
                         "kept the stair; the letters were not burned as the Queen had instructed, "
                         "and have been recovered. The matter is proven."],
                        "Your servant,", "Ric. Rich")))
    return out


# ==========================================================================
# STORYLINE 6 — SUCCESSION AND LEGACY  (1543-1547)
# ==========================================================================
def succession() -> list[Email]:
    out: list[Email] = []

    out += thread([
        mail("suc", at(1543, 7, 4, 10, 0), "henry", to=["catherine_parr"],
             subject="A question I will ask but once",
             category="narrative", subcategory="succession", storyline="Succession",
             body=compose(
                 "Madam,",
                 ["I am not the easy husband I once was, and you know better than most what the post "
                  "has cost its holders. Yet I find I want a wife of sense and kindness more than I "
                  "want another beauty.",
                  "Will you have me, and help me set my house and my children in order?"],
                 "Henry R.", "")),
        mail("suc", at(1543, 7, 6, 9, 0), "catherine_parr", to=["henry"],
             subject="Re: A question I will ask but once",
             category="narrative", subcategory="succession", storyline="Succession",
             body=compose(
                 "Your Majesty,",
                 ["It would be far better to be your wife than to refuse a king, and far better "
                  "still because I believe I can do some good for your children. I will have you, "
                  "and I will keep my head about me while I do."],
                 "Your obedient Catherine", "")),
    ], "succession-proposal")

    education = doc("xlsx", "Royal_Household_Education_Plan.xlsx",
                    "Plan for the Education of the King's Children",
                    author="catherine_parr", created=at(1544, 2, 10, 8, 0), modified=at(1544, 2, 14, 17, 0),
                    storyline="Succession",
                    spec=dict(sheet="Tutors",
                              headers=["Child", "Subject", "Tutor", "Hours/Week"],
                              rows=[
                                  ["Prince Edward", "Latin & Greek", "Dr Cheke", 12],
                                  ["Prince Edward", "Divinity", "Dr Cox", 6],
                                  ["Lady Elizabeth", "Languages", "Mr Grindal", 10],
                                  ["Lady Elizabeth", "Music", "Mr Bird", 4],
                                  ["Lady Mary", "Classics", "Self-directed", 8],
                              ],
                              note="For Their Majesties' approval."))
    out.append(mail("suc", at(1544, 2, 15, 11, 0), "catherine_parr", to=["henry"], cc=["mary"],
                    subject="The children's education — plan enclosed",
                    category="narrative", subcategory="succession", storyline="Succession",
                    attachments=[education],
                    body=compose(
                        "Your Majesty,",
                        ["I enclose a plan for the children's learning. Edward thrives at his books, "
                         "Elizabeth outpaces her tutors, and I have asked the Lady Mary to join us "
                         "more often. A household at peace is worth a province.",
                         "I should be glad of Your Majesty's approval."],
                        "Your loving Catherine", "")))

    # Parr's near-brush with the religious conservatives (she talks her way out).
    out += thread([
        mail("suc", at(1546, 7, 9, 19, 0), "gardiner", to=["henry"],
             subject="Concerning certain books in the Queen's chamber",
             category="narrative", subcategory="succession", storyline="Succession",
             confidentiality=CONF,
             body=compose(
                 "Your Majesty,",
                 ["It is my duty, however unwelcome, to note that certain reformist books have been "
                  "seen in the Queen's apartments, and that Her Majesty debates points of religion "
                  "more freely than is perhaps seemly.",
                  "I raise it only that Your Majesty may judge."],
                 "Your servant,", "S. Gardiner")),
        mail("suc", at(1546, 7, 11, 16, 0), "catherine_parr", to=["henry"],
             subject="A wife's poor opinions",
             category="narrative", subcategory="succession", storyline="Succession",
             body=compose(
                 "Your Majesty,",
                 ["If I have debated with you, it was only to take your mind off your bad leg, and "
                  "to be set right by your greater learning, as a wife should. I am a woman, with "
                  "all the imperfections of my sex, and look to Your Majesty for instruction.",
                  "I would never presume to teach where I ought to learn."],
                 "Your humble Catherine", "")),
        mail("suc", at(1546, 7, 12, 9, 0), "henry", to=["gardiner"], cc=["catherine_parr"],
             subject="Re: Concerning certain books in the Queen's chamber",
             category="narrative", subcategory="succession", storyline="Succession",
             body=compose(
                 "Gardiner,",
                 ["You have been misinformed. The Queen and I are perfectly agreed, and I find her "
                  "conversation a tonic. Trouble yourself with your diocese and not with my wife's "
                  "bookshelf.",
                  "The matter is closed."],
                 "Henry R.", "")),
    ], "succession-parr-books")

    # The king's decline and the succession (privileged memorandum family).
    will = doc("pdf", "Memorandum_on_the_Succession.pdf",
               "Memorandum on the Order of Succession",
               author="cranmer", created=at(1546, 12, 26, 7, 0), confidentiality=PRIV_AC,
               storyline="Succession", hot=True,
               spec=dict(paragraphs=[
                   "PRIVILEGED. Pursuant to the Act of Succession, the Crown is to descend first to "
                   "Prince Edward and the heirs of his body.",
                   "Failing such heirs, to the Lady Mary, and failing her, to the Lady Elizabeth, "
                   "each on the conditions the Act prescribes.",
                   "A council of regency is named to govern during the minority of Prince Edward. "
                   "This advice is privileged and prepared for the King alone."],
                   closing="Respectfully submitted. — T. Cranmer"))
    out.append(mail("suc", at(1546, 12, 27, 10, 0), "cranmer", to=["henry"], cc=["seymour_edward"],
                    subject="The succession — privileged memorandum enclosed",
                    category="narrative", subcategory="succession", storyline="Succession",
                    importance="High", confidentiality=PRIV_AC, hot=True, attachments=[will],
                    body=compose(
                        "Your Majesty,",
                        ["As Your Majesty bid me, I enclose the privileged memorandum on the "
                         "succession and the council of regency. It is for Your Majesty's eyes, and "
                         "those Your Majesty names, alone."],
                        "Your devoted servant,", "T. Cranmer")))
    out.append(mail("suc", at(1547, 1, 27, 22, 0), "catherine_parr", to=["mary", "seymour_edward"],
                    subject="The King",
                    category="narrative", subcategory="succession", storyline="Succession",
                    importance="High",
                    body=compose(
                        "Dear ones,",
                        ["The King is very low and will not see the morning, I fear. Come quietly and "
                         "say your farewells. Whatever has passed between us all, we are a family "
                         "tonight, and nothing else.",
                         "Be brave for Edward. The weight that is coming will fall hardest on the "
                         "smallest shoulders."],
                        "Catherine", "")))
    return out


# ==========================================================================
# FOREIGN-LANGUAGE DOCUMENTS  (the translation exercise)
# ==========================================================================
def foreign_language() -> list[Email]:
    """A few genuine, client-safe foreign-language documents: a Spanish appeal,
    a Latin papal citation, and a French diplomatic note."""
    out: list[Email] = []

    # Spanish — Catherine of Aragon writes to the King in her native tongue.
    out.append(mail("fl", at(1529, 6, 18, 9, 0), "aragon", to=["henry"], cc=["chapuys"],
                    subject="De vuestra fiel esposa",
                    category="narrative", subcategory="foreign_language",
                    storyline="The Great Matter", hot=False,
                    body=(
                        "Señor, mi esposo y mi rey,\n\n"
                        "Os escribo en mi propia lengua para que sintáis cuán de corazón os hablo. "
                        "He sido siempre vuestra leal y humilde esposa, y vine a vos doncella. No "
                        "consentiré en cosa que toque mi honra ni el derecho de nuestra hija doña "
                        "María.\n\n"
                        "Haced lo que vuestra conciencia os dicte, pero sabed que la mía está limpia "
                        "delante de Dios. Que Él os guarde y os dé buen consejo.\n\n"
                        "Vuestra fiel esposa,\nCatalina\n")))

    # Latin — the citation from Rome, attached for the King's scholars to construe.
    citation = doc("pdf", "Citatio_Apostolica.pdf", "Citatio Apostolica",
                   author="cranmer", created=at(1530, 3, 1, 7, 0), confidentiality=CONF,
                   storyline="The Great Matter",
                   spec=dict(paragraphs=[
                       "In nomine Domini nostri Iesu Christi, amen.",
                       "Sanctissimus in Christo Pater et Dominus Noster, divina providentia Papa, "
                       "auditis allegationibus partium in causa matrimoniali inter Serenissimum "
                       "Regem Angliae et Serenissimam Reginam Catharinam mota, mandat et praecipit "
                       "ut causa ipsa Romae, apud Sedem Apostolicam, cognoscatur atque definiatur.",
                       "Datum Romae, apud Sanctum Petrum, sub anno Incarnationis Dominicae "
                       "millesimo quingentesimo tricesimo."],
                       closing="Sub plumbo, ut moris est."))
    out.append(mail("fl", at(1530, 3, 20, 10, 0), "cromwell", to=["henry", "cranmer"],
                    subject="The citation from Rome (in Latin)",
                    category="narrative", subcategory="foreign_language",
                    storyline="The Great Matter", confidentiality=CONF, attachments=[citation],
                    body=compose(
                        "Your Majesty, my lord Archbishop,",
                        ["The long-awaited instrument has arrived from Rome. It is in Latin, as "
                         "ever, and I attach it for the King's scholars to construe at leisure.",
                         "The short of it is this: Rome insists the cause be heard there, and not "
                         "here. I need hardly say how Your Majesty will receive that news."],
                        "Your servant,", "Thomas Cromwell")))

    # French — a note from the French embassy (diplomatic lingua franca).
    out.append(mail("fl", at(1532, 9, 5, 14, 0),
                    ("Ambassadeur de France", "ambassade@france.gov.tudor"),
                    to=["henry"], cc=["cromwell"],
                    subject="Compliments du Roi Très-Chrétien",
                    category="narrative", subcategory="foreign_language",
                    storyline="The Great Matter",
                    body=(
                        "Sire,\n\n"
                        "J'ai l'honneur de transmettre à Votre Majesté les compliments très cordiaux "
                        "du Roi Très-Chrétien, mon maître. Il souhaite la continuation de l'amitié "
                        "ancienne entre nos deux royaumes et propose une entrevue à Calais avant "
                        "l'hiver.\n\n"
                        "Je demeure le très humble et très obéissant serviteur de Votre Majesté.\n\n"
                        "L'Ambassadeur de France\n")))
    return out


def all_scenes() -> list[Email]:
    return (
        great_matter()
        + anne_boleyn()
        + dissolution()
        + cleves()
        + howard_affair()
        + succession()
        + foreign_language()
    )
