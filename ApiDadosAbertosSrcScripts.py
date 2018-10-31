from DatabaseUtils import MongoDB
import Constants
import requests
import json

class ApiDadosAbertos:

	def showMeSomeNews():
		# settings to make the request
		get_url = Constants.DADOS_ABERTOS_BASE_API + Constants.PROPOSICOES_ENDPOINT
		headers = {'accept':'application/json'}
		page_number = 0
		# we will search for new PLs in every page until found one we haven't used yet
		while(True):
			page_number += 1
			parameters = {'siglaTipo':'PL',
						   'ordem':'DESC',
						   'ordenarPor':'id',
						   'pagina':page_number}
			# this request to the Dados Abertos API returns a list of projects (but they aren't complete)
			pls_list = requests.get(get_url, params=parameters, headers=headers).json().get('dados')
			for pl in pls_list:
				if(not MongoDB.verifyIfUsedPL(pl.get('id'))):
					# so, when we found a project that we haven't used yet, we request a more complete version of it 
					full_pl_infos = requests.get(pl.get('uri'), headers=headers).json().get('dados')
					if(full_pl_infos and MongoDB.insertNewUsedPL(full_pl_infos) == 'success'):
						return full_pl_infos

	def getTramitacoes(pl_id):
		try:
			# settings to make the request
			get_url = Constants.DADOS_ABERTOS_BASE_API + Constants.PROPOSICOES_TRAMITACOES_ENDPOINT.format(pl_id)
			headers = {'accept':'application/json'}
			# get and filter the data
			pl_history = requests.get(get_url, headers=headers).json().get('dados')
			return pl_history 
		except:
			return []