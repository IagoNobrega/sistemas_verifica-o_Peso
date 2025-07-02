## 🚀 Visão Geral do Projeto

O **Sistema de Verificação de Peso para Peças Industriais** é uma solução robusta e intuitiva desenvolvida para otimizar o controle de qualidade na expedição de produtos. Ele permite a verificação automatizada da quantidade de peças em caixas com base no peso, garantindo precisão e rastreabilidade em ambientes industriais.

Este sistema é ideal para empresas que lidam com uma variedade de peças (mais de 32 tipos diferentes) e buscam reduzir erros de expedição, otimizar processos e melhorar a satisfação do cliente.

## ✨ Funcionalidades

*   **Verificação de Peso Inteligente:** Calcula a quantidade de peças em uma caixa com base no peso total e no peso unitário de cada tipo de peça, considerando tolerâncias configuráveis.
*   **Suporte a Múltiplos Tipos de Peças:** Gerencia e diferencia mais de 32 tipos de modelos de peças, cada um com suas especificações de peso e quantidade padrão.
*   **Geração de Etiquetas em PDF:** Emite etiquetas de verificação profissionais em formato PDF, contendo informações detalhadas da verificação e um QR Code para rastreabilidade.
*   **Histórico de Verificações:** Mantém um registro completo de todas as verificações realizadas, permitindo auditorias e análises de desempenho.
*   **Interface Web Intuitiva:** Uma interface de usuário (UI) limpa e responsiva, desenvolvida em HTML, CSS e JavaScript, que facilita a operação por qualquer usuário.
*   **Simulação de Balança:** Inclui uma funcionalidade de simulação de leitura de balança para testes e demonstrações, com arquitetura pronta para integração com balanças reais (via porta serial, por exemplo).
*   **API RESTful:** Backend robusto em Flask que expõe endpoints para todas as funcionalidades, facilitando futuras integrações com outros sistemas.

## 🛠 Tecnologias Utilizadas

*   **Backend:**
    *   Python 3.11+
    *   Flask (Framework Web)
    *   SQLAlchemy (ORM para banco de dados)
    *   SQLite (Banco de dados leve e embarcado)
    *   ReportLab (Geração de PDF)
    *   QRCode (Geração de QR Codes)
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (Vanilla)
*   **Outros:**
    *   `pip` (Gerenciador de pacotes Python)
    *   `venv` (Ambientes virtuais Python)

## 📦 Estrutura do Projeto

```
sistema_verificacao_peso/
├── src/
│   ├── database/
│   │   └── app.db           # Banco de dados SQLite
│   ├── models/
│   │   ├── __init__.py
│   │   ├── peca.py          # Modelos de dados para Peça e Verificação
│   │   └── user.py          # Modelo de dados de usuário (exemplo)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── etiqueta.py      # Rotas para geração de etiquetas
│   │   ├── init.py          # Rota para inicialização de dados de exemplo
│   │   ├── peca.py          # Rotas para gerenciamento de peças e verificações
│   │   └── user.py          # Rotas de usuário (exemplo)
│   ├── static/
│   │   └── index.html       # Frontend (HTML, CSS, JS)
│   └── main.py              # Aplicação Flask principal
├── venv/                    # Ambiente virtual Python (não incluído no ZIP)
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo
```

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar e executar o sistema em seu ambiente local.

### Pré-requisitos

*   Python 3.11 ou superior instalado.
*   `pip` (gerenciador de pacotes Python).
*   Um navegador web moderno (Chrome, Firefox, Edge, Safari).

### Passos de Instalação

1.  **Clone o Repositório (ou descompacte o ZIP):**

    Se você recebeu o projeto como um arquivo ZIP (`sistema_verificacao_peso.zip`), descompacte-o em uma pasta de sua preferência.

    ```bash
    # Exemplo para Linux/macOS
    unzip sistema_verificacao_peso.zip
    ```

2.  **Navegue até o Diretório do Projeto:**

    ```bash
    cd sistema_verificacao_peso
    ```

3.  **Crie e Ative o Ambiente Virtual:**

    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

    ```bash
    python3 -m venv venv
    # Para ativar no Linux/macOS:
    source venv/bin/activate
    # Para ativar no Windows (Prompt de Comando):
    .\venv\Scripts\activate.bat
    # Para ativar no Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    ```

4.  **Instale as Dependências:**

    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a Aplicação Flask:**

    O sistema iniciará o servidor Flask. Por padrão, ele rodará na porta `5001`.

    ```bash
    python src/main.py
    ```

    Você deverá ver uma saída similar a:
    ```
     * Serving Flask app 'main'
     * Debug mode: on
     * Running on http://0.0.0.0:5001 (Press CTRL+C to quit)
    ```

## 🚀 Como Usar

1.  **Acesse a Interface Web:**

    Abra seu navegador e acesse `http://localhost:5001`.

2.  **Inicialize os Dados (Opcional, Primeira Vez):**

    Na primeira vez que você executar o sistema, se não houver peças cadastradas, ele tentará inicializar dados de exemplo automaticamente. Caso contrário, você pode forçar a inicialização acessando `http://localhost:5001/api/init-data` via POST (pode ser feito via Postman ou similar, ou o próprio frontend fará isso ao carregar).

3.  **Realize uma Verificação:**

    *   Selecione o **Tipo de Peça** no dropdown.
    *   Insira o **Peso Medido (kg)** manualmente ou clique em **


"Ler Balança" para simular uma leitura.
    *   Clique em **"Verificar Peso"**.

4.  **Visualize o Resultado:**

    O sistema exibirá o peso medido, a quantidade calculada, o peso esperado e a diferença, além de um status (PESO CORRETO, FALTANDO PEÇAS, PEÇAS EXTRAS).

5.  **Gere a Etiqueta:**

    Após a verificação, clique em **"Gerar Etiqueta"** para baixar o PDF com as informações e o QR Code.

6.  **Consulte o Histórico:**

    Todas as verificações são registradas e podem ser consultadas na tabela de histórico na parte inferior da página.

## 💡 Considerações para Produção

*   **Integração com Balança Real:** A simulação de balança pode ser substituída por um módulo de comunicação serial (RS-232 ou USB) para integração com balanças industriais reais. Isso exigirá desenvolvimento de drivers específicos para o modelo da balança.
*   **Servidor Web:** Para ambientes de produção, é recomendável usar um servidor WSGI como Gunicorn e um proxy reverso (Nginx ou Apache) para servir a aplicação Flask de forma mais robusta e segura.
*   **Banco de Dados:** Embora o SQLite seja adequado para testes e pequenas instalações, para alta concorrência ou grandes volumes de dados, considere migrar para PostgreSQL ou MySQL.
*   **Autenticação e Autorização:** Para ambientes multiusuário, a implementação de um sistema de autenticação e autorização (ex: login de usuários, diferentes níveis de acesso) é recomendada.
