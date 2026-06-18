Siga o template a seguir para gerar o projeto refatorado e saber onde colocar cada componente do novo projeto. Pequenas mudanças são aceitas se o framework destino tiver um padrão muito forte

src/main/kotlin/com/suaempresa/app/
├── AppApplication      # root (inicializa o projeto)
├── config/             # Configurações globais (Kafka, RestTemplate, Beans de Segurança)
├── controller/         # Ponto de entrada das requisições HTTP (Controllers)
├── model/              # Estruturas de dados (Models)
│   ├── entity/         # Classes mapeadas para o Banco de Dados
│   └── dto/            # Data Transfer Objects (Entrada e Saída da API)
├── service/            # Regras de negócio core (A "cola" da aplicação)
├── repository/         # Acesso ao banco de dados
├── integration/        # Clientes para serviços de terceiros (REST, Email)
│   ├── client/         # Integrações via HTTP (ex: OpenFeign ou RestClient)
│   └── email/          # Serviço de envio de e-mails
└── messaging/          # Mensageria assíncrona (Kafka)
    ├── producer/       # Envio de mensagens
    └── consumer/       # Escuta de tópicos
    