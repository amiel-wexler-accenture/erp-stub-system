from faker import Faker
import random
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from .base import BaseProfile

metadata = MetaData()

lfa1 = Table("LFA1", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("LAND1", String(255)),
    Column("NAME1", String(255)),
    Column("NAME2", String(255)),
    Column("NAME3", String(255)),
    Column("NAME4", String(255)),
    Column("ORT01", String(255)),
    Column("ORT02", String(255)),
    Column("PFACH", String(255)),
    Column("PSTL2", String(255)),
    Column("PSTLZ", String(255)),
    Column("REGIO", String(255)),
    Column("SORTL", String(255)),
    Column("STRAS", String(255)),
    Column("ADRNR", String(255)),
    Column("MCOD1", String(255)),
    Column("MCOD2", String(255)),
    Column("MCOD3", String(255)),
    Column("ANRED", String(255)),
    Column("BAHNS", String(255)),
    Column("BBBNR", String(255)),
    Column("BBSNR", String(255)),
    Column("BEGRU", String(255)),
    Column("BRSCH", String(255)),
    Column("BUBKZ", String(255)),
    Column("DATLT", String(255)),
    Column("DTAMS", String(255)),
    Column("DTAWS", String(255)),
    Column("ERDAT", String(255)),
    Column("ERNAM", String(255)),
    Column("ESRNR", String(255)),
    Column("KONZS", String(255)),
    Column("KTOKK", String(255)),
    Column("KUNNR", String(255)),
    Column("LNRZA", String(255)),
    Column("LOEVM", String(255)),
    Column("SPERR", String(255)),
    Column("SPERM", String(255)),
    Column("SPRAS", String(255)),
    Column("STCD1", String(255)),
    Column("STCD2", String(255)),
    Column("STKZA", String(255)),
    Column("STKZU", String(255)),
    Column("TELBX", String(255)),
    Column("TELF1", String(255)),
    Column("TELF2", String(255)),
    Column("TELFX", String(255)),
    Column("TELTX", String(255)),
    Column("TELX1", String(255)),
    Column("XCPDK", String(255)),
    Column("XZEMP", String(255)),
    Column("VBUND", String(255)),
    Column("FISKN", String(255)),
    Column("STCEG", String(255)),
    Column("STKZN", String(255)),
    Column("SPERQ", String(255)),
    Column("GBORT", String(255)),
    Column("GBDAT", String(255)),
    Column("SEXKZ", String(255)),
    Column("KRAUS", String(255)),
    Column("REVDB", String(255)),
    Column("QSSYS", String(255)),
    Column("KTOCK", String(255)),
    Column("PFORT", String(255)),
    Column("WERKS", String(255)),
    Column("LTSNA", String(255)),
    Column("WERKR", String(255)),
    Column("PLKAL", String(255)),
    Column("DUEFL", String(255)),
    Column("TXJCD", String(255)),
    Column("SPERZ", String(255)),
    Column("SCACD", String(255)),
    Column("SFRGR", String(255)),
    Column("LZONE", String(255)),
    Column("XLFZA", String(255)),
    Column("DLGRP", String(255)),
    Column("STCD3", String(255)),
    Column("STCD4", String(255)),
    Column("STCD5", String(255)),
    Column("PROFS", String(255)),
    Column("EMNFR", String(255)),
    Column("LFURL", String(255)),
    Column("CONFS", String(255)),
    Column("UPDAT", String(255)),
    Column("UPTIM", String(255)),
    Column("NODEL", String(255)),
    Column("PODKZB", String(255)),
)

lfb1 = Table("LFB1", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("BUKRS", String(255)),
    Column("PERNR", String(255)),
    Column("ALTKN", String(255)),
    Column("BEGRU", String(255)),
    Column("ZUAWA", String(255)),
    Column("AKONT", String(255)),
    Column("ALTKT", String(255)),
    Column("ALTKN2", String(255)),
    Column("ZTERM", String(255)),
    Column("WAERS", String(255)),
    Column("FDGRP", String(255)),
    Column("REPRF", String(255)),
    Column("TOGRP", String(255)),
    Column("LNRZE", String(255)),
    Column("LNRZB", String(255)),
    Column("ZINDT", String(255)),
    Column("ZINRT", String(255)),
    Column("DATLZ", String(255)),
    Column("ALTKZ", String(255)),
    Column("MINDK", String(255)),
    Column("INTAD", String(255)),
    Column("KVERM", String(255)),
    Column("BUSAB", String(255)),
    Column("UBBZG", String(255)),
    Column("EXPKK", String(255)),
    Column("ABSBE", String(255)),
    Column("ZFBDT", String(255)),
    Column("SKFOR", String(255)),
    Column("SKNTO", String(255)),
    Column("MANDT_OVERRIDE", String(255)),
)

lfbk = Table("LFBK", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("BANKS", String(255)),
    Column("BANKL", String(255)),
    Column("BANKN", String(255)),
    Column("BKONT", String(255)),
    Column("BVTYP", String(255)),
    Column("XEZER", String(255)),
    Column("BANKA", String(255)),
    Column("PROVZ", String(255)),
    Column("STRAS", String(255)),
    Column("ORT01", String(255)),
    Column("SWIFT", String(255)),
    Column("IBAN", String(255)),
    Column("KOINH", String(255)),
    Column("KOVON", String(255)),
    Column("KOBIS", String(255)),
)

lfas = Table("LFAS", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("EKORG", String(255)),
    Column("SPERM", String(255)),
    Column("LOEVM", String(255)),
    Column("VENSL", String(255)),
    Column("BSTAE", String(255)),
)

lfm1 = Table("LFM1", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("EKORG", String(255)),
    Column("WAERS", String(255)),
    Column("LIEFR", String(255)),
    Column("MINBW", String(255)),
    Column("KZABS", String(255)),
    Column("KZAUT", String(255)),
    Column("KZBESN", String(255)),
    Column("MEPRF", String(255)),
    Column("INCO1", String(255)),
    Column("INCO2", String(255)),
    Column("WEBRE", String(255)),
    Column("KZWBK", String(255)),
    Column("BOAUF", String(255)),
    Column("BOKRE", String(255)),
    Column("BOSPE", String(255)),
    Column("BOSTA", String(255)),
    Column("BOSPE2", String(255)),
    Column("UMSAE", String(255)),
)

lfm2 = Table("LFM2", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("EKORG", String(255)),
    Column("WERKS", String(255)),
    Column("SPERM", String(255)),
    Column("LOEVM", String(255)),
    Column("PLIFZ", String(255)),
    Column("MNGLG", String(255)),
    Column("MNGKO", String(255)),
    Column("MNGZE", String(255)),
    Column("UEBTO", String(255)),
    Column("UNTTO", String(255)),
    Column("UGBTO", String(255)),
)

lfb5 = Table("LFB5", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("BUKRS", String(255)),
    Column("MABER", String(255)),
    Column("MAHNS", String(255)),
    Column("MANDT2", String(255)),
)

lfbw = Table("LFBW", metadata,
    Column("MANDT", String(255)),
    Column("LIFNR", String(255)),
    Column("BUKRS", String(255)),
    Column("WITHT", String(255)),
    Column("WT_WITHCD", String(255)),
    Column("WT_EXPT", String(255)),
    Column("QSREC", String(255)),
    Column("WITHT2", String(255)),
)

