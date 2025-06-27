from requests import get
from logperformance import LogPerformance
from config import CEP_API_URL


class Cep:
    def __init__(self, cep: str = None):
        self.cep = cep

    def get_cep(self) -> dict:
        """Busca informações de um CEP específico"""
        LogPerformance().warning(f"Buscando CEP {self.cep}")
        response = get(CEP_API_URL.format(cep=self.cep))
        LogPerformance().warning(f"CEP {self.cep} encontrado: {response.json()}")
        return response.json()

    def search_address(self, uf: str, cidade: str, logradouro: str) -> list:
        """Busca CEPs por endereço"""
        LogPerformance().warning(f"Buscando endereço: {logradouro}, {cidade}/{uf}")

        search_url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"

        response = get(search_url)
        result = response.json()

        LogPerformance().warning(f"Endereço encontrado: {len(result)} resultados")
        return result if isinstance(result, list) else []
