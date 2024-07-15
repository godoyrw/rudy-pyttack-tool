# RUDY PyTTACK Tool 🐍
RUDY (Are You Dead Yet?), implementação do RUDY ataque de negação de serviço (DoS) em python.\
Version: 1.0.0

![alt text](https://github.com/godoyrw/rudy-pyttack-tool/blob/master/assets/img/rudy.jpg)

## Descrição
RUDY (Are You Dead Yet?) é uma ferramenta de ataque de negação de serviço (DoS) projetada para explorar e sobrecarregar a capacidade de resposta de servidores web, particularmente aqueles que têm vulnerabilidades relacionadas à forma como lidam com solicitações HTTP. Esse tipo de ataque visa esgotar os recursos do servidor, como a memória e a capacidade de processamento, manipulando a maneira como as solicitações HTTP são geradas e enviadas. O RUDY PyTTACK Tool funciona enviando requisições HTTP de forma lenta e progressiva, interrompendo o processo normal de resposta do servidor e forçando-o a manter conexões abertas por longos períodos. Isso pode levar a uma condição de sobrecarga onde o servidor não consegue atender a novas solicitações legítimas, resultando em um serviço interrompido para os usuários reais.

No contexto de implementação, o RUDY PyTTACK Tool pode ser utilizado para testar a robustez de sistemas web e a eficácia de suas medidas de segurança contra ataques de DoS. Em Python, uma implementação dessa ferramenta geralmente utiliza bibliotecas como requests para enviar requisições HTTP e socket para gerenciar conexões de rede. O ataque pode ser configurado para simular diferentes intensidades de carga e padrões de tráfego, proporcionando uma análise detalhada sobre como o servidor responde a diferentes cenários

## Instalação

#### Ambiente Virtual (virtual environment/venv)
```bash
    sudo apt install python3-venv -y
    python3 -m venv .venv
```

#### Ativação do ambiente virtual (active environment)
```bash
    source .venv/bin/activate
```

#### Instalação da lista de pacotes (dependencies list)
```bash
    pip3 install -r requirements.txt
```
## Usando
```
usage: rudy-pyttack [-h] [-s SOCKETS] [-t TIME] [-b BYTES] [-l LENGTH] [-x PROXY] [-v]
            [--version]
            url
rudy-pyttack 
Version: 1.0.0 
URL: https://github.com/godoyrw/rudy-pyttack-tool

positional arguments:
  url                   Absolute path to website, i.e
                        [http[s]://]host[:port][file_path]

optional arguments:
  -h, --help            show this help message and exit
  -s SOCKETS, --sockets SOCKETS
                        Number of sockets (connections) to use. Default is 150.
  -t TIME, --time TIME  Period of time in seconds that the program will wait before
                        performing another round of byte sending. Default is 10.
  -b BYTES, --bytes BYTES
                        Number of bytes that will be sent per round. Use it in
                        combination with -t, --time option in order to the set the
                        bandwidth. Default is 1.
  -l LENGTH, --length LENGTH
                        Content-Length value (bytes) in HTTP POST request. Default is
                        64.
  -x PROXY, --proxy PROXY
                        Send requests through a Socks5 proxy, e.g: 127.0.0.1:1080
  -v, --verbose         Give details about actions being performed.
  --ver                 Show version number and exit
```
## Exemplo de Uso
```
python3 rudy-pyttack.py -s 100 -t 5 https://localhost/index.php
```

## Isenção de responsabilidade (Disclaimer)

#### No entanto, é crucial lembrar que a utilização de ferramentas como o RUDY PyTTACK Tool deve ser estritamente instrutiva e ética. Seu uso deve ser limitado a ambientes controlados e de teste, com a devida autorização, para garantir que não cause danos a sistemas reais ou interrompa serviços críticos. Qualquer uso não autorizado ou malicioso de tais ferramentas pode resultar em consequências legais e éticas sérias.


#### Por favor, utilize este código exclusivamente para fins educacionais. É importante destacar que o uso malicioso de ferramentas de negação de serviço (DoS) pode ter sérias implicações legais. No Brasil, práticas como ataques DoS são consideradas crimes cibernéticos de acordo com a Lei nº 12.737/2012, conhecida como Lei Carolina Dieckmann, e outras legislações pertinentes. A realização de ataques que visam interromper serviços, comprometer sistemas ou causar danos a terceiros é punida com sanções severas, incluindo multas e penas de reclusão. Portanto, qualquer uso não autorizado ou prejudicial de tais ferramentas pode resultar em consequências legais graves. Não me responsabilizo por qualquer uso inadequado ou criminoso deste código.

## License & copyright
© Roberto Godoy - Octopus, Web Digital Solutions LTDA. All rights reserved\
Licensed under the [MIT License](LICENSE)