kna1 = Table("KNA1", metadata,
    Column("MANDT", String(255)),
    Column("KUNNR", String(255)),
    Column("LAND1", String(255)),
    Column("NAME1", String(255)),
    Column("NAME2", String(255)),
    Column("NAME3", String(255)),
    Column("NAME4", String(255)),
    Column("ORT01", String(255)),
    Column("ORT02", String(255)),
    Column("PSTLZ", String(255)),
    Column("REGIO", String(255)),
    Column("SORTL", String(255)),
    Column("STRAS", String(255)),
    Column("TELF1", String(255)),
    Column("TELF2", String(255)),
    Column("TELFX", String(255)),
    Column("TELTX", String(255)),
    Column("XCPDK", String(255)),
    Column("STCD1", String(255)),
    Column("STCD2", String(255)),
    Column("STKZU", String(255)),
    Column("ERDAT", String(255)),
    Column("ERNAM", String(255)),
    Column("KTOKD", String(255)),
    Column("SPRAS", String(255)),
    Column("ANRED", String(255)),
    Column("MCOD1", String(255)),
    Column("MCOD2", String(255)),
    Column("MCOD3", String(255)),
    Column("LOEVM", String(255)),
    Column("SPERR", String(255)),
)

knb1 = Table("KNB1", metadata,
    Column("MANDT", String(255)),
    Column("KUNNR", String(255)),
    Column("BUKRS", String(255)),
    Column("AKONT", String(255)),
    Column("ZTERM", String(255)),
    Column("WAERS", String(255)),
    Column("ZUAWA", String(255)),
    Column("BEGRU", String(255)),
    Column("ALTKN", String(255)),
    Column("REPRF", String(255)),
)

knvv = Table("KNVV", metadata,
    Column("MANDT", String(255)),
    Column("KUNNR", String(255)),
    Column("VKORG", String(255)),
    Column("VTWEG", String(255)),
    Column("SPART", String(255)),
    Column("BZIRK", String(255)),
    Column("VKBUR", String(255)),
    Column("KDGRP", String(255)),
    Column("WAERS", String(255)),
    Column("ZTERM", String(255)),
    Column("INCO1", String(255)),
    Column("INCO2", String(255)),
    Column("KVGR1", String(255)),
    Column("KVGR2", String(255)),
    Column("KVGR3", String(255)),
    Column("KVGR4", String(255)),
    Column("KVGR5", String(255)),
)

knbk = Table("KNBK", metadata,
    Column("MANDT", String(255)),
    Column("KUNNR", String(255)),
    Column("BANKS", String(255)),
    Column("BANKL", String(255)),
    Column("BANKN", String(255)),
    Column("BKONT", String(255)),
    Column("BVTYP", String(255)),
    Column("XEZER", String(255)),
    Column("BANKA", String(255)),
    Column("SWIFT", String(255)),
    Column("IBAN", String(255)),
)

mara = Table("MARA", metadata,
    Column("MANDT", String(255)),
    Column("MATNR", String(255)),
    Column("ERSDA", String(255)),
    Column("ERNAM", String(255)),
    Column("LAEDA", String(255)),
    Column("AENAM", String(255)),
    Column("MTART", String(255)),
    Column("MBRSH", String(255)),
    Column("MATKL", String(255)),
    Column("MEINS", String(255)),
    Column("BSTME", String(255)),
    Column("ZEINR", String(255)),
    Column("ZEIVR", String(255)),
    Column("ZEIFO", String(255)),
    Column("AESZN", String(255)),
    Column("BLANZ", String(255)),
    Column("FERTH", String(255)),
    Column("FORMT", String(255)),
    Column("NORMT", String(255)),
    Column("LABOR", String(255)),
    Column("EKWSL", String(255)),
    Column("BRGEW", String(255)),
    Column("GEWEI", String(255)),
    Column("NTGEW", String(255)),
    Column("VOLUM", String(255)),
    Column("VOLEH", String(255)),
    Column("BEHVO", String(255)),
    Column("RAUBE", String(255)),
    Column("TEMPB", String(255)),
    Column("DISST", String(255)),
    Column("TRAGR", String(255)),
    Column("STOFF", String(255)),
    Column("SPART", String(255)),
    Column("VHART", String(255)),
    Column("FUELG", String(255)),
    Column("IPRKZ", String(255)),
    Column("RDPRF", String(255)),
    Column("MHDRZ", String(255)),
    Column("MHDLP", String(255)),
    Column("MHDLF", String(255)),
    Column("BWVOR", String(255)),
    Column("BWSCL", String(255)),
    Column("SAISO", String(255)),
    Column("ETIAR", String(255)),
    Column("ETIFO", String(255)),
    Column("ENTAR", String(255)),
    Column("EAN11", String(255)),
    Column("NUMTP", String(255)),
    Column("LAENG", String(255)),
    Column("BREIT", String(255)),
    Column("HOEHE", String(255)),
    Column("MEABM", String(255)),
    Column("PRDHA", String(255)),
    Column("CADKZ", String(255)),
    Column("ERGEW", String(255)),
    Column("ERVOLM", String(255)),
    Column("WERKS", String(255)),
    Column("LMEINS", String(255)),
    Column("BRGEW2", String(255)),
    Column("GEWEI2", String(255)),
)

marc = Table("MARC", metadata,
    Column("MANDT", String(255)),
    Column("MATNR", String(255)),
    Column("WERKS", String(255)),
    Column("PSTAT", String(255)),
    Column("LVORM", String(255)),
    Column("BWTTY", String(255)),
    Column("XCHAR", String(255)),
    Column("MMSTA", String(255)),
    Column("MMSTD", String(255)),
    Column("MAABC", String(255)),
    Column("KZKRI", String(255)),
    Column("EKGRP", String(255)),
    Column("DISMM", String(255)),
    Column("DISPO", String(255)),
    Column("DISLS", String(255)),
    Column("BERID", String(255)),
    Column("BSTMI", String(255)),
    Column("MINBE", String(255)),
    Column("EISBE", String(255)),
    Column("MABST", String(255)),
    Column("STRGR", String(255)),
    Column("LGPRO", String(255)),
    Column("LGFSB", String(255)),
    Column("HERKL", String(255)),
    Column("INSMK", String(255)),
    Column("SSQSS", String(255)),
    Column("MTVFP", String(255)),
    Column("KZAUS", String(255)),
    Column("AUSDT", String(255)),
    Column("NFMAT", String(255)),
    Column("MFLHN", String(255)),
    Column("KZBED", String(255)),
    Column("LGPBE", String(255)),
    Column("LGOBE", String(255)),
    Column("INSMK2", String(255)),
)

makt = Table("MAKT", metadata,
    Column("MANDT", String(255)),
    Column("MATNR", String(255)),
    Column("SPRAS", String(255)),
    Column("MAKTX", String(255)),
    Column("MAKTG", String(255)),
)

ska1 = Table("SKA1", metadata,
    Column("MANDT", String(255)),
    Column("KTOPL", String(255)),
    Column("SAKNR", String(255)),
    Column("BILKT", String(255)),
    Column("ERDAT", String(255)),
    Column("ERNAM", String(255)),
    Column("GVTYP", String(255)),
    Column("KTOKS", String(255)),
    Column("MUSTR", String(255)),
    Column("VBUND", String(255)),
    Column("XBILK", String(255)),
    Column("XLOEV", String(255)),
    Column("XSPEA", String(255)),
    Column("XSPEB", String(255)),
    Column("XUMSA", String(255)),
)

