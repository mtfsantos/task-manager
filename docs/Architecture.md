# Arquitetura do Projeto de Gestão de Tarefas

Este documento detalha as decisões arquiteturais e técnicas tomadas na construção do sistema de gestão de tarefas, bem como propostas para sua evolução e escalabilidade.

## Decisões Técnicas

### 1. Tecnologias e Frameworks Escolhidos

*   **Backend:**
    *   **Python (3.12+):** Linguagem versátil, com vasta comunidade e ecossistema robusto para desenvolvimento web e automação.
    *   **FastAPI:** Escolhido pela alta performance (comparável a Node.js e Go), tipagem estática com Pydantic, documentação automática (OpenAPI/Swagger UI) e facilidade de uso. É ideal para APIs RESTful, garantindo produtividade e código limpo.
    *   **Pydantic:** Integrado ao FastAPI, facilita a validação, serialização e deserialização de dados, definindo esquemas claros para as APIs.
    *   **SQLAlchemy:** ORM (Object-Relational Mapper) robusto e flexível para Python. Permite a interação com o banco de dados de forma orientada a objetos, desacoplando o código da complexidade das consultas SQL diretas.
    *   **SQLite:** Utilizado para fins de desenvolvimento e testes pela sua facilidade de configuração (arquivo único, sem necessidade de servidor DB separado).

*   **Frontend:**
    *   **React (com Vite):** React é uma das bibliotecas JavaScript mais populares para construir interfaces de usuário, conhecida por sua abordagem baseada em componentes, reatividade e grande comunidade. O Vite foi escolhido como ferramenta de build por sua velocidade de desenvolvimento e Hot Module Replacement (HMR) instantâneo, superando ferramentas mais antigas como Webpack em cenários de desenvolvimento.
    *   **Axios:** Cliente HTTP baseado em Promises para o navegador e Node.js. Oferece uma API simples e configurável para fazer requisições HTTP, facilitando a comunicação com a API RESTful do backend.
    *   **React Router DOM:** Para gerenciamento de rotas no lado do cliente, permitindo navegação declarativa entre as diferentes telas da aplicação.
    *   **CSS Puro / Tailwind CSS (Opcional):** Para estilização, priorizando simplicidade e clareza. Tailwind CSS poderia ser integrado para um desenvolvimento de UI mais rápido e consistente, se o tempo permitisse.

*   **Infraestrutura e DevOps:**
    *   **Docker e Docker Compose:** Essenciais para containerização. Permitem empacotar a aplicação e suas dependências em imagens portáteis, garantindo que o ambiente de desenvolvimento, teste e produção seja consistente. Docker Compose facilita a orquestração de múltiplos contêineres (backend, frontend) em ambiente local.
    *   **GitHub Actions:** Escolhido como plataforma de CI/CD pela sua integração nativa com o GitHub, facilidade de configuração via YAML, e vasta biblioteca de ações predefinidas. Permite automatizar testes, linting, builds e até mesmo deploys.
    *   **Terraform:** Ferramenta de Infraestrutura como Código (IaC) da HashiCorp. Permite definir e provisionar a infraestrutura em nuvem de forma declarativa e versionável. A inclusão de um setup básico na AWS demonstra familiaridade com IaC, um pilar fundamental para ambientes escaláveis e automatizados.

### 2. Estrutura de Pastas e Organização do Projeto

O projeto adota uma estrutura de monorepo simplificada, dividindo claramente as responsabilidades entre `backend`, `frontend`, `infra` e `docs`.

*   **`backend/`:** Contém todo o código da API FastAPI. Segue uma estrutura modular, separando:
    *   `api/`: Endpoints e dependências da API.
    *   `core/`: Configurações globais e segurança.
    *   `db/`: Modelos de banco de dados e configuração de sessão.
    *   `schemas/`: Modelos Pydantic para validação de dados.
    *   `services/`: Lógica de negócio (camada de serviço).
    *   `tests/`: Testes automatizados.
