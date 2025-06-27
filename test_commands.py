#!/usr/bin/env python3
"""
Script de teste para os comandos do bot CEPzinho
"""

from cep import Cep
from messages import format_cep_response, format_address_response


def test_cep_command():
    """Testa o comando /cep"""
    print("🧪 Testando comando /cep...")

    # Teste com um CEP válido
    test_cep = "01310-100"
    try:
        cep_obj = Cep(test_cep)
        result = cep_obj.get_cep()

        if result.get("erro"):
            print(f"❌ CEP {test_cep} não encontrado")
            return False

        print(f"✅ CEP {test_cep} encontrado:")
        print(f"   Logradouro: {result.get('logradouro')}")
        print(f"   Bairro: {result.get('bairro')}")
        print(f"   Cidade: {result.get('localidade')}")
        print(f"   Estado: {result.get('uf')}")

        # Testa formatação da resposta
        formatted = format_cep_response(result)
        print(f"📝 Resposta formatada: {len(formatted)} caracteres")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar CEP {test_cep}: {e}")
        return False


def test_rua_command():
    """Testa o comando /rua"""
    print("\n🧪 Testando comando /rua...")

    # Teste com um endereço válido
    uf = "SP"
    cidade = "São Paulo"
    logradouro = "Avenida Paulista"

    try:
        cep_obj = Cep()
        result = cep_obj.search_address(uf, cidade, logradouro)

        if not result:
            print(f"❌ Endereço não encontrado: {logradouro}, {cidade}/{uf}")
            return False

        print(f"✅ Endereço encontrado: {len(result)} resultados")

        # Mostra os primeiros 3 resultados
        for i, addr in enumerate(result[:3], 1):
            print(f"   {i}. {addr.get('logradouro')} - CEP: {addr.get('cep')}")

        # Testa formatação da resposta
        formatted = format_address_response(result)
        print(f"📝 Resposta formatada: {len(formatted)} caracteres")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar endereço: {e}")
        return False


def test_address_parsing():
    """Testa o parsing de endereços"""
    print("\n🧪 Testando parsing de endereços...")

    test_cases = [
        "Avenida Paulista, São Paulo, SP",
        "Rua das Flores, 123, Centro, São Paulo, SP",
        "Praça da Sé, São Paulo, SP",
        "Rua Augusta, São Paulo",  # Sem UF
        "Avenida Paulista",  # Muito curto
    ]

    for test_case in test_cases:
        # Simula o parsing do endereço
        parts = test_case.split(",")

        if len(parts) < 2:
            print(f"❌ '{test_case}' -> inválido (poucas partes)")
            continue

        uf = parts[-1].strip().upper()
        cidade = parts[-2].strip()
        logradouro = ",".join(parts[:-2]).strip()

        if not uf or not cidade or not logradouro:
            print(f"❌ '{test_case}' -> inválido (partes vazias)")
        else:
            print(
                f"✅ '{test_case}' -> UF: {uf}, Cidade: {cidade}, Logradouro: {logradouro}"
            )


def main():
    """Executa todos os testes"""
    print("🤖 Iniciando testes dos comandos do CEPzinho...\n")

    # Testa comando /cep
    cep_test = test_cep_command()

    # Testa comando /rua
    rua_test = test_rua_command()

    # Testa parsing de endereços
    test_address_parsing()

    print("\n" + "=" * 50)
    if cep_test and rua_test:
        print("🎉 Todos os testes passaram! Os comandos estão funcionando.")
        print("\nComandos disponíveis:")
        print("   /cep [número] - Busca endereço por CEP")
        print("   /rua [endereço] - Busca CEP por endereço")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")

    print("=" * 50)


if __name__ == "__main__":
    main()
