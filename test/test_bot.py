#!/usr/bin/env python3
"""
Script de teste para o bot CEPzinho
"""

from cep import Cep


def test_cep_api():
    """Testa a API de CEP"""
    print("🧪 Testando API de CEP...")

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
        return True

    except Exception as e:
        print(f"❌ Erro ao testar CEP {test_cep}: {e}")
        return False


def test_cep_extraction():
    """Testa a extração de CEP de diferentes formatos"""
    print("\n🧪 Testando extração de CEP...")

    test_cases = [
        "01310-100",
        "01310100",
        "01310 100",
        "abc01310-100def",
        "01310",
        "013101001",
    ]

    for test_case in test_cases:
        # Simula a extração do CEP
        import re

        cep_clean = re.sub(r"[^\d]", "", test_case)

        if len(cep_clean) == 8:
            print(f"✅ '{test_case}' -> {cep_clean}")
        else:
            print(f"❌ '{test_case}' -> inválido ({len(cep_clean)} dígitos)")


def test_environment():
    """Testa se as variáveis de ambiente estão configuradas"""
    print("\n🧪 Testando configuração do ambiente...")

    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    token = getenv("TELEGRAM_TOKEN")

    if token and token != "seu_token_aqui":
        print("✅ Token do Telegram configurado")
        return True
    else:
        print("❌ Token do Telegram não configurado")
        print("   Crie um arquivo .env com: TELEGRAM_TOKEN=seu_token_aqui")
        return False


def main():
    """Executa todos os testes"""
    print("🤖 Iniciando testes do CEPzinho...\n")

    # Testa a API de CEP
    cep_test = test_cep_api()

    # Testa extração de CEP
    test_cep_extraction()

    # Testa configuração do ambiente
    env_test = test_environment()

    print("\n" + "=" * 50)
    if cep_test and env_test:
        print("🎉 Todos os testes passaram! O bot está pronto para uso.")
        print("\nPara iniciar o bot, execute:")
        print("   poetry run python main.py")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")

    print("=" * 50)


if __name__ == "__main__":
    main()