skat = Table("SKAT", metadata,
    Column("MANDT", String(255)),
    Column("SPRAS", String(255)),
    Column("KTOPL", String(255)),
    Column("SAKNR", String(255)),
    Column("TXT20", String(255)),
    Column("TXT50", String(255)),
)

csks = Table("CSKS", metadata,
    Column("MANDT", String(255)),
    Column("KOSTL", String(255)),
    Column("DATBI", String(255)),
    Column("DATAB", String(255)),
    Column("BKLAS", String(255)),
    Column("BUKRS", String(255)),
    Column("GSBER", String(255)),
    Column("KOKRS", String(255)),
    Column("KOSTLV", String(255)),
    Column("KHINR", String(255)),
    Column("KOSAR", String(255)),
    Column("VERAK", String(255)),
    Column("VERAK2", String(255)),
    Column("KTEXT", String(255)),
    Column("LTEXT", String(255)),
    Column("FUNC_AREA", String(255)),
)

ekko = Table("EKKO", metadata,
    Column("MANDT", String(255)),
    Column("EBELN", String(255)),
    Column("BUKRS", String(255)),
    Column("BSART", String(255)),
    Column("LIFNR", String(255)),
    Column("EKORG", String(255)),
    Column("EKGRP", String(255)),
    Column("WAERS", String(255)),
    Column("WKURS", String(255)),
    Column("KUFIX", String(255)),
    Column("BEDAT", String(255)),
    Column("KDATB", String(255)),
    Column("KDATE", String(255)),
    Column("KDATV", String(255)),
    Column("ABGRU", String(255)),
    Column("AUTLF", String(255)),
    Column("WEAKT", String(255)),
    Column("MEMORY", String(255)),
    Column("KZABS", String(255)),
    Column("RLWRT", String(255)),
    Column("ZTERM", String(255)),
    Column("ZBD1T", String(255)),
    Column("ZBD2T", String(255)),
    Column("ZBD3T", String(255)),
    Column("ZBD1P", String(255)),
    Column("ZBD2P", String(255)),
    Column("MWSKZ", String(255)),
    Column("IHREZ", String(255)),
    Column("VERKF", String(255)),
    Column("EXNUM", String(255)),
    Column("UNSEZ", String(255)),
    Column("INCO1", String(255)),
    Column("INCO2", String(255)),
    Column("KONNR", String(255)),
    Column("KTPNR", String(255)),
    Column("ABTYP", String(255)),
    Column("WGLIF", String(255)),
    Column("KNUMV", String(255)),
)

ekpo = Table("EKPO", metadata,
    Column("MANDT", String(255)),
    Column("EBELN", String(255)),
    Column("EBELP", String(255)),
    Column("MATNR", String(255)),
    Column("WERKS", String(255)),
    Column("LGORT", String(255)),
    Column("MATKL", String(255)),
    Column("INFNR", String(255)),
    Column("IDNLF", String(255)),
    Column("KTMNG", String(255)),
    Column("MENGE", String(255)),
    Column("MEINS", String(255)),
    Column("BPRME", String(255)),
    Column("BPUMZ", String(255)),
    Column("BPUMN", String(255)),
    Column("NETPR", String(255)),
    Column("PEINH", String(255)),
    Column("NETWR", String(255)),
    Column("BRTWR", String(255)),
    Column("BUGSZ", String(255)),
    Column("RETPO", String(255)),
    Column("WEPOS", String(255)),
    Column("WEUNB", String(255)),
    Column("REPOS", String(255)),
    Column("MWSKZ", String(255)),
    Column("ADRNR", String(255)),
    Column("PACKNO", String(255)),
    Column("FPLNR", String(255)),
    Column("BELNR", String(255)),
    Column("LOEKZ", String(255)),
    Column("BANFN", String(255)),
    Column("BNFPO", String(255)),
    Column("EBELN2", String(255)),
    Column("EBELP2", String(255)),
)

_ALL_TABLES = [
    lfa1, lfb1, lfbk, lfas, lfm1, lfm2, lfb5, lfbw,
    kna1, knb1, knvv, knbk,
    mara, marc, makt,
    ska1, skat, csks,
    ekko, ekpo,
]

_UNICODE_NAMES = [
    "Müller GmbH",
    "Société Générale",
    "日本電気株式会社",
    "شركة أرامكو السعودية",
]

_VALID_COUNTRIES = [
    "US", "DE", "GB", "FR", "JP", "BR", "CN", "CA", "AU", "IT",
    "ES", "NL", "SE", "CH", "AT", "BE", "PL", "MX", "KR", "IN",
]
_INVALID_COUNTRIES = ["XX", "ZZ", "QQ"]

_VALID_BRSCH = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
]
_INVALID_BRSCH = ["999", "000", "XYZ"]

_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "BRL", "CHF", "CAD", "AUD", "CNY", "KRW"]
_EKORG_VALUES = ["1000", "2000", "3000", "4000", "5000"]
_BUKRS_VALUES = ["1000", "2000", "3000", "4000", "5000"]
_WERKS_VALUES = ["1000", "1001", "1002", "2000", "2001", "3000", "3001", "4000", "5000", "5001"]
_VKORG_VALUES = ["1000", "2000", "3000"]
_VTWEG_VALUES = ["10", "20", "30"]
_SPART_VALUES = ["00", "01", "02", "03", "04"]
_LANGUAGES = ["E", "D", "F", "J", "P"]
_MTART_VALUES = ["ROH", "HALB", "FERT", "HIBE", "VERP", "DIEN", "NLAG", "ERSA"]
_MEINS_VALUES = ["ST", "KG", "L", "M", "M2", "M3", "EA", "PC"]
_INCO1_VALUES = ["EXW", "FCA", "CPT", "CIP", "DAT", "DAP", "DDP", "FOB", "CFR", "CIF"]
_ZTERM_VALUES = ["0001", "0002", "0003", "NT30", "NT60", "NT90", "2/10NET30"]


def _ts(val: str) -> str:
    if val and random.random() < 0.20:
        return val + "   "
    return val


def _null_val():
    return random.choice([None, "", "N/A"])


def _erdat(fake: Faker) -> str:
    d = fake.date_between(start_date="-15y", end_date="today")
    if random.random() < 0.5:
        return d.strftime("%Y%m%d")
    else:
        return d.strftime("%d.%m.%Y")


def _mandt(base: str = "100") -> str:
    if random.random() < 0.005:
        return "200"
    return base


def _land1() -> str:
    if random.random() < 0.03:
        return random.choice(_INVALID_COUNTRIES)
    return random.choice(_VALID_COUNTRIES)


def _brsch() -> str:
    if random.random() < 0.03:
        return random.choice(_INVALID_BRSCH)
    return random.choice(_VALID_BRSCH)


def _name1(fake: Faker) -> str:
    if random.random() < 0.05:
        return random.choice(_UNICODE_NAMES)
    return fake.company()


