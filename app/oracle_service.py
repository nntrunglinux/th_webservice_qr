from dataclasses import dataclass
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from lxml import etree

@dataclass()
class OracleService:
    host: str
    plugins: list
    username: str
    password: str

    def __post_init__(self):
        session = Session()
        session.auth = HTTPBasicAuth(self.username, self.password)
        transport = Transport(session=session)
        self.report_client = Client(
            self.host + "xmlpserver/services/ExternalReportWSSService?wsdl",
            plugins=self.plugins,
            transport=transport,
        )

    def get_report_xml(self, report_path, report_params):
        report_request = {
            "reportRequest": {
                "byPassCache": True,
                "flattenXML": True,
                "attributeFormat": "xml",
                "reportAbsolutePath": report_path,
                "parameterNameValues": {"item": report_params},
                "sizeOfDataChunkDownload": -1,
            },
            "appParams": "",
        }
        res = self.report_client.service.runReport(**report_request)
        report_xml = etree.fromstring(res.reportBytes)
        return report_xml

    def get_report_params(self, report_path):
        report_request = {
            "reportRequest": {
                "byPassCache": True,
                "flattenXML": False,
                "attributeFormat": "xml",
                "reportAbsolutePath": report_path,
                "sizeOfDataChunkDownload": -1,
            },
        }
        res = self.report_client.service.getReportParameters(**report_request)
        return res