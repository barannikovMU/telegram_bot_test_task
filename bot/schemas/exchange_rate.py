from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, validator


class SchemaBodyValute(BaseModel):
    id: str = Field(alias='ID')
    num_code: str = Field(alias='NumCode')
    char_code: str = Field(alias='CharCode')
    nominal: int = Field(alias='Nominal')
    name: str = Field(alias='Name')
    value: float = Field(alias='Value')
    previous: float = Field(alias='Previous')


class SchemaValute(BaseModel):
    aud: SchemaBodyValute = Field(alias='AUD')
    azn: SchemaBodyValute = Field(alias='AZN')
    gbp: SchemaBodyValute = Field(alias='GBP')
    amd: SchemaBodyValute = Field(alias='AMD')
    byn: SchemaBodyValute = Field(alias='BYN')
    bgn: SchemaBodyValute = Field(alias='BGN')
    brl: SchemaBodyValute = Field(alias='BRL')
    huf: SchemaBodyValute = Field(alias='HUF')
    vnd: SchemaBodyValute = Field(alias='VND')
    hkd: SchemaBodyValute = Field(alias='HKD')
    gel: SchemaBodyValute = Field(alias='GEL')
    dkk: SchemaBodyValute = Field(alias='DKK')
    aed: SchemaBodyValute = Field(alias='AED')
    usd: SchemaBodyValute = Field(alias='USD')
    eur: SchemaBodyValute = Field(alias='EUR')
    egp: SchemaBodyValute = Field(alias='EGP')
    inr: SchemaBodyValute = Field(alias='INR')
    idr: SchemaBodyValute = Field(alias='IDR')
    kzt: SchemaBodyValute = Field(alias='KZT')
    cad: SchemaBodyValute = Field(alias='CAD')
    qar: SchemaBodyValute = Field(alias='QAR')
    kgs: SchemaBodyValute = Field(alias='KGS')
    cny: SchemaBodyValute = Field(alias='CNY')
    mdl: SchemaBodyValute = Field(alias='MDL')
    nzd: SchemaBodyValute = Field(alias='NZD')
    nok: SchemaBodyValute = Field(alias='NOK')
    pln: SchemaBodyValute = Field(alias='PLN')
    ron: SchemaBodyValute = Field(alias='RON')
    xdr: SchemaBodyValute = Field(alias='XDR')
    sgd: SchemaBodyValute = Field(alias='SGD')
    tjs: SchemaBodyValute = Field(alias='TJS')
    thb: SchemaBodyValute = Field(alias='THB')
    tmt: SchemaBodyValute = Field(alias='TMT')
    uzs: SchemaBodyValute = Field(alias='UZS')
    uah: SchemaBodyValute = Field(alias='UAH')
    czk: SchemaBodyValute = Field(alias='CZK')
    sek: SchemaBodyValute = Field(alias='SEK')
    chf: SchemaBodyValute = Field(alias='CHF')
    rsd: SchemaBodyValute = Field(alias='RSD')
    zar: SchemaBodyValute = Field(alias='ZAR')
    krw: SchemaBodyValute = Field(alias='KRW')
    jpy: SchemaBodyValute = Field(alias='JPY')


class SchemaBodyCurrentExchangeRate(BaseModel):
    date: datetime = Field(alias='Date')
    previous_date: datetime = Field(alias='PreviousDate')
    previous_url: str = Field(alias='PreviousURL')
    timestamp: datetime = Field(alias='Timestamp')
    valute: SchemaValute = Field(alias='Valute')


class CurrencyValue(BaseModel):
    value: Decimal = Field()

    @validator('value')
    def quantize(cls, value):
        if value <= 0:
            raise ValueError('The value must be > 0')
        return Decimal(value).quantize(Decimal('1.0000'))