class SapEccProfile(BaseProfile):

    @property
    def profile_id(self) -> str:
        return "sap_ecc"

    @property
    def system_name(self) -> str:
        return "ECC-1"

    @property
    def system_type(self) -> str:
        return "SAP ECC"

    @property
    def version(self) -> str:
        return "6.0 EHP8"

    @property
    def description(self) -> str:
        return "SAP ECC 6.0 EHP8 — legacy system with 15+ years of accumulated data"

    async def create_tables(self, engine: AsyncEngine) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def drop_tables(self, engine: AsyncEngine) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def seed_data(self, engine: AsyncEngine) -> None:
        fake = Faker(["en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "pt_BR"])
        Faker.seed(42)
        random.seed(42)

        async with engine.begin() as conn:
            # ── LFA1 ──────────────────────────────────────────────────────────
            lfa1_rows = []
            lifnr_list = []
            dup_names = []  # for near-duplicate DQ issue

            for n in range(1, 2001):
                lifnr_val = f"{n:010d}"
                lifnr_list.append(lifnr_val)
                mandt_val = _mandt()
                name1_val = _name1(fake)

                # DQ #3: near-duplicate (~2%)
                if n > 50 and random.random() < 0.02 and dup_names:
                    name1_val = random.choice(dup_names)
                else:
                    dup_names.append(name1_val)
                    if len(dup_names) > 100:
                        dup_names.pop(0)

                # DQ #8: blocked/deleted (~5%)
                loevm_val = "X" if random.random() < 0.05 else None

                # optional name fields DQ #2
                name2_val = _null_val() if random.random() < 0.30 else fake.company_suffix()
                name3_val = _null_val() if random.random() < 0.50 else fake.bs()[:20]
                name4_val = _null_val() if random.random() < 0.70 else None

                row = {
                    "MANDT": mandt_val,
                    "LIFNR": lifnr_val,
                    "LAND1": _land1(),
                    "NAME1": _ts(name1_val),
                    "NAME2": name2_val,
                    "NAME3": name3_val,
                    "NAME4": name4_val,
                    "ORT01": _ts(fake.city()),
                    "ORT02": _null_val() if random.random() < 0.40 else fake.city(),
                    "PFACH": _null_val() if random.random() < 0.60 else fake.postcode(),
                    "PSTL2": fake.postcode(),
                    "PSTLZ": fake.postcode(),
                    "REGIO": fake.state_abbr() if hasattr(fake, "state_abbr") else fake.bothify("??"),
                    "SORTL": _ts(name1_val[:10].upper()),
                    "STRAS": _ts(fake.street_address()),
                    "ADRNR": str(random.randint(100000, 999999)),
                    "MCOD1": _ts(name1_val[:25].upper()),
                    "MCOD2": None,
                    "MCOD3": None,
                    "ANRED": random.choice(["Firma", "Herr", "Frau", "Mr.", "Ms.", None]),
                    "BAHNS": None,
                    "BBBNR": _null_val() if random.random() < 0.70 else fake.numerify("########"),
                    "BBSNR": None,
                    "BEGRU": random.choice(["0001", "0002", "0003", None]),
                    "BRSCH": _brsch(),
                    "BUBKZ": None,
                    "DATLT": None,
                    "DTAMS": None,
                    "DTAWS": None,
                    "ERDAT": _erdat(fake),
                    "ERNAM": fake.user_name()[:12],
                    "ESRNR": None,
                    "KONZS": None,
                    "KTOKK": random.choice(["LIEF", "KRED", "0001"]),
                    "KUNNR": None,
                    "LNRZA": None,
                    "LOEVM": loevm_val,
                    "SPERR": None,
                    "SPERM": None,
                    "SPRAS": random.choice(_LANGUAGES),
                    "STCD1": _null_val() if random.random() < 0.20 else fake.numerify("##########"),
                    "STCD2": None,
                    "STKZA": None,
                    "STKZU": random.choice(["X", None]),
                    "TELBX": None,
                    "TELF1": _ts(fake.phone_number()[:16]),
                    "TELF2": _null_val() if random.random() < 0.60 else fake.phone_number()[:16],
                    "TELFX": _null_val() if random.random() < 0.50 else fake.phone_number()[:16],
                    "TELTX": None,
                    "TELX1": None,
                    "XCPDK": None,
                    "XZEMP": None,
                    "VBUND": None,
                    "FISKN": None,
                    "STCEG": _null_val() if random.random() < 0.30 else fake.numerify("DE###########"),
                    "STKZN": None,
                    "SPERQ": None,
                    "GBORT": None,
                    "GBDAT": None,
                    "SEXKZ": None,
                    "KRAUS": None,
                    "REVDB": None,
                    "QSSYS": None,
                    "KTOCK": None,
                    "PFORT": None,
                    "WERKS": random.choice(_WERKS_VALUES),
                    "LTSNA": None,
                    "WERKR": None,
                    "PLKAL": random.choice(["01", "02", "03", None]),
                    "DUEFL": None,
                    "TXJCD": None,
                    "SPERZ": None,
                    "SCACD": None,
                    "SFRGR": None,
                    "LZONE": None,
                    "XLFZA": None,
                    "DLGRP": None,
                    "STCD3": None,
                    "STCD4": None,
                    "STCD5": None,
                    "PROFS": None,
                    "EMNFR": None,
                    "LFURL": _null_val() if random.random() < 0.60 else fake.url(),
                    "CONFS": None,
                    "UPDAT": fake.date_between(start_date="-2y", end_date="today").strftime("%Y%m%d"),
                    "UPTIM": fake.time(pattern="%H%M%S"),
                    "NODEL": None,
                    "PODKZB": None,
                }
                lfa1_rows.append(row)

            for i in range(0, len(lfa1_rows), 500):
                await conn.execute(lfa1.insert(), lfa1_rows[i:i+500])

            # ── LFB1 ──────────────────────────────────────────────────────────
            lfb1_rows = []
            for n in range(3000):
                lifnr_val = random.choice(lifnr_list)
                bukrs_val = random.choice(_BUKRS_VALUES)
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": lifnr_val,
                    "BUKRS": bukrs_val,
                    "PERNR": None,
                    "ALTKN": None,
                    "BEGRU": random.choice(["0001", "0002", None]),
                    "ZUAWA": random.choice(["001", "002", "003"]),
                    "AKONT": fake.numerify("######"),
                    "ALTKT": None,
                    "ALTKN2": None,
                    "ZTERM": random.choice(_ZTERM_VALUES),
                    "WAERS": random.choice(_CURRENCIES),
                    "FDGRP": None,
                    "REPRF": None,
                    "TOGRP": None,
                    "LNRZE": None,
                    "LNRZB": None,
                    "ZINDT": None,
                    "ZINRT": None,
                    "DATLZ": None,
                    "ALTKZ": None,
                    "MINDK": None,
                    "INTAD": None,
                    "KVERM": None,
                    "BUSAB": fake.bothify("??"),
                    "UBBZG": None,
                    "EXPKK": None,
                    "ABSBE": None,
                    "ZFBDT": None,
                    "SKFOR": None,
                    "SKNTO": None,
                    "MANDT_OVERRIDE": None,
                }
                lfb1_rows.append(row)
            for i in range(0, len(lfb1_rows), 500):
                await conn.execute(lfb1.insert(), lfb1_rows[i:i+500])

            # ── LFBK ──────────────────────────────────────────────────────────
            lfbk_rows = []
            for n in range(2000):
                lifnr_val = random.choice(lifnr_list)
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": lifnr_val,
                    "BANKS": random.choice(_VALID_COUNTRIES),
                    "BANKL": fake.numerify("########"),
                    "BANKN": fake.numerify("##########"),
                    "BKONT": None,
                    "BVTYP": None,
                    "XEZER": None,
                    "BANKA": _ts(fake.company()),
                    "PROVZ": None,
                    "STRAS": _ts(fake.street_address()),
                    "ORT01": _ts(fake.city()),
                    "SWIFT": fake.swift(),
                    "IBAN": fake.iban(),
                    "KOINH": _null_val() if random.random() < 0.50 else fake.name(),
                    "KOVON": None,
                    "KOBIS": None,
                }
                lfbk_rows.append(row)
            for i in range(0, len(lfbk_rows), 500):
                await conn.execute(lfbk.insert(), lfbk_rows[i:i+500])

            # ── LFAS ──────────────────────────────────────────────────────────
            lfas_rows = []
            for n in range(2500):
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": random.choice(lifnr_list),
                    "EKORG": random.choice(_EKORG_VALUES),
                    "SPERM": None,
                    "LOEVM": None,
                    "VENSL": None,
                    "BSTAE": random.choice(["X", None]),
                }
                lfas_rows.append(row)
            for i in range(0, len(lfas_rows), 500):
                await conn.execute(lfas.insert(), lfas_rows[i:i+500])

            # ── LFM1 ──────────────────────────────────────────────────────────
            lfm1_rows = []
            for n in range(2500):
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": random.choice(lifnr_list),
                    "EKORG": random.choice(_EKORG_VALUES),
                    "WAERS": random.choice(_CURRENCIES),
                    "LIEFR": None,
                    "MINBW": None,
                    "KZABS": None,
                    "KZAUT": None,
                    "KZBESN": None,
                    "MEPRF": random.choice(["1", "2", "3", None]),
                    "INCO1": random.choice(_INCO1_VALUES),
                    "INCO2": _null_val() if random.random() < 0.40 else fake.city(),
                    "WEBRE": None,
                    "KZWBK": None,
                    "BOAUF": None,
                    "BOKRE": None,
                    "BOSPE": None,
                    "BOSTA": None,
                    "BOSPE2": None,
                    "UMSAE": None,
                }
                lfm1_rows.append(row)
            for i in range(0, len(lfm1_rows), 500):
                await conn.execute(lfm1.insert(), lfm1_rows[i:i+500])

            # ── LFM2 ──────────────────────────────────────────────────────────
            lfm2_rows = []
            for n in range(3000):
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": random.choice(lifnr_list),
                    "EKORG": random.choice(_EKORG_VALUES),
                    "WERKS": random.choice(_WERKS_VALUES),
                    "SPERM": None,
                    "LOEVM": None,
                    "PLIFZ": str(random.randint(1, 30)),
                    "MNGLG": None,
                    "MNGKO": None,
                    "MNGZE": None,
                    "UEBTO": str(round(random.uniform(0, 10), 1)),
                    "UNTTO": str(round(random.uniform(0, 10), 1)),
                    "UGBTO": None,
                }
                lfm2_rows.append(row)
            for i in range(0, len(lfm2_rows), 500):
                await conn.execute(lfm2.insert(), lfm2_rows[i:i+500])

            # ── LFB5 ──────────────────────────────────────────────────────────
            lfb5_rows = []
            for n in range(1500):
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": random.choice(lifnr_list),
                    "BUKRS": random.choice(_BUKRS_VALUES),
                    "MABER": random.choice(["0001", "0002", "0003"]),
                    "MAHNS": str(random.randint(0, 5)),
                    "MANDT2": None,
                }
                lfb5_rows.append(row)
            for i in range(0, len(lfb5_rows), 500):
                await conn.execute(lfb5.insert(), lfb5_rows[i:i+500])

            # ── LFBW ──────────────────────────────────────────────────────────
            lfbw_rows = []
            for n in range(1000):
                row = {
                    "MANDT": _mandt(),
                    "LIFNR": random.choice(lifnr_list),
                    "BUKRS": random.choice(_BUKRS_VALUES),
                    "WITHT": fake.bothify("??"),
                    "WT_WITHCD": fake.bothify("??"),
                    "WT_EXPT": random.choice(["X", None]),
                    "QSREC": random.choice(["K", "N", "W", None]),
                    "WITHT2": None,
                }
                lfbw_rows.append(row)
            for i in range(0, len(lfbw_rows), 500):
                await conn.execute(lfbw.insert(), lfbw_rows[i:i+500])

            # ── KNA1 ──────────────────────────────────────────────────────────
            kna1_rows = []
            kunnr_list = []
            for n in range(1, 2001):
                kunnr_val = f"{n:010d}"
                kunnr_list.append(kunnr_val)
                loevm_val = "X" if random.random() < 0.03 else None
                row = {
                    "MANDT": _mandt(),
                    "KUNNR": kunnr_val,
                    "LAND1": _land1(),
                    "NAME1": _ts(_name1(fake)),
                    "NAME2": _null_val() if random.random() < 0.40 else fake.company_suffix(),
                    "NAME3": None,
                    "NAME4": None,
                    "ORT01": _ts(fake.city()),
                    "ORT02": None,
                    "PSTLZ": fake.postcode(),
                    "REGIO": fake.bothify("??"),
                    "SORTL": fake.company()[:10].upper(),
                    "STRAS": _ts(fake.street_address()),
                    "TELF1": _ts(fake.phone_number()[:16]),
                    "TELF2": None,
                    "TELFX": None,
                    "TELTX": None,
                    "XCPDK": None,
                    "STCD1": _null_val() if random.random() < 0.20 else fake.numerify("##########"),
                    "STCD2": None,
                    "STKZU": random.choice(["X", None]),
                    "ERDAT": _erdat(fake),
                    "ERNAM": fake.user_name()[:12],
                    "KTOKD": random.choice(["DEBI", "0001", "D001"]),
                    "SPRAS": random.choice(_LANGUAGES),
                    "ANRED": random.choice(["Firma", "Herr", "Frau", None]),
                    "MCOD1": None,
                    "MCOD2": None,
                    "MCOD3": None,
                    "LOEVM": loevm_val,
                    "SPERR": None,
                }
                kna1_rows.append(row)
            for i in range(0, len(kna1_rows), 500):
                await conn.execute(kna1.insert(), kna1_rows[i:i+500])

            # ── KNB1 ──────────────────────────────────────────────────────────
            knb1_rows = []
            for n in range(2500):
                row = {
                    "MANDT": _mandt(),
                    "KUNNR": random.choice(kunnr_list),
                    "BUKRS": random.choice(_BUKRS_VALUES),
                    "AKONT": fake.numerify("######"),
                    "ZTERM": random.choice(_ZTERM_VALUES),
                    "WAERS": random.choice(_CURRENCIES),
                    "ZUAWA": random.choice(["001", "002", "003"]),
                    "BEGRU": random.choice(["0001", "0002", None]),
                    "ALTKN": None,
                    "REPRF": None,
                }
                knb1_rows.append(row)
            for i in range(0, len(knb1_rows), 500):
                await conn.execute(knb1.insert(), knb1_rows[i:i+500])

            # ── KNVV ──────────────────────────────────────────────────────────
            knvv_rows = []
            for n in range(3000):
                row = {
                    "MANDT": _mandt(),
                    "KUNNR": random.choice(kunnr_list),
                    "VKORG": random.choice(_VKORG_VALUES),
                    "VTWEG": random.choice(_VTWEG_VALUES),
                    "SPART": random.choice(_SPART_VALUES),
                    "BZIRK": fake.bothify("???"),
                    "VKBUR": fake.numerify("####"),
                    "KDGRP": fake.bothify("??"),
                    "WAERS": random.choice(_CURRENCIES),
                    "ZTERM": random.choice(_ZTERM_VALUES),
                    "INCO1": random.choice(_INCO1_VALUES),
                    "INCO2": None,
                    "KVGR1": None,
                    "KVGR2": None,
                    "KVGR3": None,
                    "KVGR4": None,
                    "KVGR5": None,
                }
                knvv_rows.append(row)
            for i in range(0, len(knvv_rows), 500):
                await conn.execute(knvv.insert(), knvv_rows[i:i+500])

            # ── KNBK ──────────────────────────────────────────────────────────
            knbk_rows = []
            for n in range(2000):
                row = {
                    "MANDT": _mandt(),
                    "KUNNR": random.choice(kunnr_list),
                    "BANKS": random.choice(_VALID_COUNTRIES),
                    "BANKL": fake.numerify("########"),
                    "BANKN": fake.numerify("##########"),
                    "BKONT": None,
                    "BVTYP": None,
                    "XEZER": None,
                    "BANKA": _ts(fake.company()),
                    "SWIFT": fake.swift(),
                    "IBAN": fake.iban(),
                }
                knbk_rows.append(row)
            for i in range(0, len(knbk_rows), 500):
                await conn.execute(knbk.insert(), knbk_rows[i:i+500])

            # ── MARA ──────────────────────────────────────────────────────────
            mara_rows = []
            matnr_list = []
            for n in range(1, 2001):
                matnr_val = f"MAT{n:07d}"
                matnr_list.append(matnr_val)
                row = {
                    "MANDT": _mandt(),
                    "MATNR": matnr_val,
                    "ERSDA": _erdat(fake),
                    "ERNAM": fake.user_name()[:12],
                    "LAEDA": fake.date_between(start_date="-2y", end_date="today").strftime("%Y%m%d"),
                    "AENAM": fake.user_name()[:12],
                    "MTART": random.choice(_MTART_VALUES),
                    "MBRSH": random.choice(["A", "C", "E", "F", "M", "R"]),
                    "MATKL": fake.numerify("######"),
                    "MEINS": random.choice(_MEINS_VALUES),
                    "BSTME": random.choice(_MEINS_VALUES),
                    "ZEINR": None,
                    "ZEIVR": None,
                    "ZEIFO": None,
                    "AESZN": None,
                    "BLANZ": None,
                    "FERTH": None,
                    "FORMT": None,
                    "NORMT": None,
                    "LABOR": None,
                    "EKWSL": None,
                    "BRGEW": str(round(random.uniform(0.1, 1000), 3)),
                    "GEWEI": random.choice(["KG", "G", "LB"]),
                    "NTGEW": str(round(random.uniform(0.1, 1000), 3)),
                    "VOLUM": str(round(random.uniform(0.001, 100), 3)),
                    "VOLEH": random.choice(["L", "M3", "CM3"]),
                    "BEHVO": None,
                    "RAUBE": None,
                    "TEMPB": None,
                    "DISST": None,
                    "TRAGR": None,
                    "STOFF": None,
                    "SPART": random.choice(_SPART_VALUES),
                    "VHART": None,
                    "FUELG": None,
                    "IPRKZ": None,
                    "RDPRF": None,
                    "MHDRZ": None,
                    "MHDLP": None,
                    "MHDLF": None,
                    "BWVOR": None,
                    "BWSCL": None,
                    "SAISO": None,
                    "ETIAR": None,
                    "ETIFO": None,
                    "ENTAR": None,
                    "EAN11": fake.ean(length=13),
                    "NUMTP": None,
                    "LAENG": str(round(random.uniform(1, 200), 1)),
                    "BREIT": str(round(random.uniform(1, 200), 1)),
                    "HOEHE": str(round(random.uniform(1, 200), 1)),
                    "MEABM": random.choice(["CM", "M", "IN"]),
                    "PRDHA": None,
                    "CADKZ": None,
                    "ERGEW": None,
                    "ERVOLM": None,
                    "WERKS": random.choice(_WERKS_VALUES),
                    "LMEINS": None,
                    "BRGEW2": None,
                    "GEWEI2": None,
                }
                mara_rows.append(row)
            for i in range(0, len(mara_rows), 500):
                await conn.execute(mara.insert(), mara_rows[i:i+500])

            # ── MARC ──────────────────────────────────────────────────────────
            marc_rows = []
            for n in range(5000):
                row = {
                    "MANDT": _mandt(),
                    "MATNR": random.choice(matnr_list),
                    "WERKS": random.choice(_WERKS_VALUES),
                    "PSTAT": fake.bothify("?"),
                    "LVORM": None,
                    "BWTTY": None,
                    "XCHAR": random.choice(["X", None]),
                    "MMSTA": None,
                    "MMSTD": None,
                    "MAABC": random.choice(["A", "B", "C"]),
                    "KZKRI": None,
                    "EKGRP": fake.numerify("###"),
                    "DISMM": random.choice(["PD", "MK", "VB", "ND"]),
                    "DISPO": fake.bothify("???"),
                    "DISLS": random.choice(["EX", "FX", "LF", None]),
                    "BERID": None,
                    "BSTMI": str(random.randint(1, 100)),
                    "MINBE": str(random.randint(0, 50)),
                    "EISBE": str(random.randint(0, 30)),
                    "MABST": None,
                    "STRGR": None,
                    "LGPRO": None,
                    "LGFSB": None,
                    "HERKL": None,
                    "INSMK": random.choice(["X", None]),
                    "SSQSS": None,
                    "MTVFP": None,
                    "KZAUS": None,
                    "AUSDT": None,
                    "NFMAT": None,
                    "MFLHN": None,
                    "KZBED": None,
                    "LGPBE": None,
                    "LGOBE": None,
                    "INSMK2": None,
                }
                marc_rows.append(row)
            for i in range(0, len(marc_rows), 500):
                await conn.execute(marc.insert(), marc_rows[i:i+500])

            # ── MAKT ──────────────────────────────────────────────────────────
            makt_rows = []
            for n in range(3000):
                row = {
                    "MANDT": _mandt(),
                    "MATNR": random.choice(matnr_list),
                    "SPRAS": random.choice(_LANGUAGES),
                    "MAKTX": _ts(fake.catch_phrase()[:40]),
                    "MAKTG": fake.catch_phrase()[:40].upper(),
                }
                makt_rows.append(row)
            for i in range(0, len(makt_rows), 500):
                await conn.execute(makt.insert(), makt_rows[i:i+500])

            # ── SKA1 ──────────────────────────────────────────────────────────
            ska1_rows = []
            saknr_list = []
            account_ranges = [
                ("1", 100000, 199999, "Asset"),
                ("2", 200000, 299999, "Liability"),
                ("3", 300000, 399999, "Equity"),
                ("4", 400000, 499999, "Revenue"),
                ("5", 500000, 599999, "Expense"),
            ]
            for i in range(400):
                range_info = account_ranges[i % len(account_ranges)]
                saknr_val = str(random.randint(range_info[1], range_info[2]))
                saknr_list.append(saknr_val)
                row = {
                    "MANDT": "100",
                    "KTOPL": "INT",
                    "SAKNR": saknr_val,
                    "BILKT": None,
                    "ERDAT": _erdat(fake),
                    "ERNAM": fake.user_name()[:12],
                    "GVTYP": range_info[0],
                    "KTOKS": fake.bothify("????"),
                    "MUSTR": None,
                    "VBUND": None,
                    "XBILK": random.choice(["X", None]),
                    "XLOEV": None,
                    "XSPEA": None,
                    "XSPEB": None,
                    "XUMSA": None,
                }
                ska1_rows.append(row)
            for i in range(0, len(ska1_rows), 500):
                await conn.execute(ska1.insert(), ska1_rows[i:i+500])

            # ── SKAT ──────────────────────────────────────────────────────────
            skat_rows = []
            for n in range(500):
                saknr_val = random.choice(saknr_list)
                row = {
                    "MANDT": "100",
                    "SPRAS": random.choice(_LANGUAGES),
                    "KTOPL": "INT",
                    "SAKNR": saknr_val,
                    "TXT20": fake.bs()[:20],
                    "TXT50": _ts(fake.catch_phrase()[:50]),
                }
                skat_rows.append(row)
            for i in range(0, len(skat_rows), 500):
                await conn.execute(skat.insert(), skat_rows[i:i+500])

            # ── CSKS ──────────────────────────────────────────────────────────
            csks_rows = []
            for n in range(300):
                row = {
                    "MANDT": "100",
                    "KOSTL": fake.numerify("##########"),
                    "DATBI": "99991231",
                    "DATAB": fake.date_between(start_date="-10y", end_date="-1y").strftime("%Y%m%d"),
                    "BKLAS": None,
                    "BUKRS": random.choice(_BUKRS_VALUES),
                    "GSBER": fake.bothify("????"),
                    "KOKRS": "1000",
                    "KOSTLV": None,
                    "KHINR": None,
                    "KOSAR": random.choice(["A", "B", "C", "D"]),
                    "VERAK": fake.user_name()[:12],
                    "VERAK2": None,
                    "KTEXT": _ts(fake.job()[:20]),
                    "LTEXT": fake.bs()[:40],
                    "FUNC_AREA": None,
                }
                csks_rows.append(row)
            for i in range(0, len(csks_rows), 500):
                await conn.execute(csks.insert(), csks_rows[i:i+500])

            # ── EKKO ──────────────────────────────────────────────────────────
            ekko_rows = []
            ebeln_list = []
            for n in range(1, 5001):
                ebeln_val = f"{n:010d}"
                ebeln_list.append(ebeln_val)

                # DQ #4: orphan FK (~1%)
                if random.random() < 0.01:
                    lifnr_fk = "9999999999"
                else:
                    lifnr_fk = random.choice(lifnr_list)

                row = {
                    "MANDT": _mandt(),
                    "EBELN": ebeln_val,
                    "BUKRS": random.choice(_BUKRS_VALUES),
                    "BSART": random.choice(["NB", "ZB", "UB", "FO"]),
                    "LIFNR": lifnr_fk,
                    "EKORG": random.choice(_EKORG_VALUES),
                    "EKGRP": fake.numerify("###"),
                    "WAERS": random.choice(_CURRENCIES),
                    "WKURS": str(round(random.uniform(0.5, 2.0), 5)),
                    "KUFIX": None,
                    "BEDAT": fake.date_between(start_date="-5y", end_date="today").strftime("%Y%m%d"),
                    "KDATB": None,
                    "KDATE": fake.date_between(start_date="-5y", end_date="today").strftime("%Y%m%d"),
                    "KDATV": None,
                    "ABGRU": None,
                    "AUTLF": random.choice(["X", None]),
                    "WEAKT": random.choice(["X", None]),
                    "MEMORY": None,
                    "KZABS": None,
                    "RLWRT": None,
                    "ZTERM": random.choice(_ZTERM_VALUES),
                    "ZBD1T": str(random.randint(0, 30)),
                    "ZBD2T": str(random.randint(0, 60)),
                    "ZBD3T": str(random.randint(0, 90)),
                    "ZBD1P": str(round(random.uniform(0, 3), 1)),
                    "ZBD2P": str(round(random.uniform(0, 2), 1)),
                    "MWSKZ": random.choice(["V1", "V2", "V3", None]),
                    "IHREZ": None,
                    "VERKF": None,
                    "EXNUM": None,
                    "UNSEZ": None,
                    "INCO1": random.choice(_INCO1_VALUES),
                    "INCO2": None,
                    "KONNR": None,
                    "KTPNR": None,
                    "ABTYP": None,
                    "WGLIF": None,
                    "KNUMV": fake.numerify("##########"),
                }
                ekko_rows.append(row)
            for i in range(0, len(ekko_rows), 500):
                await conn.execute(ekko.insert(), ekko_rows[i:i+500])

            # ── EKPO ──────────────────────────────────────────────────────────
            ekpo_rows = []
            for n in range(15000):
                ebeln_val = random.choice(ebeln_list)
                ebelp_val = f"{(n % 999) + 1:05d}"
                row = {
                    "MANDT": _mandt(),
                    "EBELN": ebeln_val,
                    "EBELP": ebelp_val,
                    "MATNR": random.choice(matnr_list),
                    "WERKS": random.choice(_WERKS_VALUES),
                    "LGORT": fake.numerify("####"),
                    "MATKL": fake.numerify("######"),
                    "INFNR": None,
                    "IDNLF": None,
                    "KTMNG": None,
                    "MENGE": str(round(random.uniform(1, 1000), 3)),
                    "MEINS": random.choice(_MEINS_VALUES),
                    "BPRME": random.choice(_MEINS_VALUES),
                    "BPUMZ": None,
                    "BPUMN": None,
                    "NETPR": str(round(random.uniform(1, 10000), 2)),
                    "PEINH": "1",
                    "NETWR": str(round(random.uniform(100, 1000000), 2)),
                    "BRTWR": str(round(random.uniform(100, 1000000), 2)),
                    "BUGSZ": None,
                    "RETPO": None,
                    "WEPOS": random.choice(["X", None]),
                    "WEUNB": None,
                    "REPOS": None,
                    "MWSKZ": random.choice(["V1", "V2", "V3", None]),
                    "ADRNR": None,
                    "PACKNO": None,
                    "FPLNR": None,
                    "BELNR": None,
                    "LOEKZ": None,
                    "BANFN": None,
                    "BNFPO": None,
                    "EBELN2": None,
                    "EBELP2": None,
                }
                ekpo_rows.append(row)
            for i in range(0, len(ekpo_rows), 500):
                await conn.execute(ekpo.insert(), ekpo_rows[i:i+500])

    def get_tables(self) -> list[dict]:
        return [
            {"name": "LFA1", "domain": "Vendor Master", "record_count": 2000, "primary_keys": ["MANDT", "LIFNR"]},
            {"name": "LFB1", "domain": "Vendor Master", "record_count": 3000, "primary_keys": ["MANDT", "LIFNR", "BUKRS"]},
            {"name": "LFBK", "domain": "Vendor Master", "record_count": 2000, "primary_keys": ["MANDT", "LIFNR", "BANKS", "BANKL", "BANKN"]},
            {"name": "LFAS", "domain": "Vendor Master", "record_count": 2500, "primary_keys": ["MANDT", "LIFNR", "EKORG"]},
            {"name": "LFM1", "domain": "Vendor Master", "record_count": 2500, "primary_keys": ["MANDT", "LIFNR", "EKORG"]},
            {"name": "LFM2", "domain": "Vendor Master", "record_count": 3000, "primary_keys": ["MANDT", "LIFNR", "EKORG", "WERKS"]},
            {"name": "LFB5", "domain": "Vendor Master", "record_count": 1500, "primary_keys": ["MANDT", "LIFNR", "BUKRS", "MABER"]},
            {"name": "LFBW", "domain": "Vendor Master", "record_count": 1000, "primary_keys": ["MANDT", "LIFNR", "BUKRS", "WITHT"]},
            {"name": "KNA1", "domain": "Customer Master", "record_count": 2000, "primary_keys": ["MANDT", "KUNNR"]},
            {"name": "KNB1", "domain": "Customer Master", "record_count": 2500, "primary_keys": ["MANDT", "KUNNR", "BUKRS"]},
            {"name": "KNVV", "domain": "Customer Master", "record_count": 3000, "primary_keys": ["MANDT", "KUNNR", "VKORG", "VTWEG", "SPART"]},
            {"name": "KNBK", "domain": "Customer Master", "record_count": 2000, "primary_keys": ["MANDT", "KUNNR", "BANKS", "BANKL"]},
            {"name": "MARA", "domain": "Material Master", "record_count": 2000, "primary_keys": ["MANDT", "MATNR"]},
            {"name": "MARC", "domain": "Material Master", "record_count": 5000, "primary_keys": ["MANDT", "MATNR", "WERKS"]},
            {"name": "MAKT", "domain": "Material Master", "record_count": 3000, "primary_keys": ["MANDT", "MATNR", "SPRAS"]},
            {"name": "SKA1", "domain": "Finance", "record_count": 400, "primary_keys": ["MANDT", "KTOPL", "SAKNR"]},
            {"name": "SKAT", "domain": "Finance", "record_count": 500, "primary_keys": ["MANDT", "SPRAS", "KTOPL", "SAKNR"]},
            {"name": "CSKS", "domain": "Finance", "record_count": 300, "primary_keys": ["MANDT", "KOSTL", "DATBI"]},
            {"name": "EKKO", "domain": "Purchasing", "record_count": 5000, "primary_keys": ["MANDT", "EBELN"]},
            {"name": "EKPO", "domain": "Purchasing", "record_count": 15000, "primary_keys": ["MANDT", "EBELN", "EBELP"]},
        ]

    def get_schema(self, table_name: str) -> dict:
        _descriptions = {
            "MANDT": "Client",
            "LIFNR": "Vendor Account Number",
            "LAND1": "Country Key",
            "NAME1": "Name 1",
            "NAME2": "Name 2",
            "NAME3": "Name 3",
            "NAME4": "Name 4",
            "ORT01": "City",
            "ORT02": "District",
            "PSTLZ": "Postal Code",
            "REGIO": "Region (State/Province)",
            "STRAS": "Street Address",
            "LOEVM": "Central Deletion Flag",
            "SPERR": "Central Posting Block",
            "SPERM": "Purchasing Block",
            "SPRAS": "Language Key",
            "ERDAT": "Date Record Created",
            "ERNAM": "Name of Person Who Created Record",
            "BUKRS": "Company Code",
            "EKORG": "Purchasing Organization",
            "WERKS": "Plant",
            "KUNNR": "Customer Account Number",
            "MATNR": "Material Number",
            "EBELN": "Purchasing Document Number",
            "EBELP": "Item Number of Purchasing Document",
            "KTOKK": "Vendor Account Group",
            "WAERS": "Currency Key",
            "ZTERM": "Terms of Payment Key",
            "INCO1": "Incoterms (Part 1)",
            "INCO2": "Incoterms (Part 2)",
            "AKONT": "Reconciliation Account",
            "BRSCH": "Industry",
            "SORTL": "Sort Field",
            "STCD1": "Tax Number 1",
            "STCEG": "VAT Registration Number",
            "TELF1": "First Telephone Number",
            "KTOPL": "Chart of Accounts",
            "SAKNR": "G/L Account Number",
            "KOSTL": "Cost Center",
            "DATBI": "Valid To Date",
            "DATAB": "Valid From Date",
            "MAKTX": "Material Description",
            "MTART": "Material Type",
            "MEINS": "Base Unit of Measure",
            "MENGE": "Purchase Order Quantity",
            "NETPR": "Net Price",
            "NETWR": "Net Order Value",
        }

        table_obj_map = {
            "LFA1": lfa1, "LFB1": lfb1, "LFBK": lfbk, "LFAS": lfas,
            "LFM1": lfm1, "LFM2": lfm2, "LFB5": lfb5, "LFBW": lfbw,
            "KNA1": kna1, "KNB1": knb1, "KNVV": knvv, "KNBK": knbk,
            "MARA": mara, "MARC": marc, "MAKT": makt,
            "SKA1": ska1, "SKAT": skat, "CSKS": csks,
            "EKKO": ekko, "EKPO": ekpo,
        }
        tbl = table_obj_map.get(table_name)
        if tbl is None:
            return {"table_name": table_name, "columns": []}

        columns = []
        for col in tbl.columns:
            columns.append({
                "name": col.name,
                "type": "String(255)",
                "nullable": True,
                "description": _descriptions.get(col.name, col.name),
                "sample_values": [],
            })
        return {"table_name": table_name, "columns": columns}

    def get_relationships(self, table_name: str) -> list[dict]:
        _rels = {
            "LFB1": [{"from_table": "LFB1", "from_column": "LIFNR", "to_table": "LFA1", "to_column": "LIFNR"}],
            "LFBK": [{"from_table": "LFBK", "from_column": "LIFNR", "to_table": "LFA1", "to_column": "LIFNR"}],
            "LFAS": [{"from_table": "LFAS", "from_column": "LIFNR", "to_table": "LFA1", "to_column": "LIFNR"}],
            "LFM1": [{"from_table": "LFM1", "from_column": "LIFNR", "to_table": "LFA1", "to_column": "LIFNR"}],
            "LFM2": [{"from_table": "LFM2", "from_column": "LIFNR", "to_table": "LFM1", "to_column": "LIFNR"}],
            "LFB5": [{"from_table": "LFB5", "from_column": "LIFNR", "to_table": "LFB1", "to_column": "LIFNR"}],
            "LFBW": [{"from_table": "LFBW", "from_column": "LIFNR", "to_table": "LFB1", "to_column": "LIFNR"}],
            "KNB1": [{"from_table": "KNB1", "from_column": "KUNNR", "to_table": "KNA1", "to_column": "KUNNR"}],
            "KNVV": [{"from_table": "KNVV", "from_column": "KUNNR", "to_table": "KNA1", "to_column": "KUNNR"}],
            "KNBK": [{"from_table": "KNBK", "from_column": "KUNNR", "to_table": "KNA1", "to_column": "KUNNR"}],
            "MARC": [{"from_table": "MARC", "from_column": "MATNR", "to_table": "MARA", "to_column": "MATNR"}],
            "MAKT": [{"from_table": "MAKT", "from_column": "MATNR", "to_table": "MARA", "to_column": "MATNR"}],
            "EKKO": [{"from_table": "EKKO", "from_column": "LIFNR", "to_table": "LFA1", "to_column": "LIFNR"}],
            "EKPO": [
                {"from_table": "EKPO", "from_column": "EBELN", "to_table": "EKKO", "to_column": "EBELN"},
                {"from_table": "EKPO", "from_column": "MATNR", "to_table": "MARA", "to_column": "MATNR"},
            ],
        }
        return _rels.get(table_name, [])