*   **`frontend/`:** Contém todo o código da aplicação React. Estruturado para modularidade com:
    *   `src/components/`: Componentes reutilizáveis de UI.
    *   `src/contexts/`: Gerenciamento de estado global (ex: autenticação).
    *   `src/api/`: funcoções para lógica reutilizável.
    *   `src/pages/`: Componentes que representam páginas inteiras.
    *   `src/services/`: Clientes de API e lógica de requisições.
*   **`infra/`:** Deverá conter os scripts de Infraestrutura como Código, segregados por provedor (ex: `aws/`).
*   **`docs/`:** Documentação adicional do projeto, como este arquivo e a simulação de distribuição de tarefas.
*   **`.github/workflows/`:** Deverá conter as definições do pipeline de CI/CD para GitHub Actions.
*   **Arquivos de Raiz:** `README.md`, `.gitignore`para configurar o ambiente global e o versionamento.

### 3. Estratégias de Separação de Responsabilidades

A separação de responsabilidades é um pilar fundamental para a manutenibilidade e escalabilidade do código.

*   **Backend (FastAPI):**
    *   **Camada de Roteamento/Endpoints (`api/endpoints`):** Responsável por receber requisições HTTP, validar dados de entrada (com Pydantic) e orquestrar a chamada para a camada de serviço. Mínima lógica de negócio aqui.
    *   **Camada de Serviço (`services`):** Contém a lógica de negócio principal da aplicação. Manipula as operações de CRUD, validações específicas do domínio e interage com a camada de dados. Isso garante que a lógica de negócio não esteja acoplada aos endpoints da API.
    *   **Camada de Dados (`db/models`, `db/session`):** Define os modelos de dados e gerencia a conexão e as operações de baixo nível com o banco de dados (via SQLAlchemy). Os serviços interagem com esta camada, mas não se preocupam com os detalhes de implementação do DB.
    *   **Schemas (`schemas`):** Usados para definir a estrutura de dados de entrada e saída da API, garantindo validação e tipagem claras.
    *   **Configurações e Segurança (`core`):** Funções e variáveis globais, como configurações de ambiente e utilitários de segurança, são centralizadas.

*   **Frontend (React):**
    *   **Componentes Reutilizáveis (`components`):** Partes da UI que podem ser usadas em várias páginas (botões, cards de tarefas, formulários genéricos). São "dumb" (presentational) ou com lógica interna focada no próprio componente.
    *   **Páginas (`pages`):** Componentes de alto nível que orquestram a composição de múltiplos componentes para formar uma tela completa. Contêm a lógica de chamada de API e gerenciamento de estado da página.
    *   **Serviços de API (`services/api.js`):** Encapsula todas as chamadas HTTP para o backend. Isso centraliza a configuração do Axios e facilita a manutenção das rotas da API.
    *   **Contextos (`contexts`):** Para gerenciamento de estado global (como autenticação), evitando prop drilling e facilitando o compartilhamento de dados entre componentes não relacionados diretamente.
    *   **Chamadas Customizadas (`api`):** Separado as chamadas especificas para integração com a API.

## Evolução e Escalabilidade

### 1. Propostas de Evolução da Aplicação

*   **Autenticação e Autorização Robustas:**
    *   Implementar autenticação JWT completa (geração, validação, refresh tokens) no backend.
    *   Adicionar gerenciamento de usuários com registro, recuperação de senha.
    *   Implementar controle de acesso baseado em papéis (RBAC) para diferentes níveis de usuários (administrador, usuário comum), permitindo, por exemplo, que apenas administradores possam remover tarefas de outros usuários.
*   **Notificações em Tempo Real:**
    *   Integrar WebSockets (ex: `websockets` no Python, `Socket.IO` no frontend) para notificações em tempo real sobre atualizações de tarefas (ex: "Tarefa X foi concluída por Y").
*   **Gerenciamento de Usuários e Equipes:**
    *   Permitir que tarefas sejam atribuídas a usuários específicos.
    *   Criação de equipes/projetos onde usuários podem colaborar em um conjunto de tarefas.
