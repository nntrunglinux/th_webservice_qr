from loguru import logger
from .settings import Setting
from .oracle_service import OracleService
from .purchase_order_constants import REPORT_PARAMS, TAG_PAIR
from . import utils

settings = Setting()
oracle_service = OracleService(
    host=settings.ORACLE_HOST,
    plugins=[],
    username=settings.ORACLE_BI_USERNAME,
    password=settings.ORACLE_BI_PASSWORD,
)

def update_po_value(po):
    total_amount_float = utils.safe_cast(po.get('total_amount'), float, 0.0)
    tax_rate = utils.safe_cast(po.get('tax_rate'), float, 0.0) / 100
    total_amount_vat = total_amount_float + (total_amount_float * tax_rate)
    total_amount_currency = utils.float_to_currency_str(total_amount_vat)
    created_date = po.get('created_date')
    approved_date = po.get('approved_date')

    po.update({
        'total_amount': total_amount_currency,
        'created_date': utils.date_safe_cast(created_date),
        'approved_date': utils.date_safe_cast(approved_date),
    })

def purchase_order(po_number=None):
    try:
        if not po_number:
            logger.error(f"Không nhận được po_number")
            return

        report_params = REPORT_PARAMS
        utils.update_report_params(report_params, po_number)
        po_xml = oracle_service.get_report_xml(
            settings.ORACLE_BI_REPORT_PATH,
            report_params
        )

        if len(po_xml) <= 0:
            logger.error(f"po_number = {po_number} không có dữ liệu.")
            return
        if po_xml[0].find(f'.//PO_NUMBER') is None:
            logger.error(f"po_number = {po_number} không có dữ liệu.")
            return

        po = {}
        first_po = po_xml[0]
        for key, tag in TAG_PAIR.items():
            node = first_po.find(f".//{tag}")
            if node is None:
                value = ""
            else:
                value = node.text
            po.update({
                key: value
            })

        update_po_value(po)
        return po
    except Exception as e:
        logger.error(f"Lỗi trong quá trình lấy po_number = {po_number}. Lỗi: {e}")


