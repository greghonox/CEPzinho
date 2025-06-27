#!/usr/bin/env python3
"""
Script de teste para funcionalidade inline do bot CEPzinho
"""

from cep import Cep
from messages import (
    format_inline_cep_result,
    format_inline_address_result,
    INLINE_RESULT_TITLE_CEP,
    INLINE_RESULT_DESCRIPTION_CEP,
    INLINE_RESULT_TITLE_ADDRESS,
    INLINE_RESULT_DESCRIPTION_ADDRESS,
)


def test_inline_cep_formatting():
    """Testa a formatação de resultados inline para CEP"""
    print("🧪 Testando formatação inline para CEP...")

    # Teste com um CEP válido
    test_cep = "01310-100"
    try:
        cep_obj = Cep(test_cep)
        result = cep_obj.get_cep()

        if result.get("erro"):
            print(f"❌ CEP {test_cep} não encontrado")
            return False

        # Testa formatação inline
        inline_content = format_inline_cep_result(result)
        print(f"✅ Conteúdo inline formatado:")
        print(f"   {inline_content}")

        # Testa título e descrição
        title = INLINE_RESULT_TITLE_CEP.format(cep=result.get("cep"))
        description = INLINE_RESULT_DESCRIPTION_CEP.format(
            logradouro=result.get("logradouro", "N/A"),
            bairro=result.get("bairro", "N/A"),
            cidade=result.get("localidade", "N/A"),
            uf=result.get("uf", "N/A"),
        )

        print(f"   Título: {title}")
        print(f"   Descrição: {description}")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar formatação inline CEP: {e}")
        return False


def test_inline_address_formatting():
    """Testa a formatação de resultados inline para endereço"""
    print("\n🧪 Testando formatação inline para endereço...")

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

        # Testa formatação inline
        inline_content = format_inline_address_result(result)
        print(f"✅ Conteúdo inline formatado:")
        print(f"   {inline_content}")

        # Testa título e descrição para o primeiro resultado
        if result:
            first_addr = result[0]
            title = INLINE_RESULT_TITLE_ADDRESS.format(
                logradouro=first_addr.get("logradouro", "N/A")
            )
            description = INLINE_RESULT_DESCRIPTION_ADDRESS.format(
                cep=first_addr.get("cep", "N/A"),
                cidade=first_addr.get("localidade", "N/A"),
                uf=first_addr.get("uf", "N/A"),
            )

            print(f"   Título: {title}")
            print(f"   Descrição: {description}")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar formatação inline endereço: {e}")
        return False


def test_inline_query_parsing():
    """Testa o parsing de consultas inline"""
    print("\n🧪 Testando parsing de consultas inline...")

    test_cases = [
        ("01310-100", "CEP válido"),
        ("01310100", "CEP sem hífen"),
        ("Avenida Paulista, São Paulo, SP", "Endereço completo"),
        ("Rua das Flores, 123, Centro, São Paulo, SP", "Endereço com número"),
        ("", "Query vazia"),
        ("abc123", "Texto inválido"),
    ]

    for query, description in test_cases:
        print(f"   Testando: '{query}' ({description})")

        # Simula o parsing da query
        if not query.strip():
            print(f"     → Query vazia (placeholder)")
            continue

        # Verifica se é CEP
        import re

        cep_clean = re.sub(r"[^\d]", "", query)
        if len(cep_clean) == 8:
            print(f"     → CEP detectado: {cep_clean}")
        else:
            # Verifica se é endereço
            parts = query.split(",")
            if len(parts) >= 2:
                uf = parts[-1].strip().upper()
                cidade = parts[-2].strip()
                logradouro = ",".join(parts[:-2]).strip()

                if uf and cidade and logradouro:
                    print(f"     → Endereço detectado: {logradouro}, {cidade}/{uf}")
                else:
                    print(f"     → Endereço inválido")
            else:
                print(f"     → Formato inválido")


def main():
    """Executa todos os testes de funcionalidade inline"""
    print("🤖 Iniciando testes da funcionalidade inline do CEPzinho...\n")

    # Testa formatação inline para CEP
    cep_test = test_inline_cep_formatting()

    # Testa formatação inline para endereço
    address_test = test_inline_address_formatting()

    # Testa parsing de consultas inline
    test_inline_query_parsing()

    print("\n" + "=" * 50)
    if cep_test and address_test:
        print("🎉 Todos os testes inline passaram!")
        print("\nFuncionalidade inline disponível:")
        print("   • Digite @seu_bot_username + CEP em qualquer chat")
        print("   • Digite @seu_bot_username + endereço em qualquer chat")
        print("   • Respostas formatadas e organizadas")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")

    print("=" * 50)


if __name__ == "__main__":
    main()
