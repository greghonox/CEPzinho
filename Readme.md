🤖 CEPzinho
O Seu Ajudante de Endereços no Telegram! 📍
Com o CEPzinho, você encontra CEPs e endereços completos de forma rápida e descomplicada. Perfeito para entregas, cadastros e para nunca mais se perder!

---

🌟 Funcionalidades

📍 **Busca por CEP**: Use `/cep [número]` e receba o endereço completo (rua, bairro, cidade, estado, DDD, IBGE).

🏠 **Busca por Endereço**: Use `/rua [endereço]` e descubra o CEP correspondente.

🔍 **Modo Inline**: Use o bot em qualquer chat sem adicioná-lo ao grupo!

🤖 **Interface Simples**: Interaja com o bot de forma intuitiva e eficiente diretamente no Telegram.

⚡ **Gratuito e Rápido**: Obtenha suas informações de endereço sem custo e em poucos segundos.

---

🚀 Como Usar

**1. Encontre o bot no Telegram:**

- Procure por @CEPzinho na barra de busca do Telegram
- Clique em "Iniciar" ou "Start"

**2. Comandos disponíveis:**

- `/start`: Inicia o bot e exibe a mensagem de boas-vindas
- `/help`: Exibe informações de ajuda e como usar o bot
- `/cep [número]`: Busca endereço por CEP
- `/rua [endereço]`: Busca CEP por endereço

**3. Modo Inline (Funcionalidade Avançada):**

- Digite `@seu_bot_username` + CEP ou endereço em qualquer chat
- O bot responderá diretamente no chat sem precisar ser adicionado
- Funciona em grupos, canais e conversas privadas

**4. Exemplos de uso:**

📍 **Buscar por CEP:**

```
/cep 01310-100
/cep 01310100
/cep 01310 100

# Modo Inline:
@seu_bot_username 01310-100
```

🏠 **Buscar por Endereço:**

```
/rua Avenida Paulista, São Paulo, SP
/rua Rua das Flores, 123, Centro, São Paulo, SP
/rua Praça da Sé, São Paulo, SP

# Modo Inline:
@seu_bot_username Avenida Paulista, São Paulo, SP
```

---

⚙️ Instalação (Para Desenvolvedores)

**Pré-requisitos:**

- Python 3.12+
- Poetry (recomendado para gerenciamento de dependências)
- Token de API do seu bot no Telegram

**Passos para Instalar:**

1. **Clone o repositório:**

```bash
git clone https://github.com/[SeuUsuario]/CEPzinho.git
cd CEPzinho
```

2. **Instale as dependências com Poetry:**

```bash
poetry install
```

3. **Configure o bot do Telegram:**

   - Acesse [@BotFather](https://t.me/BotFather) no Telegram
   - Crie um novo bot com `/newbot`
   - Copie o token fornecido
   - **Importante**: Ative o modo inline com `/setinline`

4. **Crie o arquivo de configuração:**
   - Crie um arquivo chamado `.env` na raiz do projeto
   - Adicione o seguinte conteúdo:

```env
TELEGRAM_TOKEN=SEU_TOKEN_DO_BOT_AQUI
```

5. **Execute o bot:**

```bash
poetry run python main.py
```

---

🔧 Configuração do Bot

**Para criar um bot no Telegram:**

1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Escolha um nome para seu bot (ex: "CEPzinho")
4. Escolha um username único (ex: "meu_cepzinho_bot")
5. BotFather fornecerá um token - copie-o
6. Cole o token no arquivo `.env`

**Para ativar o modo inline:**

1. Envie `/setinline` para @BotFather
2. Selecione seu bot
3. Digite o texto que aparecerá quando o usuário digitar @seu_bot_username
4. Exemplo: "Digite um CEP ou endereço para buscar informações"

---

📋 Informações Retornadas

**Para consulta por CEP (`/cep` ou modo inline):**

- **CEP**: O CEP formatado
- **Logradouro**: Nome da rua/avenida
- **Bairro**: Nome do bairro
- **Cidade**: Nome da cidade
- **Estado**: Sigla do estado (UF)
- **DDD**: Código de discagem direta
- **IBGE**: Código do município no IBGE
- **SIAFI**: Código SIAFI do município

**Para consulta por endereço (`/rua` ou modo inline):**

- Lista de endereços encontrados (máximo 5 em comandos, 3 em inline)
- CEP de cada endereço
- Bairro e cidade de cada endereço

---

🔍 Modo Inline - Vantagens

- **Não precisa adicionar o bot ao grupo**: Use em qualquer chat
- **Resposta rápida**: Resultados aparecem instantaneamente
- **Privacidade**: O bot não fica no histórico do grupo
- **Flexibilidade**: Funciona em grupos, canais e conversas privadas
- **Fácil de usar**: Apenas digite @seu_bot_username + consulta

---

🤝 Contribuições

Contribuições são muito bem-vindas! Se você tiver ideias para melhorias, encontrou um bug ou deseja adicionar novas funcionalidades:

1. Faça um fork do projeto
2. Crie uma nova branch para sua feature (`git checkout -b feature/minha-nova-funcionalidade`)
3. Faça suas alterações e commit (`git commit -m 'feat: adiciona nova funcionalidade X'`)
4. Envie suas alterações para o upstream (`git push origin feature/minha-nova-funcionalidade`)
5. Abra um Pull Request

---

📜 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

✉️ Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato:

- **Telegram**: @greghono
- **Email**: greghono@gmail.com

---

🔗 APIs Utilizadas

- **ViaCEP**: API gratuita para consulta de CEPs brasileiros
- **python-telegram-bot**: Biblioteca para criação de bots no Telegram