*   **Recursos Avançados de Tarefas:**
    *   Anexos (arquivos, imagens) para tarefas.
    *   Prazos e lembretes com integração a calendários (Google Calendar, Outlook).
    *   Subtarefas, prioridades e tags.
    *   Histórico de atividades por tarefa (quem fez o quê e quando).
*   **Pesquisa Avançada:**
    *   Implementar um motor de busca de texto completo para tarefas (ex: Elasticsearch, ou funções de busca nativas do DB).
*   **Interface do Usuário (UI/UX) Aprimorada:**
    *   Melhorias na experiência do usuário, como arrastar e soltar (drag-and-drop) para reorganizar tarefas ou alterar status.
    *   Visualizações alternativas (calendário, Kanban board).
*   **Terraform para Gestão de Recursos:**
    * Implementar Terraform como ferramenta principal de Infrastructure as Code (IaC)
    * Separar configurações por provedor (AWS, Azure, GCP, etc.)
    * Organizar em módulos reutilizáveis por tipo de recurso
    * Criar ambientes isolados (dev, staging, production). 
*   **Pipeline de CI/CD:**
    *   Desenvolver pipeline automatizado para deploy contínuo
    Integrar testes automatizados em todas as etapas
    Implementar aprovações manuais para ambientes críticos
    * Configurar rollback automático em caso de falhas

### 2. Sugestões Técnicas para Ganho de Performance e Manutenção

*   **Banco de Dados Robusto:** Migrar do SQLite para um SGBD de produção. Estes oferecem melhor performance, escalabilidade, recursos de backup/restauração, replicação e segurança.
*   **Camada de Caching:**
    *   Implementar caching em memória (ex: Redis) para dados frequentemente acessados (listas de tarefas populares, configurações). Isso reduz a carga no banco de dados e acelera as respostas da API.
    *   Caching HTTP (CDN, Nginx) para ativos estáticos do frontend.
*   **Otimização de Consultas (Backend):**
    *   Monitorar e otimizar consultas SQL (índices, `EXPLAIN ANALYZE`).
    *   Paginação e limitação de resultados para listas grandes.
*   **Monitoramento e Observabilidade:**
    *   Integração com ferramentas de monitoramento de performance de aplicações (APM) como Prometheus/Grafana, Datadog ou New Relic para coletar métricas (latência, erros, uso de recursos).
    *   Centralização de logs (ELK Stack, Loki/Grafana, AWS CloudWatch) para facilitar a depuração e análise de problemas.
    *   Tracing distribuído (OpenTelemetry, Jaeger) para entender o fluxo de requisições através de múltiplos serviços.
*   **Infraestrutura Escalável:**
    *   Migrar de uma única instância EC2 para arquiteturas mais escaláveis e resilientes:
        *   **Backend:** Deploy em contêineres gerenciados (AWS ECS Fargate, Kubernetes) com balanceamento de carga e auto-scaling.
        *   **Frontend:** Hospedagem de arquivos estáticos em um serviço como AWS S3 + CloudFront (CDN) para entrega rápida global.
    *   Utilizar Managed Databases Services (AWS RDS, Google Cloud SQL) para gerenciar o banco de dados.
*   **Testes Abrangentes:**
    *   Aumentar a cobertura de testes unitários e de integração.
    *   Implementar testes de end-to-end (e2e) com ferramentas como Cypress ou Playwright para simular o fluxo do usuário na interface.
    *   Realizar testes de carga (ex: JMeter, K6) para identificar gargalos de performance.
*   **Padronização de Código e Revisões:**
    *   Manter linters e formatadores de código (Black, ESLint, Prettier) configurados e aplicados via CI/CD para garantir consistência.
    *   Fortalecer a cultura de code review e pair programming para disseminar conhecimento e manter a qualidade do código.
*   **Documentação Contínua:**
    *   Manter a documentação da API atualizada (FastAPI gera automaticamente, mas validação e descrição são importantes).
    *   Manter a documentação arquitetural e de decisões técnicas como um artefato vivo do projeto.
*   **Gestão de Dependências:**
    *   Manter as dependências atualizadas, mas de forma controlada, para evitar vulnerabilidades de segurança e garantir compatibilidade.