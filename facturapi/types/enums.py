from enum import Enum


class FileType(str, Enum):
    """Enum to define a file type."""

    pdf = 'pdf'
    xml = 'xml'
    zip = 'zip'


class InvoiceRelation(str, Enum):
    """Relation key in SAT catalogue for related invoices."""

    nota_de_credito = '01'
    nota_de_debito = '02'
    devolucion_de_mercancia = '03'
    sustitucion_de_cfdi_previos = '04'
    traslados_de_mercancia_facturados_previamente = '05'
    factura_por_traslados_previos = '06'
    aplicacion_de_anticipo = '07'
    pagos_en_parcialidades = '08'
    pagos_diferidos = '09'


class InvoiceType(str, Enum):
    """Type of an invoice."""

    ingreso = 'I'
    egreso = 'E'
    traslado = 'T'
    nomina = 'N'
    pago = 'P'


class InvoiceUse(str, Enum):
    """CFDI use code from SAT catalogue."""

    adquisicion_mercancias = 'G01'
    devoluciones_descuentos_bonificaciones = 'G02'
    gastos_en_general = 'G03'
    construcciones = 'I01'
    mobiliario_y_equipo_de_oficina = 'I02'
    equipo_de_transporte = 'I03'
    equipo_de_computo = 'I04'
    dados_troqueles_herramental = 'I05'
    comunicaciones_telefonicas = 'I06'
    comunicaciones_satelitales = 'I07'
    otra_maquinaria = 'I08'
    honorarios_medicos = 'D01'
    gastos_medicos_por_incapacidad = 'D02'
    gastos_funerales = 'D03'
    donativos = 'D04'
    intereses_por_creditos_hipotecarios = 'D05'
    aportaciones_voluntarias_sar = 'D06'
    prima_seguros_gastos_medicos = 'D07'
    gastos_transportacion_escolar = 'D08'
    cuentas_ahorro_pensiones = 'D09'
    servicios_educativos = 'D10'
    sin_efectos_fiscales = 'S01'
    pagos = 'CP01'
    nomina = 'CN01'


class PaymentForm(str, Enum):
    """Payment from code according to SAT."""

    efectivo = '01'
    cheque_nominativo = '02'
    transferencia_electronica_de_fondos = '03'
    tarjeta_de_credito = '04'
    monedero_electronico = '05'
    dinero_electronico = '06'
    vales_de_despensa = '06'
    dacion_en_pago = '12'
    pago_por_subrogacion = '13'
    pago_por_consignacion = '14'
    condonacion = '15'
    compensacion = '17'
    novacion = '23'
    confusion = '24'
    remision_de_deuda = '25'
    prescripcion_o_caducidad = '26'
    a_satisfaccion_del_acreedor = '27'
    tarjeta_de_debito = '28'
    tarjeta_de_servicios = '29'
    aplicacion_de_anticipos = '30'
    intermediario_pagos = '31'
    por_definir = '99'


class PaymentMethod(str, Enum):
    """Payment method code according to SAT."""

    contado = 'PUE'
    parcialidades = 'PPD'


class TaxSystemType(str, Enum):
    GRL_PM = "601"  # General de Ley Personas Morales
    PM_FN = "603"  # Personas Morales con Fines no Lucrativos
    SAL_IS = "605"  # Sueldos y Salarios e Ingresos Asimilados a Salarios
    ARR = "606"  # Arrendamiento
    DEM_ING = "608"  # Demás ingresos
    CONS = "609"  # Consolidación
    RES_EXT = "610"  # Residentes en el Extranjero sin Establecimiento Permanente en México # noqa: E501
    DIV = "611"  # Ingresos por Dividendos (socios y accionistas)
    PF_AEP = "612"  # Personas Físicas con Actividades Empresariales y Profesionales # noqa: E501
    INT = "614"  # Ingresos por intereses
    SIN_OBL = "616"  # Sin obligaciones fiscales
    SCP_DIF = "620"  # Sociedades Cooperativas de Producción que optan por diferir sus ingresos # noqa: E501
    INC_FISC = "621"  # Incorporación Fiscal
    AGRO_GAN_SILV_PES = "622"  # Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras # noqa: E501
    OP_GRUPO_SOC = "623"  # Opcional para Grupos de Sociedades
    COOR = "624"  # Coordinados
    HID = "628"  # Hidrocarburos
    ENAJ_ADQ = "607"  # Régimen de Enajenación o Adquisición de Bienes
    PREF_EM_MULT = "629"  # De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales # noqa: E501
    ENAJ_ACC_BOL = "630"  # Enajenación de acciones en bolsa de valores
    ING_PREM = "615"  # Régimen de los ingresos por obtención de premios
    AE_PLAT_TEC = "625"  # Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas # noqa: E501
    RS_CONF = "626"  # Régimen Simplificado de Confianza
