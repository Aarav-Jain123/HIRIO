from zeep import Client

def verify_vat(country_code, vat_number):
    wsdl_url = 'https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    client = Client(wsdl=wsdl_url)

    try:
        result = client.service.checkVat(countryCode=country_code, vatNumber=vat_number)
        return {
            "valid": result.valid,
            "name": result.name,
            "address": result.address
        }
    except Exception as e:
        return {"error": str(e)}