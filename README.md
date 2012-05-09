mapadeocorrencias
=================

Mapa de Ocorrências Policiais. 

Exemplo em: http://jgs.mapadeocorrencias.com.br/

Baseado no original https://github.com/Caged/portlandcrime, com as seguintes modificações:

- convertido para Python (era Ruby) 
- banco trocado de MongoDB para PostgreSQL/PostGIS. 
- simplificação: retirada dos scripts CoffeScript
- substituição do mapa da Cloudmade.com por um servidor de mapas próprio*

A parte visual permanece praticamente a mesma.

Underconstruction: Estou dando uma limpa no projeto para poder subi-lo.

(*) essa parte necessitará de uma mudança pois meu servidor só tem o mapa de eixos de Blumenau e de Jaraguá do Sul. 
Como meu servidor usa mesma tecnologia do Open Street Maps, a substituição será simples.