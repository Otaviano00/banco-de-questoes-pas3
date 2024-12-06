Projeto protópico de banco de questões do PAS. Esse projeto busca na internet as pdfs das provas e gabaritos mais recentes do PAS 3, captura as questões, filtra e mostra para o usuário de forma aleatório.

O projeto ainda está em desenvolvimento, pois faltam muitas funcionalidades. Ainda tenho que arrumar os textos das questões (mas a maioria dos enunciados estão corretos), fazer a analise gráfica das questões que o usuário acertou ou não, separar as questões por tópicos, capturar as imagens e criar uma bateria de questões. Pretendo continuar com esse projeto e se possível torná-lo em um site.

Para executar esse programa, é necessário ter o poetry instalado. A partir disso, basta entrar na pasta onde está o pyproject, executar o comando "poetry install" (que instalará localmente as bibliotecas necessárias para o programa), executar o comando 

    "poetry shell" 

e executar o comando 

    "py  questoes\main.py" 

Ao iniciar, o programa irá baixar os pdfs (caso os pdfs não estejam já baixados), criar o arquivo 'questoes.csv' e mostrar na tela o menu de opções.
