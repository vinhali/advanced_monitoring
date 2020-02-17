## Monitoramento Avançado - IA
<h1 align="left">
    <img alt="Advanced Monitoring" src="https://i.imgur.com/HoeiIso.png" width="300px" />
</h1>

## :bust_in_silhouette: Sobre o desenvolvedor

Este projeto é o desenvolvimento de um trabalho acadêmico (TCC) realizado para Universidade Paulista (UNIP) por Luis Vinhali, portador do número de matrícula N18202-4, para apresentação no ano de 2020.

## :mortar_board: Orientadores

Prof. Mestre Amaury B. André

Prof. Mestre Mateus Locci


## :rocket: Sobre o projeto

O projeto tem como core de desenvolvimento a monitoração de infraestrutura (servidores), incluindo diversos componentes, como:

Componentes| Dados  |
---------- | ------ |
| CPU | total/livre/uso/etc |
| Memória | total/livre/uso/etc |
| Disco | total/livre/uso/etc |
| Processos | usuário/nativos/críticos/etc |
| Redes | outbound/inbound/regras/etc |
| Banco de dados | query/filesystems/permissões/etc |

Entre outros componentes possíveis de monitoração pela plataforma Zabbix.

Atualmente o monitoramento realizados por pequenas e grandes empresas é baseado em criar uma atuação técnica ou autômata em cima do treshold (limite) estabelicido pela trigger (gatilho) para o host/device monitorado. Agindo de forma não preventiva, ou seja, eliminando o problema após ocorrer.
<br>
Em cima do que foi dissertado agora, o projeto tem como iniciativa gerar um monitoramento inteligente prevendo eventuais tendências de um host/device considerando sua matriz de criticidade ao ambiente do cliente, e além disso analisar se o treshold estabelicido é o recomendado para tal cenário, possibilitando gerar ações de correções para o problema pelo orquestrador de infraestrutura ansible, com visualização e documentação dos eventos com Grafana e GLPI.


## :heavy_exclamation_mark: Diferença entre o projeto e a função forecast do Zabbix

Como pode ser lido na documentação oficial do ZABBIX a função forecast utiliza regressão linear, este projeto utiliza redes neurais recorrentes que são estruturas de processamento capazes de representar uma tendência com filtros não-lineares, ou seja, que não são vísiveis em linha, como o uso de memória de um dispositivo.

<b>Exemplo:</b>

Um e-commerce possuí uma determinada demanda durante dias normais, em temporadas como black friday essa demanda não é linear, ou seja, sua previsão só poder ser feita por algoritmos não-lineares como redes neurais recorrentes.

<h1 align="right">
    <a href="https://www.zabbix.com/documentation/3.0/pt/manual/config/triggers/prediction">
    <img alt="Forecast" src="https://assets.zabbix.com/img/logo/zabbix_logo_500x131.png" width="50px" height="25px"/>
    </a>
</h1>


## :skull: Estrutura do projeto

<h1 align="left">
    <img alt="Estrutura do projeto" src="https://i.ibb.co/L135GtG/MONITORING-EXPERT.png" width="500px" height="500px"/>
</h1>


## :computer: Fases

:heavy_check_mark: Fase 1 - Instalação e configuração do ambiente em Linux (Debian stable 10)

:heavy_check_mark: Fase 2 - Configuração do Zabbix Server (Monitoramento)

:heavy_check_mark: Fase 3 - Configuração do PostgreSQL (Banco de Dados)

:heavy_check_mark: Fase 4 - Configuração do Ansible Server (Orquestrador de infraestrutura)

:heavy_check_mark: Fase 5 - Configuração do Grafana Server (Dashboard)

:heavy_check_mark: Fase 6 - Configuração do GLPI Server (Portal de chamados)

:heavy_check_mark: Fase 7 - Elaboração do código de redes neurais recorrentes em Python 

:heavy_check_mark: Fase 8 - Implementação dos dados de previsão com o Ansible para correções automáticas

:heavy_check_mark: Fase 9 - Gerar chamados no portal GLPI

:heavy_check_mark: Fase 10 - Plotar todas as informações dentro do Dashboard Grafana

## :movie_camera: Cenário teste do projeto

Um cliente possuí um device alocado em cloud, onde essa máquina possuí configurações de baixo desempenho para economizar no valor de custo de horas online, levando em conta que a regra de negocío desse cliente é disponibilidade (24x7x365). A temporada de preço baixo está se aproximando, conhecida como BLACK FRIDAY, o CEO da empresa gostaria que seu monitoramento fosse realizado por demanda, ou seja, que a alocação de uma nova máquina só seja realizada quando necessário.
<br>
O Zabbix server é o responsável por monitorar o servidor que está alocado o banco de dados e serviço web dessa empresa, com tais informações coletadas o servidor de inteligência irá processar as informações coletadas em tempo real com as informações posteriores dessa temporada, considerando que a retenção de logs seja >= 365 dias.
<br>
Após esse processamento por redes neurais recorrentes utilizando Python como kernel da análise, os dados serão enviadas para o banco de dados PostgreSQL via batch, o script de health check irá ler os dados recém inseridos e buscar por possíveis problemas, após detectar um alto consumo de memória da máquina pelo banco de dados, irá realizar o START de uma nova máquina com configurações superiores a máquina em execução gerando um alerta no GLPI sobre o incidente que o ocorreu e quais foram as soluções testadas até o incidente ser tratado, gerando uma base histórica para facilitar a próxima análise, por fim o cliente e técnicos podem visualizar todo o processo de forma amigável pelo Dashboard criado no Grafana.


## :memo: Licença

Esse projeto está sob a licença das ferramentas open-source utilizadas para desenvolvimento, vide cada licença para implatação do código, não faça apropriação indébita de conteúdo intelectual, ou revenda algo que é gratuito!

## Tecnologias

![Zabbix version logo](https://img.shields.io/badge/Zabbix-v4.2+-green.svg?style=flat)
    
[![Python Version](https://img.shields.io/static/v1?label=python&message=3.7&color=green&logo=python)](https://www.python.org/downloads/release/python-370/)
[![Ansible Version](https://img.shields.io/static/v1?label=ansible&message=2.7.11&color=green&logo=ansible)](https://docs.ansible.com/ansible/2.7/)
[![Postgres Version](https://img.shields.io/static/v1?label=postgresql&message=11&color=green&logo=postgresql)](https://www.postgresql.org/about/news/1894/)
[![Zabbix Version](https://img.shields.io/static/v1?label=zabbix&message=4.4&color=green&logo=zabbix)](https://www.zabbix.com/whats_new_4_4)
[![Glpi Version](https://img.shields.io/static/v1?label=glpi&message=4.4&color=green&logo=glpi)](https://glpi-project.org/glpi-9-4-1/)
[![Grafana Version](https://img.shields.io/static/v1?label=grafana&message=6.6&color=green&logo=grafana)](https://grafana.com/blog/2020/01/27/grafana-v6.6-released/)
