INTERATIVE_BOT_GREETING_MESSAGE = "Olá, cidadã(o), {0}!\n" + \
								  'Esse é o bot "QUE LEIS ESTÃO ROLANDO", criado para uma pesquisa dentro da Universidade de São Paulo.\n' + \
								  "Por aqui vou enviar Projetos de Lei (famosas PL) que estão passando atualmente pela Câmara dos Deputados para te manter informado(a)!\n\n" + \
								  "Você pode interagir comigo através dos botões presente abaixo de cada mensagem enviada.\n" + \
								  "Através deles posso:\n" + \
								  "- Te disponibilizar o link para a proposta na íntegra\n" + \
								  "- Enviar os autores responsáveis pela proposta\n" + \
								  "- Enviar as palavras chave da proposta\n" + \
								  "- O histórico de tramitações dela na câmara dos deputados\n" + \
								  "- E o despacho (deliberação) da mesma\n\n" + \
								  "É válido destacar que todos os prejos que envio eu pego diretamente da API de Dados Abertos da Câmara dos Deputados.\n" + \
								  "Inclusive, no final de cada mensagem vou enviar também o id da proposta na API, assim, se houver interesse, você poderá se informar mais por lá além do que eu te passar por aqui :)\n\n" + \
								  "Obrigado(a) por participar da pesquisa!"

SIMPLE_BOT_GREETING_MESSAGE = "Olá, {0}, bem vindo ao parque do dinossauros.\n" + \
							  "A ideia é que aqui eu fale um pouco sobre de onde a gente pega os dados e tal.\n" + \
							  "Também fale o que você pode fazer com esse bot...\n" + \
							  "Ah, e agradeço por participar da pesquisa.\n" + \
							  "Temos que formular isso aqui."

NEW_PL_MESSAGE_MODEL =  "PL {0}/{1}\n\n"        + \
						"EMENTA: {2}\n"         + \
						"Tramitação: {4}\n"     + \
						"Situação: {5}\n"       + \
						"Justificativa: {6}\n"  + \
						"Data: {7}\n\n"         + \
						"ID da PL na API de Dados Abertos: {8}"

PL_KEYWORDS_MESSAGE = "PL {0}/{1}\n\n"  + \
					  "PALAVRAS CHAVE: {2}"

PL_KEYWORDS_ERROR_MESSAGE  = "NÃO FOI ADICIONADO DESPACHO A ESSE PROJETO\n\n" + \
							 "Nem todos os projetos possuem palavras chave :(\n" + \
							 "Tente com outros projetos :)"							 

PL_DESPACHO_MESSAGE = "PL {0}/{1}\n\n"  + \
					  "DESPACHO: {2}"

PL_DESPACHO_ERROR_MESSAGE  = "NÃO FORAM FORNECIDAS PALAVRAS CHAVE PARA ESSE PROJETO\n\n" + \
							 "Tente novamente mais tarde ou com outros projetos :)"

DONT_KNOW_WHAT_TO_SAY = "Olá! Você está inscrito no chatbot QUE LEIS ESTÃO ROLANDO.\n\n"      + \
						"Eu não consigo entender ainda as mensagens que "                     + \
						"os usuários digitam, mas para interagir comigo você "                + \
						"pode usar os botões que aparecem embaixo das mensagens que envio!\n" + \
						"Sempre fico muito feliz em poder ajudar! :)\n\n"                     + \
						"Se estiver procurando mais informações sobre o projeto QUE LEIS "    + \
						"ESTÃO ROLANDO digite /start para receber nossa mensagem de boas vindas."
