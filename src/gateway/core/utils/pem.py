from cryptography import x509
import typing


def get_domains_from_certificate(pem_data: str) -> typing.Tuple[str, typing.List[str]]:
    cert = x509.load_pem_x509_certificate(pem_data.encode())
    # We need to find the extension subjectAltName
    subjectAltName = x509.ObjectIdentifier('2.5.29.17')       # ObjectIdentifier(oid=2.5.29.17, name=subjectAltName)
    extension = cert.extensions.get_extension_for_oid(subjectAltName)
    dns_names = extension.value.get_values_for_type(x509.DNSName)

    parent_domain = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value      # Subject <Name(CN=core.zuberipay.com)>
    return parent_domain, dns_names

    

"""
data = '-----BEGIN CERTIFICATE-----\nMIIH...3yz\n-----END CERTIFICATE-----\n'

get_domains_from_certificate(data)
"""