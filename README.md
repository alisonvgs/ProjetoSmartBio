# Projeto SmartBio - UPE
## Integrantes
Alison Vinicius, Caiubi Staffoker, Edson Gomes, Haderson Almeida e Thiago Oliveira
## Apresentação
Este projeto está sendo desenvolvido para a disciplina de Aplicações em Computação Inteligente (ACI), ministrado pelo Docente Dr. Carlo Marcelo Revoredo da Silva.
O projeto SmartBio trata-se do desenvolvimento de um biodigestor automatizado, o qual possuirá uma IA generativa LLM (LLaMA 3 - via Ollama) para reconhecer as imagens
dos objetos que serão despejados dentro do biodigestor e identificar quantos Kilowatts de potência o descarte irá produzir para poder realizar o carregamento de um carro
elétrico ou então para o suprimento domiciliar ou para o suprimento de uma padaria, por exemplo.
A IA também poderá verificar cada objeto descartado e indicar se o objeto apresenta algum problema para o biodigestor, como risco de explosão e assim avisar ao usuário final
para remoção do material despejado.
## Objetivo
Desenvolver um biogestor automatizado com uma IA Generativa que atuará sobre um modelo treinado, via Keras TensorFlow, com base em um dataset com 15.000 imagens.
## Base de dados e modelo desenvolvido
Base de dados para criação do modelo: https://www.kaggle.com/datasets/alistairking/recyclable-and-household-waste-classification/data

Link do modelo desenvolvido com Keras: https://drive.google.com/file/d/1SZC5xn94Iq2NEs9sqlut9YLo0znoNvxt/view?usp=drive_link

## Para rodar o código, siga as seguintes etapas:
1. Adicione o seguinte comando no seu computador:

### No Linux/macOS
export PYTHONPATH=$PYTHONPATH:/c/{caminho}/Documents/ProjetoSmartBio/

### No Windows (CMD)
set PYTHONPATH=%PYTHONPATH%;C:\{caminho}\Documents\ProjetoSmartBio\

### No Windows (PowerShell)
$env:PYTHONPATH += ";C:\{caminho}\Documents\ProjetoSmartBio\"

2. Se estiver utilizando o Promp de Comando, acesse a pasta de origem e depois envie o comando:
streamlit run c:\ {caminho} \ProjetoSmartBio\smartbio_app.py
3. Lembre-se que todos os arquivos devem estar dentro da mesma pasta, junto com o modelo Keras.
