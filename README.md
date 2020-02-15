##Monitoramento avançado - IA
<h1 align="left">
    <img alt="Advanced Monitoring" src="https://www.sierraexperts.com/documents/2016/04/Infrastructure-Monitoring.png" width="200px" />
</h1>

## :rocket: Sobre o desenvolvedor

Este projeto é o desenvolvimento de um trabalho acadêmico (TCC) realizado para Universidade Paulista (UNIP) por Luis Vinhali, portado do número de matrícula N18202-4, em 2020.

## :rocket: Sobre o projeto

O projeto tem como core de desenvolvimento a monitorção de infraesturtura (servidores), incluindo diversos componentes como:

Componentes| Dados  |
---------- | ------ |
| CPU | total/livre/uso/etc |
| Memória | total/livre/uso/etc |
| Disco | total/livre/uso/etc |
| Processos | usuário/nativos/críticos/etc |
| Redes | outbound/inbound/regras/etc |
| Banco de dados | query/filesystems/permissões/etc |

Entre outros componentes possíveis de monitoração pela plataforma Zabbix.

Atualmente o monitoramento realizados por pequenas e grandes empresas é baseado em criar uma atuação técnica ou autômata em cima do treshold (limite) estabelicido na trigger (gatilho) do device monitorado. Agindo de forma não preventiva, ou seja, eliminando o problema após ocorrer. Em cima do que foi dissertado agora, o projeto tem como iniciativa gerar um monitoramento inteligente prevendo eventuais tendências de um device considerando sua matriz de criticidade ao ambiente do cliente, e além disso analisar se o treshold estabelicido é o recomendado para tal cenário, possibilitando gerar ações de correções para o problema pelo orquestrador de infraestrutura ansible, com visualização e documentação dos eventos com Grafana e GLPI.

<h1 align="center"><b> Diferença entre o projeto e a função forecast do Zabbix </b></h1>

Como pode ser lido na documentação oficial do ZABBIX a função forecast utiliza regressão linear, este projeto utiliza redes neurais recorrentes que são estruturas de processamento capazes de representar uma tendência com filtros não-lineares, ou seja, que não são vísiveis em linha, como o uso de memória de dispositivo.

<b>Exemplo:</b>

Um e-commerce possuí uma determinada demanda durante dias normais, em temporadas como black friday essa demanda não é linear.

[Forecast Zabbix](https://www.zabbix.com/documentation/3.0/pt/manual/config/triggers/prediction)

## :rocket: Esturtura do projeto

<h1 align="left">
    <img alt="Estrutura do projeto" src="https://i.ibb.co/L135GtG/MONITORING-EXPERT.png" width="500px" height="500px"/>
</h1>

## :rocket: Fases

:heavy_check_mark: Fase 1 - Instalação e configuração do ambiente em Linux (Debian stable 10)

:heavy_check_mark: Fase 2 - Configuração do Zabbix Server (Monitoramento)

:heavy_check_mark: Fase 3 - Configuração do PostgreSQL (Banco de Dados)

:heavy_check_mark: Fase 4 - Configuração do Ansible Server (Orquestrador de infraestrutura)

:heavy_check_mark: Fase 5 - Configuração do Grafana Server (Dashboard)

:heavy_check_mark: Fase 6 - Configuração do GLPI Server (Portal de chamados)

:heavy_check_mark: Fase 7 - Elaboração do código de redes neurais recorrentes em Python 

:heavy_check_mark: Fase 8 - Implementação dos dados de previsão com o Ansible

:heavy_check_mark: Fase 9 - Gerar chamados no portal GLPI

:heavy_check_mark: Fase 10 - Plotar todas as informações dentro do Dashboard Grafana


## :memo: Licença

Esse projeto está sob a licença das ferramentas open-source utilizadas para desenvolvimento, vide cada licença para implatação do código, não faça apropriação indébita de conteúdo intelectual, ou revenda algo que é gratuito!
